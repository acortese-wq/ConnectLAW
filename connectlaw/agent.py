"""Agent-Kern: Anthropic Messages API mit Websuche, Prompt-Caching und
Multi-Turn-Verlauf.

Designentscheidungen (vgl. claude-api-Best-Practices):
- System-Prompt + [DOK]-Wissen werden als stabiles, gecachtes Präfix
  geführt (cache_control auf dem letzten System-Block). Tools rendern
  vor system, werden also mitgecacht.
- Adaptives Thinking (claude-opus-4-8) + output_config.effort.
- Server-seitiger web_search-Tool mit Domain-Beschränkung auf CH-Quellen.
- Streaming für gute CLI-UX; pause_turn wird im Loop aufgelöst, damit die
  server-seitige Such-Schleife sauber fortgesetzt wird.
"""

from __future__ import annotations

import anthropic

from .config import Config, SWISS_SEARCH_DOMAINS


class LegalAgent:
    """Mehrstufiger juristischer Chat-Agent mit persistentem Verlauf."""

    def __init__(
        self,
        config: Config,
        system_prompt: str,
        knowledge_text: str = "",
    ) -> None:
        self.config = config
        self.client = anthropic.Anthropic(api_key=config.api_key)
        self.system_blocks = self._build_system_blocks(system_prompt, knowledge_text)
        self.tools = self._build_tools()
        # Gesprächsverlauf (stateless API → vollständige Historie pro Aufruf).
        self.messages: list[dict] = []
        # Letzte finale Message (für Diagnose/usage).
        self.last_message: anthropic.types.Message | None = None

    # ------------------------------------------------------------------ #
    # Aufbau von System-Präfix und Tools
    # ------------------------------------------------------------------ #
    @staticmethod
    def _build_system_blocks(system_prompt: str, knowledge_text: str) -> list[dict]:
        blocks: list[dict] = [{"type": "text", "text": system_prompt}]
        if knowledge_text:
            blocks.append({"type": "text", "text": knowledge_text})
        # Cache-Breakpoint auf dem letzten stabilen System-Block:
        # cacht Tools + gesamtes System-Präfix gemeinsam.
        blocks[-1]["cache_control"] = {"type": "ephemeral"}
        return blocks

    def _build_tools(self) -> list[dict]:
        if not self.config.web_search:
            return []
        return [
            {
                "type": "web_search_20260209",
                "name": "web_search",
                # Technische Durchsetzung der CH-Quellenregel (Ziff. 4):
                "allowed_domains": SWISS_SEARCH_DOMAINS,
                "max_uses": self.config.web_search_max_uses,
            }
        ]

    # ------------------------------------------------------------------ #
    # Verlauf
    # ------------------------------------------------------------------ #
    def reset(self) -> None:
        """Setzt den Gesprächsverlauf zurück (System-Präfix bleibt erhalten)."""
        self.messages.clear()

    # ------------------------------------------------------------------ #
    # Eine Frage stellen (streamt die Antwort nach stdout)
    # ------------------------------------------------------------------ #
    def iter_answer(self, user_input: str):
        """Sendet eine Nutzerfrage und liefert Text-Deltas als Generator.

        Pflegt den Verlauf und löst pause_turn (server-seitige Websuche) auf.
        Die finale Message wird unter self.last_message abgelegt.
        """
        self.messages.append({"role": "user", "content": user_input})

        while True:  # Auflösung von pause_turn bei server-seitiger Websuche
            with self.client.messages.stream(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                system=self.system_blocks,
                thinking={"type": "adaptive"},
                output_config={"effort": self.config.effort},
                tools=self.tools,
                messages=self.messages,
            ) as stream:
                for text in stream.text_stream:
                    yield text
                final = stream.get_final_message()

            # Vollständigen Content (inkl. server_tool_use/thinking) anhängen.
            self.messages.append({"role": "assistant", "content": final.content})
            self.last_message = final

            if final.stop_reason == "pause_turn":
                # Server-seitige Such-Schleife hat das Iterationslimit erreicht;
                # erneut senden, damit der Server fortsetzt.
                continue
            break

    def ask(self, user_input: str, on_text=print) -> "anthropic.types.Message | None":
        """Sendet eine Nutzerfrage, streamt die Antwort und pflegt den Verlauf.

        on_text: Callback für Text-Deltas (Standard: print, flush).
        Rückgabe: die finale Message (für Diagnose/usage).
        """
        for text in self.iter_answer(user_input):
            on_text(text)
        return self.last_message
