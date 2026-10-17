// Small progressive enhancements; every page works without them (server-rendered, htmx for the
// sources panel and progress polling). Theme toggle, sources panel, option switch, part highlight,
// example chips, copy-as-reply, print.
(function () {
  "use strict";
  var root = document.documentElement;

  function effectiveTheme() {
    if (root.dataset.theme) return root.dataset.theme;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function initTabs(group) {
    var tabs = Array.prototype.slice.call(group.querySelectorAll('[role="tab"]'));
    function select(tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        var panel = document.getElementById(t.getAttribute("aria-controls"));
        if (panel) { if (on) panel.removeAttribute("data-hidden"); else panel.setAttribute("data-hidden", ""); }
      });
      if (focus) tab.focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(t, false); });
      t.addEventListener("keydown", function (ev) {
        var k = ev.key, n = tabs.length, next = null;
        if (k === "ArrowRight") next = tabs[(i + 1) % n];
        else if (k === "ArrowLeft") next = tabs[(i - 1 + n) % n];
        else if (k === "Home") next = tabs[0];
        else if (k === "End") next = tabs[n - 1];
        if (next) { ev.preventDefault(); select(next, true); }
      });
    });
  }

  // Hovering a node or a spec item highlights the matching parts of the drawn setup.
  function initHighlight(panel) {
    function set(parts, on) {
      panel.querySelectorAll(".sn").forEach(function (g) {
        if (parts.indexOf(g.getAttribute("data-part")) >= 0) g.classList.toggle("hl", on);
      });
    }
    panel.querySelectorAll(".specs > div[data-parts]").forEach(function (d) {
      var parts = d.getAttribute("data-parts").split(" ");
      ["mouseenter", "focusin"].forEach(function (e) { d.addEventListener(e, function () { d.classList.add("hl"); set(parts, true); }); });
      ["mouseleave", "focusout"].forEach(function (e) { d.addEventListener(e, function () { d.classList.remove("hl"); set(parts, false); }); });
    });
    panel.querySelectorAll(".sn").forEach(function (g) {
      g.addEventListener("mouseenter", function () { g.classList.add("hl"); });
      g.addEventListener("mouseleave", function () { g.classList.remove("hl"); });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var toggle = document.getElementById("theme-toggle");
    if (toggle) toggle.addEventListener("click", function () {
      var next = effectiveTheme() === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      try { localStorage.setItem("afs-theme", next); } catch (e) { /* private mode: no persistence */ }
    });

    document.querySelectorAll('[role="tablist"]').forEach(initTabs);
    document.querySelectorAll(".opt").forEach(initHighlight);

    // Example chips fill the question box instead of navigating.
    var box = document.getElementById("enquiry");
    document.querySelectorAll(".chip[data-fill]").forEach(function (c) {
      c.addEventListener("click", function (ev) {
        if (!box) return;
        ev.preventDefault();
        box.value = c.getAttribute("data-fill");
        box.focus();
      });
    });

    // Sources panel.
    var panel = document.getElementById("panel");
    var body = document.getElementById("panel-body");
    var closeBtn = document.getElementById("panel-close");
    var opener = null;
    function clearCurrent() {
      document.querySelectorAll('.tag[aria-current="true"]').forEach(function (t) { t.removeAttribute("aria-current"); });
    }
    function closePanel() {
      if (!panel || panel.hidden) return;
      panel.hidden = true;
      clearCurrent();
      if (opener) opener.focus();
    }
    document.addEventListener("click", function (ev) {
      var tag = ev.target.closest && ev.target.closest("a[data-panel]");
      if (tag) { opener = tag; clearCurrent(); tag.setAttribute("aria-current", "true"); }
    });
    document.body.addEventListener("htmx:afterSwap", function (ev) {
      if (body && ev.detail.target === body) { panel.hidden = false; body.scrollTop = 0; body.focus(); }
    });
    if (closeBtn) closeBtn.addEventListener("click", closePanel);
    document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") closePanel(); });

    // Hand-off: copy the plain-text reply; print with every folded row open.
    var status = document.querySelector(".handoff .copied");
    document.querySelectorAll("[data-copy]").forEach(function (b) {
      b.addEventListener("click", function () {
        var src = document.getElementById(b.getAttribute("data-copy"));
        if (!src) return;
        var done = function () { if (status) status.textContent = "Copied."; };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(src.value).then(done, function () { src.select(); document.execCommand("copy"); done(); });
        } else { src.select(); document.execCommand("copy"); done(); }
      });
    });
    var opened = [];
    window.addEventListener("beforeprint", function () {
      opened = [];
      document.querySelectorAll("details:not([open])").forEach(function (d) { d.open = true; opened.push(d); });
    });
    window.addEventListener("afterprint", function () { opened.forEach(function (d) { d.open = false; }); });
    document.querySelectorAll("[data-print]").forEach(function (b) { b.addEventListener("click", function () { window.print(); }); });

    // A submitted form shows it is working (the next page is the step list).
    document.querySelectorAll("form[method=post]").forEach(function (f) {
      f.addEventListener("submit", function () {
        var b = f.querySelector("button[type=submit]");
        if (b) { b.setAttribute("aria-busy", "true"); b.textContent = "Starting…"; }
      });
    });
  });
})();
