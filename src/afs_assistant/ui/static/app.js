// Small progressive enhancements; every page works without them (server-rendered, htmx for the
// sources panel and progress polling). Theme toggle, present mode, sources panel, margin notes, option switch,
// part highlight, example and follow-up chips, copy-as-reply, print.
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

  // Scrolling is instant when the person asks for reduced motion.
  function scrollBehavior() {
    return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth";
  }

  document.addEventListener("DOMContentLoaded", function () {
    // A conversation opens at its latest turn (a link to a part of the page keeps its own target).
    var thread = document.querySelector(".conversation");
    if (thread && !window.location.hash) {
      var turns = thread.querySelectorAll(".chat-turn");
      if (turns.length > 1) turns[turns.length - 1].scrollIntoView({ block: "start", behavior: "auto" });
    }

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
      root.classList.remove("panel-open");
      clearCurrent();
      if (opener) opener.focus();
    }
    document.addEventListener("click", function (ev) {
      var tag = ev.target.closest && ev.target.closest("a[data-panel]");
      if (tag) { opener = tag; clearCurrent(); tag.setAttribute("aria-current", "true"); }
    });
    document.body.addEventListener("htmx:afterSwap", function (ev) {
      if (body && ev.detail.target === body) { panel.hidden = false; root.classList.add("panel-open"); body.scrollTop = 0; body.focus(); }
    });
    if (closeBtn) closeBtn.addEventListener("click", closePanel);
    document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") closePanel(); });

    // Present mode: larger type and blocks for a projector; remembered per browser.
    var present = document.getElementById("present-toggle");
    if (present) {
      present.setAttribute("aria-pressed", root.dataset.present === "on" ? "true" : "false");
      present.addEventListener("click", function () {
        var on = root.dataset.present !== "on";
        if (on) root.dataset.present = "on"; else delete root.dataset.present;
        present.setAttribute("aria-pressed", on ? "true" : "false");
        try { localStorage.setItem("afs-present", on ? "on" : "off"); } catch (e) { /* no persistence */ }
      });
    }

    // Margin notes: a note's source link loads the verification view (quote in its page text, check result) into
    // the note itself (htmx); a second click closes it. A numbered reference in the text opens its note.
    function noteOf(el) { return el && el.closest ? el.closest(".mnote") : null; }
    function setNote(note, open) {
      var link = note.querySelector("a[data-note]");
      note.classList.toggle("is-open", open);
      if (link) link.setAttribute("aria-expanded", open ? "true" : "false");
      if (!open) { var ctx = note.querySelector(".mnote-ctx"); if (ctx) ctx.innerHTML = ""; }
    }
    document.body.addEventListener("htmx:beforeRequest", function (ev) {
      var link = ev.detail.elt;
      if (!link || !link.matches || !link.matches("a[data-note]")) return;
      var note = noteOf(link);
      if (note && note.classList.contains("is-open")) { ev.preventDefault(); setNote(note, false); }
    });
    document.body.addEventListener("htmx:afterSwap", function (ev) {
      var t = ev.detail.target;
      if (!t || !t.classList || !t.classList.contains("mnote-ctx")) return;
      setNote(noteOf(t), true);
      var box = t.querySelector(".source-text"), mark = box && box.querySelector("mark");
      if (mark) box.scrollTop = Math.max(0, mark.offsetTop - 48);   // the quote in view, with context (box is the offset parent)
    });
    document.addEventListener("click", function (ev) {
      var ref = ev.target.closest && ev.target.closest("a.ref[data-ref]");
      if (!ref) return;
      var note = document.getElementById(ref.getAttribute("data-ref"));
      if (!note) return;
      ev.preventDefault();
      document.querySelectorAll(".claim.is-active, .dek.is-active").forEach(function (c) { c.classList.remove("is-active"); });
      var said = ref.closest(".claim, .dek");
      if (said) said.classList.add("is-active");
      var link = note.querySelector("a[data-note]");
      if (link && !note.classList.contains("is-open")) link.click();
      note.scrollIntoView({ block: "nearest", behavior: scrollBehavior() });
      if (link) link.focus({ preventScroll: true });
    });

    // A job in this conversation that failed or was stopped (polling ended without a redirect): the composer
    // takes input again; the error stays visible in the step list.
    document.body.addEventListener("htmx:afterSettle", function () {
      var steps = document.getElementById("job-steps");
      var composer = document.querySelector(".composer");
      if (!steps || !composer || steps.hasAttribute("hx-get")) return;
      composer.querySelectorAll("input[disabled], button[disabled]").forEach(function (el) { el.disabled = false; });
      var hint = document.getElementById("composer-hint");
      if (hint) hint.textContent = "This question did not finish. You can send it again.";
    });

    // Suggested follow-ups fill the composer; the person still sends.
    var ask = document.getElementById("ask");
    document.querySelectorAll(".chip[data-ask]").forEach(function (c) {
      c.addEventListener("click", function () {
        if (!ask || ask.disabled) return;
        ask.value = c.getAttribute("data-ask");
        ask.focus();
      });
    });

    // Hand-off: copy the plain-text reply; print with every folded row open.
    document.querySelectorAll("[data-copy]").forEach(function (b) {
      var status = b.parentElement.querySelector(".copied");
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
