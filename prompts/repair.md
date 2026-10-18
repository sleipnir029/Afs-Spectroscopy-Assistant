Your previous assessment failed automatic verification. Below are your previous JSON and the list of failures, each with its location.

Fix ONLY the failing items and return the complete corrected assessment JSON.

- **quote failures:** replace the quote with an exact passage from the cited page that supports the claim. If no passage on any supplied page supports it, remove the citation and either soften the claim to what the sources do say, or move the point to `not_in_sources` / `key_unknowns`.
- **scope failures:** cite a page whose scope supports the claim, or reword the claim as a reason to test rather than proof.
- **number failures:** remove the figure, or use only a number that appears in that item's own quote or in the enquiry.
- **screen failures:** a failed candidate may only appear with role `not_recommended`, with its reason.
- **unknown-slot failures:** add a clarification question about that property, or state the assumption explicitly.
- **status failures:** make `decision_status` consistent with the premise checks and recommendations.
- **forbidden wording:** rephrase cautiously.
- **option failures:** give 2-3 solution options with distinct tiers and exactly one `recommended`; reference only existing recommendation ids that are not `not_recommended` and existing parameter ids; no two options may use the same set of recommendation ids; give the `extended` option a `fusion_note`; every `spectroscopy` parameter's method must be used by some option.
- **duplicate ids:** give every recommendation, option and parameter its own id and update the references.
- **proposal / brief answer failures:** fill the empty fields; `best_current_option` must be one of the option ids.
- **single primary:** keep exactly one `primary`; make the others `comparison` or `conditional`.
- **premise-status failures:** `premise_not_supported` needs a `contradicted` premise check; otherwise choose another status.
- **questions for unknowns:** add the deciding clarification questions for the open key unknowns, Q1 first, each with `affects`.
- **extended with two methods:** give the `extended` option a second, different method (another recommendation, or the primary); a recommendation's own method in its `combined_with` does not count.

Do not change items that passed. Do not add new claims without exact citations.
