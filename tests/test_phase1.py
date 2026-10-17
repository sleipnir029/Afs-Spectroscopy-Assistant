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
    assert c[("NIR", "transmission_transflection")].status == "fail"
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
    c = _by(screen({"physical_state": "liquid", "optical_regime": "clear", "fiber_family": "silica"}))
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
    assert quotes.verify("S01", 10, "NIR spectra (780-2500 nm) contain predominantly overtonez").status == "fuzzy"
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


# --------------------------------------------------------------------- scope
def test_scope_rules():
    assert scope.check("readiness_clinical", "S03", 14)[0] is False
    assert scope.check("readiness_process", "S02", 14)[0] is True
    assert scope.check("readiness_process", "S02", 13)[0] is False
    assert scope.check("general", "S01", 10)[0] is True
    assert scope.check("general", "S01", 99)[0] is False


# --------------------------------------------------------------------- knowledge base
def test_kb_check_all_pass():
    failed = [f for f in kb_check.run() if not f.ok]
    assert not failed, failed


def test_case_id_pattern():
    assert kb_check.CASE_ID.search("see D03 here")
    assert not kb_check.CASE_ID.search("D09 or HD01x or ID01")
