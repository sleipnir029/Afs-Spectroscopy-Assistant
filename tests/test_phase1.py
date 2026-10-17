"""Phase 1 acceptance tests: normalisation, units, fibers, screening, quotes, numbers, scope, KB."""

from __future__ import annotations

import pytest

from afs_assistant import kb, kb_check, quotes, scope
from afs_assistant.fibers import coverage, method_fiber_coverage
from afs_assistant.normalize import loose, normalize
from afs_assistant.numbers import find_numbers, unsupported_numbers
from afs_assistant.screen import screen
from afs_assistant.units import convert, range_to_um, to_um


# --------------------------------------------------------------------- normalisation
def test_normalize_ligature_dash_whitespace():
    assert normalize("conﬁrmed  the\nresult – here") == "confirmed the result - here"


def test_normalize_keeps_line_break_hyphen():
    assert normalize("measure-\nment of fiber-\noptic") == "measure-ment of fiber-optic"
    assert loose("measure-ment") == loose("measurement")


# --------------------------------------------------------------------- units
def test_wavenumber_to_micrometre():
    assert to_um(4000, "cm-1") == pytest.approx(2.5)
    assert convert(2.5, "um", "nm") == pytest.approx(2500)
    assert range_to_um(4000, 400, "cm-1") == pytest.approx((2.5, 25.0))


def test_unknown_unit_rejected():
    with pytest.raises(ValueError):
        to_um(1, "furlong")


# --------------------------------------------------------------------- fibers
def _status(cov, fiber_id):
    return next(c.status for c in cov if c.fiber_id == fiber_id)


def test_silica_does_not_cover_mir():
    cov = coverage(2.5, 25, "um")
    assert _status(cov, "silica_vis_nir") == "none"
    assert _status(cov, "silica_uv_vis") == "none"


def test_cir_covers_short_mir_and_pir_does_not():
    assert _status(coverage(2.5, 6.5, "um"), "cir_chalcogenide") == "full"
    assert _status(coverage(2.5, 3.0, "um"), "pir_polycrystalline") == "none"


def test_silica_covers_nir_only_partially():
    assert _status(method_fiber_coverage("NIR"), "silica_vis_nir") == "partial"


# --------------------------------------------------------------------- screening
def _by(cands):
    return {(c.method, c.technique): c for c in cands}


def test_opaque_liquid_excludes_transmission_keeps_reflection_atr_raman():
    c = _by(screen({"physical_state": "liquid", "optical_regime": "opaque"}))
    assert c[("NIR", "transmission_transflection")].status == "unknown"  # transflection stays open (R-GEO-5)
    assert any(r["rule"] == "R-GEO-2" for r in c[("NIR", "transmission_transflection")].reasons)
    assert c[("NIR", "diffuse_reflection")].status == "pass"
    assert c[("MIR", "ATR")].status == "pass"
    assert c[("Raman", "raman_probe")].status == "pass"


def test_unknown_regime_gives_unknown_not_fail():
    """Regression: a shadowed variable once failed ATR for liquids with an unknown regime."""
    c = _by(screen({"physical_state": "liquid"}))
    assert c[("NIR", "transmission_transflection")].status == "unknown"
    assert c[("MIR", "ATR")].status == "pass"


def test_empty_slots_never_fail():
    assert all(c.status in ("unknown", "pass") for c in screen({}))


def test_fluorescence_needs_fluorophore():
    unknown = _by(screen({"physical_state": "liquid", "optical_regime": "clear"}))
    no = _by(screen({"physical_state": "liquid", "optical_regime": "clear", "fluorophore": "no"}))
    yes = _by(screen({"physical_state": "liquid", "optical_regime": "clear", "fluorophore": "yes"}))
    key = ("Fluorescence", "fluorescence_probe")
    assert (unknown[key].status, no[key].status, yes[key].status) == ("unknown", "fail", "pass")


def test_silica_link_fails_mir_but_not_nir():
    c = _by(screen({"physical_state": "liquid", "optical_regime": "clear",
                    "proposed_fiber": {"family": "silica"}}))
    assert c[("MIR", "ATR")].status == "fail"
    assert any(r["rule"] == "R-FIB-1" for r in c[("MIR", "ATR")].reasons)
    assert c[("NIR", "transmission_transflection")].status == "pass"


def test_powder_excludes_atr():
    c = _by(screen({"physical_state": "powder", "optical_regime": "opaque"}))
    assert c[("MIR", "ATR")].status == "fail"
    assert c[("NIR", "diffuse_reflection")].status == "pass"


# --------------------------------------------------------------------- quotes
def test_quote_exact_with_offsets_and_hash():
    c = quotes.verify("S01", 10, "NIR spectra (780–2500 nm)")
    page = kb.page("S01", 10)
    assert c.status == "exact"
    assert page["text"][c.start:c.end] == normalize("NIR spectra (780–2500 nm)")
    assert c.page_sha256 == page["sha256"]


def test_quote_loose_and_fuzzy_and_missing():
    assert quotes.verify("S01", 10, "near-ir VIBRATIONAL spectroscopy (NIR)").status == "loose"
    near = quotes.verify("S01", 10, "NIR spectra (780-2500 nm) contain predominantly overtonez")
    assert near.status == "fuzzy_review" and not near.ok
    assert quotes.verify("S01", 10, "Raman is the best method for every customer").status == "not_found"
    assert quotes.verify("S01", 99, "anything at all here").status == "bad_page"
    assert quotes.verify("S01", 10, "NIR").status == "too_short"


def test_quote_on_wrong_page_is_not_found():
    assert not quotes.verify("S01", 11, "NIR spectra (780-2500 nm)").ok


# --------------------------------------------------------------------- numbers
def test_numbers_found_and_locators_ignored():
    found = [n.text for n in find_numbers("Use 780–2500 nm (S01 p.10, Table 1, R-FIB-1) at 4000 cm-1.")]
    assert found == ["780-2500 nm", "4000 cm-1"]


def test_unsupported_numbers_flagged():
    answer = "NIR 780-2500 nm gives 0.5% accuracy over a 150 m fiber."
    flagged = [n.text for n in unsupported_numbers(answer, ["NIR spectra (780-2500 nm)"])]
    assert flagged == ["0.5%", "150 m"]


ALLOWED = ["below 0.1 percent", "NIR spectra (780-2500 nm)", "Robust 100-300m cables", "(4000-400 cm-1)", "2400 nm"]


@pytest.mark.parametrize("answer", ["detection limit 0.1 mg/L", "accuracy 300 %", "range 100-2500 nm",
                                    "1,000 m", "-5 °C", "10x", "3.0 m"])
def test_numbers_need_same_value_and_unit_dimension(answer):
    assert unsupported_numbers(answer, ALLOWED), answer


@pytest.mark.parametrize("answer", ["below 0.1 %", "NIR 780–2500 nm", "2.4 µm", "2.5-25 µm", "4000 cm-1"])
def test_numbers_supported_across_unit_spellings(answer):
    assert not unsupported_numbers(answer, ALLOWED), answer


def test_numbers_ignore_locators_labels_and_small_counts():
    assert find_numbers("S01 p.10-11, Phase 2, Stage 3 of 5, Path A, 5 questions, 2 methods") == []
    assert find_numbers("1. First step") == []


# --------------------------------------------------------------------- scope
def test_scope_rules():
    assert scope.check("readiness_clinical", "S03", 14)[0] == "not_supported"
    assert scope.check("readiness_process", "S02", 14)[0] == "precedent_only"
    assert scope.check("readiness_process", "S02", 13)[0] == "not_supported"
    assert scope.check("general", "S01", 10)[0] == "ok"
    assert scope.check("general", "S01", 99)[0] == "not_supported"
    assert scope.check("general", "S05", 1)[0] == "not_supported"


def test_mixed_tag_literature_pages_cannot_support_readiness():
    """Review B6: S01 p.14/15 are process example AND literature map."""
    assert scope.check("readiness_process", "S01", 14)[0] == "not_supported"
    assert scope.check("readiness_process", "S01", 15)[0] == "not_supported"


def test_scope_unknown_claim_kind_raises():
    with pytest.raises(ValueError):
        scope.check("proof", "S01", 10)


# --------------------------------------------------------------------- knowledge base
def test_kb_check_all_pass():
    failed = [f for f in kb_check.run() if not f.ok]
    assert not failed, failed


def test_case_id_pattern():
    assert kb_check.CASE_ID.search("see D03 here")
    assert not kb_check.CASE_ID.search("D09 or HD01x or ID01")


# --------------------------------------------------------------------- review fixes (1.R)
@pytest.mark.parametrize("quote", [
    "may lack the sensitivity to detect trace compounds above 0.1 percent.",
    "may lack the sensitivity to detect trace compounds below 1 percent.",
])
def test_fuzzy_rejects_changed_numbers_or_comparisons(quote):
    assert quotes.verify("S01", 16, quote).status == "not_found"


def test_fuzzy_rejects_dropped_negation():
    assert quotes.verify("S01", 5, "However, most chemicals do exhibit this property.").status == "not_found"


def test_own_s02_descriptions_are_not_quotable():
    """Review B2: our figure descriptions live in `notes`, never in quotable text."""
    assert not quotes.verify("S02", 9, "laboratory comparison samples (lengths 1-2 m across slides 9-10)").ok
    assert not quotes.verify("S02", 13, "they look like prepared mixtures, but this is our inference").ok
    assert "Figure (our description)" in kb.page("S02", 13)["notes"]
    assert "Figure (our description)" not in kb.page("S02", 13)["text"]


def test_s02_text_layer_and_image_text_are_quotable():
    assert quotes.verify("S02", 16, "to work with 680nm & 785nm laser excitation").ok
    assert quotes.verify("S02", 10, "1.25 Meter Silver Halide - straight run").ok


def test_warn_rules_respect_target():
    """Review B5: a reflection warning must not land on ATR or Raman."""
    c = _by(screen({"physical_state": "liquid", "optical_regime": "clear"}))
    assert "R-GEO-4" in c[("NIR", "diffuse_reflection")].warnings
    assert "R-GEO-4" not in c[("MIR", "ATR")].warnings
    assert "R-GEO-4" not in c[("Raman", "raman_probe")].warnings
    cir = _by(screen({"physical_state": "liquid", "proposed_fiber": {"family": "chalcogenide", "for_method": "MIR"}}))
    assert "R-FIB-3" not in cir[("MIR", "ATR")].warnings


def test_opaque_liquid_transflection_is_unknown_not_fail():
    """Review B7: R-GEO-2 excludes transmission; R-GEO-5 keeps transflection open."""
    c = _by(screen({"physical_state": "liquid", "optical_regime": "opaque"}))
    cand = c[("NIR", "transmission_transflection")]
    assert cand.status == "unknown"
    assert any("R-GEO-5" in r["message"] for r in cand.reasons)


def test_proposed_fiber_applies_only_to_its_method():
    c = _by(screen({"physical_state": "liquid", "optical_regime": "clear",
                    "proposed_fiber": {"family": "chalcogenide", "for_method": "MIR"}}))
    assert c[("Raman", "raman_probe")].status == "pass"
    assert any("usable range" in n for n in c[("MIR", "ATR")].notes)


def test_dark_absorbing_sample_leaves_reflection_open():
    c = _by(screen({"physical_state": "liquid", "optical_regime": "opaque_absorbing"}))
    assert c[("NIR", "diffuse_reflection")].status == "unknown"
    assert c[("NIR", "transmission_transflection")].status == "unknown"


@pytest.mark.parametrize("slots", [{"physical_state": "gas"}, {"colour": "red"},
                                   {"proposed_fiber": {"family": "copper"}}])
def test_invalid_slots_raise(slots):
    with pytest.raises(ValueError):
        screen(slots)


def test_units_reject_zero_and_negative():
    with pytest.raises(ValueError):
        to_um(0, "cm-1")
    with pytest.raises(ValueError):
        convert(-5, "nm", "um")


def test_private_use_glyph_mapped():
    assert normalize("C\ue0c8O stretch") == "C=O stretch"


def test_r_fib_2_states_no_mir_link_length():
    rule = next(r for r in kb.rules() if r["id"] == "R-FIB-2")
    assert "No source states an achievable length for an MIR link" in rule["statement"]
    assert "2 m" not in rule["statement"].replace("1-2 m", "")
