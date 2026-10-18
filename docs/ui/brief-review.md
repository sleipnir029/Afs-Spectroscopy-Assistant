# C1 Brief restyle: independent UI/UX review (2026-10-18 ~11:55)

**Verdict: APPROVE WITH FIXES.**

## Blocking
1. Margin notes show an unverified recommendation quote exactly like a verified one (`conversation.html:92`). Add "not verified" and "precedent only" markers.
2. The pinned strip says "question 1 below is still open". "Below" has no fixed referent in a sticky strip. Use a short pinned form ("Q1 open") that links to the current sharpen block.
3. The page opens at the oldest turn: its v1 headline contradicts the v2 strip, so the 5-second test fails. Scroll to the latest turn on load, and collapse the body of earlier assessment turns into a closed `<details>`. Otherwise the thread reads as stacked one-off reports.

## Non-blocking
- Follow-up chips are fixed and generic. Build them from the data: setup per option, "why X not Y", top questions.
- The composer lock is a no-op. Give a reason when another job is running, and re-enable the composer after a failed job.
- The v3 hint is hidden on phones. "Provisional" appears twice.
- Two ways to check a citation (margin vs side panel).
- The header is crowded.
- Phone DOM order vs visual order (WCAG 2.4.3). Smooth scroll ignores reduced motion. No `aria-live` on the note context.
- Present-mode screenshot shows the hint. Newsreader is not preloaded.
- Checked and fine: XSS, works without JS, fonts self-hosted, contrast.

## Test gaps
Pinned strip; unique ids across turns; unverified marker; `cite.html` HX-Target id handling; chips hidden when busy.
