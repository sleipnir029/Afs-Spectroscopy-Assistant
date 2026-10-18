# Short brief view

One short page per final case (`H01.md` to `H06.md`, about 550 to 700 words each).

- **How it is made:** code builds it (`uv run afs-assist brief outputs/final --out outputs/final/brief`, module `src/afs_assistant/brief.py`) from the frozen run JSON (`outputs/final/H0x.json`). No model is called. The code only selects, orders and copies fields the run already holds, and it adds no facts. Running it again on the same JSON gives the same files.
- **The full answer is authoritative:** `outputs/final/H0x.md` (same case number) holds every section, the verified quote for each citation and the verification log. If the two ever differ, the full answer is right.
- **Section order:** the organiser's answer structure (REF §3) and worked answers: decision status, requirements, clarification questions, recommendation, measurement concept, spectral range, risks and uncertainty, feasibility plan, sources.
- **What is shortened:** fields and list items are chosen, never cut mid-sentence. This view shows the top 3 clarification questions, the top 3 risks, and the confidence level only (the reasons are in the full answer). It also shows the methods of the proposed option with their citations. Secondary literature appears only when a verified external item supports the proposed option, and then only one item.
- **Citations:** every `S0x p.N` / `REF §N` shown here is one the run verified verbatim on that page. A risk with no citation but with a tagged domain rule shows that rule's stored AFS quote as a *related AFS source*. That quote is checked verbatim on its page, but it has **not** been checked against the risk sentence.
- **Internal ids** (option, recommendation, question and parameter ids) are replaced by plain labels.

The development set has the same view in `outputs/dev/brief/`.
