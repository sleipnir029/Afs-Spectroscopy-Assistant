// Theme toggle and the citation side panel; everything else is server-rendered (htmx for the panel and polling).
(function () {
  "use strict";
  var root = document.documentElement;

  function effectiveTheme() {
    if (root.dataset.theme) return root.dataset.theme;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  document.addEventListener("DOMContentLoaded", function () {
    var toggle = document.getElementById("theme-toggle");
    if (toggle) {
      toggle.addEventListener("click", function () {
        var next = effectiveTheme() === "dark" ? "light" : "dark";
        root.dataset.theme = next;
        try { localStorage.setItem("afs-theme", next); } catch (e) { /* private mode: no persistence */ }
      });
    }

    var panel = document.getElementById("panel");
    var body = document.getElementById("panel-body");
    var closeBtn = document.getElementById("panel-close");
    var opener = null;

    function closePanel() {
      if (!panel || panel.hidden) return;
      panel.hidden = true;
      document.querySelectorAll('.tag[aria-current="true"]').forEach(function (t) { t.removeAttribute("aria-current"); });
      if (opener) opener.focus();
    }

    document.addEventListener("click", function (ev) {
      var tag = ev.target.closest && ev.target.closest("a[data-panel]");
      if (tag) {
        opener = tag;
        document.querySelectorAll('.tag[aria-current="true"]').forEach(function (t) { t.removeAttribute("aria-current"); });
        tag.setAttribute("aria-current", "true");
      }
    });
    document.body.addEventListener("htmx:afterSwap", function (ev) {
      if (ev.detail.target === body) {
        panel.hidden = false;
        body.scrollTop = 0;
        body.focus();
      }
    });
    if (closeBtn) closeBtn.addEventListener("click", closePanel);
    document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") closePanel(); });

    // A submitted form shows it is working (a run takes minutes; the next page is the step list).
    document.querySelectorAll("form").forEach(function (f) {
      f.addEventListener("submit", function () {
        var b = f.querySelector("button[type=submit]");
        if (b) { b.setAttribute("aria-busy", "true"); b.textContent = "Starting…"; }
      });
    });
  });
})();
