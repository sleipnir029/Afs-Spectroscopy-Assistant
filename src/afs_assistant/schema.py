"""Structured outputs of the two LLM stages (pydantic -> JSON schema for strict mode).

Intake  = AFS-Ashby steps 0-2 (route, translate the request, sample physics).
Assessment = steps 5-8 (rank, document, risks and questions, feasibility plan).
Steps 3-4 (screen, configure) are deterministic code between the two.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Method = Literal["NIR", "MIR", "Raman", "Fluorescence", "UV-Vis"]
Technique = Literal["ATR", "transmission_transflection", "diffuse_reflection", "diffuse_reflection_remote",
                    "raman_probe", "fluorescence_probe", "emission_probe", "combination", "to_be_determined"]
Basis = Literal["stated", "inferred_from_stated", "unknown"]
Doc = Literal["S01", "S02", "S03", "S04", "S05", "S06", "REF"]
# Claim kinds offered to the model. Readiness claims are deliberately not offered:
# no supplied source can support them (R-EVI-1/2), and the lexicon check blocks the wording.
ClaimKind = Literal["general", "application_precedent", "performance_figure", "method_gain"]


# ----------------------------------------------------------------- intake (steps 0-2)
class Fact(BaseModel):
    text: str = Field(description="One fact the customer stated, in plain words.")
    enquiry_quote: str = Field(description="Verbatim span from the enquiry that states it.")


class Target(BaseModel):
    variable: str
    purpose: str
    enquiry_quote: str


class StateSlot(BaseModel):
    value: Literal["liquid", "paste", "soft_solid", "powder", "solid", "unknown"]
    basis: Basis
    enquiry_quote: str | None


class RegimeSlot(BaseModel):
    value: Literal["clear", "turbid", "opaque", "opaque_absorbing", "unknown"]
    basis: Basis
    enquiry_quote: str | None


class YesNoSlot(BaseModel):
    value: Literal["yes", "no", "unknown"]
    basis: Basis
    enquiry_quote: str | None


class SampleSlots(BaseModel):
    physical_state: StateSlot
    optical_regime: RegimeSlot = Field(description="clear/turbid/opaque (scattering)/opaque_absorbing (dark).")
    aqueous: YesNoSlot
    heterogeneous: YesNoSlot
    fluorophore: YesNoSlot = Field(description="Is a fluorescent target or a justified fluorescent indicator identified?")


class ProcessFact(BaseModel):
    aspect: Literal["location", "temperature", "pressure", "distance_or_remote_analyzer", "hazardous_area",
                    "cleaning_or_fouling", "response_time", "existing_equipment", "reference_method",
                    "variability", "other"]
    value: str
    enquiry_quote: str


class Premise(BaseModel):
    claim: str = Field(description="An assumption, belief or request in the enquiry that must be checked against the sources.")
    enquiry_quote: str


class ProposedFiber(BaseModel):
    family: Literal["silica", "chalcogenide", "polycrystalline", "hollow_waveguide", "fluoride", "none"]
    for_method: Literal["NIR", "MIR", "Raman", "Fluorescence", "UV-Vis", "none"]
    enquiry_quote: str | None


class Intake(BaseModel):
    routes: list[Literal["in_scope", "needs_clarification", "premise_to_check", "certainty_or_approval_requested",
                         "clinical_context", "out_of_scope"]]
    summary: str = Field(description="One-sentence restatement of what the customer wants to know.")
    facts_stated: list[Fact]
    targets: list[Target]
    sample: SampleSlots
    process: list[ProcessFact]
    customer_premises: list[Premise]
    proposed_fiber: ProposedFiber
    unknowns: list[str] = Field(description="Information needed for a method choice that the enquiry does not give.")


# ----------------------------------------------------------------- assessment (steps 5-8)
class Citation(BaseModel):
    doc: Doc
    page: int = Field(description="1-based page; S02 = slide number; REF = section number (3 or 5).")
    quote: str = Field(description="Verbatim passage copied from that page's text.")
    claim_kind: ClaimKind


class PremiseCheck(BaseModel):
    premise: str
    verdict: Literal["supported", "contradicted", "not_covered", "precedent_only"] = Field(
        description="precedent_only: a source shows a similar published application; a reason to test, not proof.")
    explanation: str
    citations: list[Citation]


class Question(BaseModel):
    id: str = Field(description="Q1, Q2, ... in priority order.")
    question: str
    why_it_matters: str
    affects: list[str] = Field(description="What the answer could change; each item is exactly one of 'method', "
                                           "'technique', 'installation', 'status', or a recommendation id (M1, ...). "
                                           "'method' (the method choice) affects every option.")


class Recommendation(BaseModel):
    id: str = Field(description="M1, M2, ...")
    method: Method
    technique: Technique
    role: Literal["primary", "comparison", "conditional", "not_recommended"]
    combined_with: list[Method] = Field(description="Other methods to fuse with this one, as a later hypothesis "
                                                    "after single-method tests; always empty for role primary.")
    rationale: str
    conditions: str = Field(description="When this applies / what must be true; 'none' if unconditional.")
    citations: list[Citation]


class MeasurementConcept(BaseModel):
    probe_and_geometry: str
    location: str
    fiber_link: str
    citations: list[Citation]


class SpectralRange(BaseModel):
    method: Method
    statement: str = Field(description="Nominal range in correct units; say it is not an instrument/fiber range.")
    citations: list[Citation]


class Risk(BaseModel):
    risk: str
    rule_ids: list[str]
    citations: list[Citation]


class PlanStep(BaseModel):
    step: str
    purpose: str
    citations: list[Citation]


class FeasibilityPlan(BaseModel):
    steps: list[PlanStep]
    reference_measurements: str
    decision_basis: str = Field(description="Go/no-go basis; numerical criteria come from the customer, never invented.")


class MeasuredBy(BaseModel):
    type: Literal["spectroscopy", "auxiliary_sensor", "reference_lab", "not_measurable_inline"]
    method: Method | None = Field(description="The spectroscopy method if type is spectroscopy; else null.")
    sensor: str | None = Field(description="Free text naming the auxiliary sensor or reference lab method; else null.")
    alternative: str | None = Field(description="If not_measurable_inline: how it could be measured instead; else null.")


class Parameter(BaseModel):
    id: str = Field(description="P1, P2, ...")
    name: str
    kind: Literal["quantitative", "qualitative"]
    necessity: Literal["required", "optional"]
    why: str
    measured_by: MeasuredBy
    citations: list[Citation]


class SolutionOption(BaseModel):
    id: str = Field(description="O1, O2, ...")
    tier: Literal["simple", "recommended", "extended"]
    recommendation_ids: list[str] = Field(description="Recommendation ids (M1, ...) this option uses.")
    parameter_ids: list[str] = Field(description="Parameter ids (P1, ...) this option covers.")
    ease_of_use: str
    maintenance: str
    performance_fit: str
    cost_drivers: str = Field(description="What drives the cost, in words; never a price or currency.")
    fusion_note: str | None = Field(description="Required for the extended tier: fusion level, same sampling spot, "
                                                "synchronisation, per-block calibration, must beat the best single "
                                                "method. Else null.")
    citations: list[Citation]


class Proposal(BaseModel):
    best_current_option: str = Field(description="The option id (O1, ...) proposed now.")
    basis: Literal["supplied", "engineering_judgement"]
    what_would_change_it: str
    next_step: str


class Assessment(BaseModel):
    decision_status: Literal["provisional_assessment", "insufficient_information", "premise_not_supported",
                             "outside_supported_scope"]
    status_reason: str
    premise_checks: list[PremiseCheck]
    requirements_stated: list[str]
    key_unknowns: list[str]
    clarification_questions: list[Question]
    recommendations: list[Recommendation]
    measurement_concept: MeasurementConcept
    spectral_ranges: list[SpectralRange]
    risks: list[Risk]
    feasibility_plan: FeasibilityPlan
    assumptions: list[str]
    not_in_sources: list[str] = Field(description="Points the supplied sources do not cover (state them, do not fill them).")
    parameters: list[Parameter]
    solution_options: list[SolutionOption]
    chemometrics_note: str | None
    realtime_tracking_note: str | None
    future_direction: str | None
    proposal: Proposal
    brief_answer: str = Field(description="2-4 sentences in plain words.")
