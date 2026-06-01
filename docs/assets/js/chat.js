/* ConnectLAW – statisches Chat-Frontend.
 * Spricht ein konfigurierbares Backend (server.py) an. Es wird KEIN
 * API-Schlüssel im Browser gespeichert – der liegt ausschliesslich im Backend.
 */
(function () {
  "use strict";

  var LS_BACKEND = "connectlaw.backend";
  var LS_SESSION = "connectlaw.session";

  var els = {
    chat: document.getElementById("chat"),
    form: document.getElementById("composer"),
    input: document.getElementById("input"),
    send: document.getElementById("send-btn"),
    reset: document.getElementById("reset-btn"),
    settingsBtn: document.getElementById("settings-btn"),
    settings: document.getElementById("settings"),
    backendUrl: document.getElementById("backend-url"),
    health: document.getElementById("health"),
  };

  // ----- Sitzung & Backend-URL -------------------------------------- //
  function uuid() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    return "s-" + Date.now().toString(36) + Math.random().toString(36).slice(2);
  }

  var sessionId = localStorage.getItem(LS_SESSION);
  if (!sessionId) {
    sessionId = uuid();
    localStorage.setItem(LS_SESSION, sessionId);
  }

  function backend() {
    var url = (localStorage.getItem(LS_BACKEND) || "http://localhost:8000").trim();
    return url.replace(/\/+$/, "");
  }

  els.backendUrl.value = localStorage.getItem(LS_BACKEND) || "";
  els.backendUrl.addEventListener("change", function () {
    localStorage.setItem(LS_BACKEND, els.backendUrl.value.trim());
    checkHealth();
  });

  // ----- Hilfen ----------------------------------------------------- //
  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  // Hebt Risikohinweis-Zeilen (⚠) hervor; sonst reiner, escapter Text.
  function render(text) {
    return escapeHtml(text)
      .split("\n")
      .map(function (line) {
        if (line.indexOf("⚠") !== -1) return '<span class="warn-line">' + line + "</span>";
        return line;
      })
      .join("\n");
  }

  function clearEmptyHint() {
    var hint = els.chat.querySelector(".empty-hint");
    if (hint) hint.remove();
  }

  function showEmptyHint() {
    els.chat.innerHTML =
      '<div class="empty-hint"><h2>Interner juristischer Analyse-Assistent</h2>' +
      "<p>Schwerpunkt: Netzbau · Werkleitungen · Gestattungen · Tiefbau · Schadenregulierung (Schweizer Recht).</p>" +
      "<ul>" +
      "<li>Sachverhalt schildern → Analyse nach Schema Sachverhalt → Norm/Prinzip → Subsumtion → Ergebnis → Empfehlung.</li>" +
      "<li>Live-Recherche [WEB] nur auf Schweizer Quellen.</li>" +
      "<li>Erfundene Normen/Entscheide sind ausgeschlossen – im Zweifel: Rechtsdienst.</li>" +
      "</ul></div>";
  }

  function addMessage(role, initial) {
    clearEmptyHint();
    var wrap = document.createElement("div");
    wrap.className = "msg " + role;
    var avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = role === "user" ? "Sie" : "§";
    var bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.innerHTML = render(initial || "");
    wrap.appendChild(avatar);
    wrap.appendChild(bubble);
    els.chat.appendChild(wrap);
    els.chat.scrollTop = els.chat.scrollHeight;
    return bubble;
  }

  function setBusy(busy) {
    els.send.disabled = busy;
    els.input.disabled = busy;
  }

  // ----- Backend-Status --------------------------------------------- //
  function checkHealth() {
    els.health.textContent = "prüfe …";
    els.health.className = "health";
    fetch(backend() + "/health")
      .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
      .then(function (info) {
        els.health.textContent =
          "verbunden (" + info.model + ", effort=" + info.effort +
          (info.web_search ? ", Websuche an" : ", Websuche aus") + ")";
        els.health.className = "health ok";
      })
      .catch(function () {
        els.health.textContent = "nicht erreichbar – Backend starten & URL prüfen";
        els.health.className = "health err";
      });
  }

  // ----- Senden (mit Streaming) ------------------------------------- //
  function send(message) {
    addMessage("user", message);
    var bubble = addMessage("bot", "");
    bubble.innerHTML = '<span class="cursor">▋</span>';
    setBusy(true);

    var acc = "";

    fetch(backend() + "/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, message: message }),
    })
      .then(function (resp) {
        if (!resp.ok) throw new Error("HTTP " + resp.status);
        if (!resp.body || !resp.body.getReader) {
          return resp.text().then(function (t) { acc = t; bubble.innerHTML = render(acc); });
        }
        var reader = resp.body.getReader();
        var dec = new TextDecoder();
        function pump() {
          return reader.read().then(function (res) {
            if (res.done) {
              bubble.innerHTML = render(acc);
              return;
            }
            acc += dec.decode(res.value, { stream: true });
            bubble.innerHTML = render(acc) + '<span class="cursor">▋</span>';
            els.chat.scrollTop = els.chat.scrollHeight;
            return pump();
          });
        }
        return pump();
      })
      .catch(function (err) {
        bubble.innerHTML = render(
          (acc ? acc + "\n\n" : "") +
            "⚠ Verbindung zum Backend fehlgeschlagen (" + err.message + ").\n" +
            "Bitte unter ⚙ Backend die URL prüfen und das Backend starten."
        );
      })
      .finally(function () {
        setBusy(false);
        els.input.focus();
        els.chat.scrollTop = els.chat.scrollHeight;
      });
  }

  // ----- Events ----------------------------------------------------- //
  els.form.addEventListener("submit", function (e) {
    e.preventDefault();
    var msg = els.input.value.trim();
    if (!msg) return;
    els.input.value = "";
    els.input.style.height = "auto";
    send(msg);
  });

  // Enter = senden, Shift+Enter = neue Zeile
  els.input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      els.form.requestSubmit();
    }
  });

  // Auto-Höhe der Textarea
  els.input.addEventListener("input", function () {
    els.input.style.height = "auto";
    els.input.style.height = Math.min(els.input.scrollHeight, 180) + "px";
  });

  els.reset.addEventListener("click", function () {
    fetch(backend() + "/reset", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId }),
    }).catch(function () {});
    sessionId = uuid();
    localStorage.setItem(LS_SESSION, sessionId);
    showEmptyHint();
  });

  els.settingsBtn.addEventListener("click", function () {
    els.settings.classList.toggle("hidden");
    if (!els.settings.classList.contains("hidden")) checkHealth();
  });

  // ----- Start ------------------------------------------------------ //
  showEmptyHint();
  checkHealth();
})();
