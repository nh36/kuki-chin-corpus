#!/usr/bin/env python3
"""
Build a corpus-wide analyzer-based audit for Tedim stem alternation.

Outputs:
    - output/publication_review/stem_alternation_corpus_audit.tsv
    - output/publication_review/stem_alternation_environment_summary.tsv
    - output/publication_review/stem_alternation_pair_summary.tsv
    - output/publication_review/stem_alternation_example_matrix.tsv
    - output/publication_review/stem_alternation_lexical_inventory.tsv
    - output/publication_review/stem_alternation_promotable_examples.tsv

The audit uses the analyzer's stem-pair inventory plus the local Tedim token
export. `data/ctd_analysis/tokens.tsv` remains generated local build output and
is intentionally not tracked in git. The row-level audit is likewise generated
locally, while the smaller summaries and representative example matrix are
intended for git tracking.
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOKENS_PATH = ROOT / "data" / "ctd_analysis" / "tokens.tsv"
VERSES_PATH = ROOT / "data" / "verses_aligned.tsv"
OUTPUT_DIR = ROOT / "output" / "publication_review"
CORPUS_AUDIT_PATH = OUTPUT_DIR / "stem_alternation_corpus_audit.tsv"
ENV_SUMMARY_PATH = OUTPUT_DIR / "stem_alternation_environment_summary.tsv"
PAIR_SUMMARY_PATH = OUTPUT_DIR / "stem_alternation_pair_summary.tsv"
EXAMPLE_MATRIX_PATH = OUTPUT_DIR / "stem_alternation_example_matrix.tsv"
LEXICAL_INVENTORY_PATH = OUTPUT_DIR / "stem_alternation_lexical_inventory.tsv"
PROMOTABLE_EXAMPLES_PATH = OUTPUT_DIR / "stem_alternation_promotable_examples.tsv"
MANUAL_PROMOTION_REVIEW_PATH = OUTPUT_DIR / "stem_alternation_manual_promotion_review.tsv"
CANDIDATES_PATH = OUTPUT_DIR / "candidates_stem_alternation.tsv"
GRAMMAR_PACKET_PATH = OUTPUT_DIR / "grammar_stem_alternation_print_slice.md"
DICTIONARY_PACKET_PATH = OUTPUT_DIR / "dictionary_stem_alternation_print_slice.md"
REVIEW_NOTES_PATH = OUTPUT_DIR / "review_notes_stem_alternation.md"
DOSSIER_PATH = OUTPUT_DIR / "dossier_stem_alternation.md"
STEMS_LIT_REVIEW_PATH = ROOT / "docs" / "grammar" / "lit-reviews" / "05-verb-01-stems-lit.md"

sys.path.insert(0, str(ROOT / "scripts"))
from analyze_morphemes import VERB_STEM_PAIRS  # noqa: E402
from generate_vsa_report import PSC_TO_TEDIM  # noqa: E402


CORPUS_COLUMNS = [
    "pair_id",
    "form_i",
    "form_ii",
    "attested_form",
    "stem_form",
    "verse_id",
    "reference",
    "token_index",
    "surface_form",
    "normalized_form",
    "segmentation",
    "gloss",
    "lemma",
    "pos",
    "stem_alternation",
    "prefix_chain",
    "suffix_chain",
    "usage_type",
    "function_type",
    "local_context",
    "kjv",
    "inferred_environment",
    "environment_confidence",
    "print_status",
    "notes",
]

ENV_SUMMARY_COLUMNS = [
    "pair_id",
    "form_i",
    "form_ii",
    "environment",
    "form_i_count",
    "form_ii_count",
    "total_count",
    "representative_references",
    "notes",
]

PAIR_SUMMARY_COLUMNS = [
    "pair_id",
    "form_i",
    "form_ii",
    "gloss",
    "alternation_type",
    "form_i_total",
    "form_ii_total",
    "total",
    "dominant_form_i_environments",
    "dominant_form_ii_environments",
    "analyzer_status",
    "used_in_print_packet",
    "in_candidate_tsv",
    "candidate_statuses",
    "publication_status",
    "recommendation",
    "notes",
]

EXAMPLE_MATRIX_COLUMNS = [
    "pair_id",
    "form_i",
    "form_ii",
    "gloss",
    "alternation_type",
    "stem_side",
    "attested_form",
    "environment",
    "environment_count_for_side",
    "verse_id",
    "reference",
    "token_index",
    "surface_form",
    "normalized_form",
    "segmentation",
    "gloss_span",
    "lemma",
    "pos",
    "local_context",
    "kjv",
    "print_status",
    "selection_reason",
    "notes",
]

LEXICAL_INVENTORY_COLUMNS = [
    "lexeme_id",
    "form_i",
    "form_ii",
    "gloss",
    "alternation_type",
    "source_henderson",
    "source_zam_ngaih_cing",
    "source_vsa_questionnaire",
    "source_analyzer_inventory",
    "source_bible_audit",
    "source_project_review",
    "source_notes",
    "lexical_category",
    "category_evidence",
    "form_i_bible_attested",
    "form_ii_bible_attested",
    "form_i_clean_token_count",
    "form_ii_clean_token_count",
    "form_i_family_count",
    "form_ii_family_count",
    "clean_verb_form_i_count",
    "clean_verb_form_ii_count",
    "best_form_i_examples",
    "best_form_ii_examples",
    "best_clean_verb_form_i_examples",
    "best_clean_verb_form_ii_examples",
    "nominalized_examples",
    "dependent_temporal_examples",
    "purpose_examples",
    "relative_or_attributive_examples",
    "negative_examples",
    "finite_predicate_examples",
    "derived_or_causative_examples",
    "compound_or_lexicalized_examples",
    "homophone_or_noise_notes",
    "bible_attestation_profile",
    "lexical_pair_status",
    "recommended_grammar_treatment",
    "print_example_status",
    "promotion_status",
    "promotion_blocker",
    "notes",
]

PROMOTABLE_EXAMPLES_COLUMNS = [
    "lexeme_id",
    "form_side",
    "reference",
    "verse_id",
    "token_index",
    "surface_form",
    "normalized_form",
    "segmentation",
    "gloss_span",
    "lemma",
    "pos",
    "local_context",
    "kjv",
    "environment",
    "lexical_category",
    "example_quality",
    "reason_selected",
    "blocking_or_caveat_notes",
]

MANUAL_PROMOTION_REVIEW_COLUMNS = [
    "lexeme_id",
    "form_i",
    "form_ii",
    "gloss",
    "current_lexical_category",
    "current_promotion_status",
    "current_promotion_blocker",
    "clean_verb_form_i_count",
    "clean_verb_form_ii_count",
    "best_form_i_review_example",
    "best_form_ii_review_example",
    "environment_distribution_summary",
    "main_obstacle",
    "manual_review_decision",
    "recommended_new_promotion_status",
    "recommended_grammar_location",
    "decision_rationale",
    "next_manual_check",
]

REVIEW_CITED_SAFE_ENVIRONMENTS = {
    "finite_main_or_matrix",
    "dependent_temporal_ciangin",
    "dependent_temporal_ni_in",
    "clause_linking_kipan",
    "nominalized_na",
    "possessed_or_genitive_attributive",
    "relative_or_attributive_mi",
}

OBVIOUS_NOISY_ROW_FORMS = {
    "luimu",
    "muhdah",
    "mualtung",
    "mukte",
    "ngaihsun",
    "ngaihsut",
    "ngaihsutna",
    "ngaihsutna-in",
    "piangsak",
    "piangkhiasak",
    "piangsakin",
    "honkhia",
    "honkhiat",
    "hu",
    "huh",
}

MANUAL_REVIEW_ROW_ALLOWLIST = {
    ("mu-muh", "01019001", "20"): "print_usable_with_caveat",
    ("za-zak", "01003008", "13"): "print_usable_with_caveat",
    ("pia-piak", "01004005", "5"): "print_usable_with_caveat",
    ("nusia-nusiat", "01002024", "10"): "print_usable_with_caveat",
}

MANUAL_PUBLICATION_STATUS = {
    "mu-muh": "print_ready",
    "ne-nek": "print_ready",
    "nei-neih": "print_ready",
    "za-zak": "print_usable_with_caveat",
    "pia-piak": "print_usable_with_caveat",
    "nusia-nusiat": "print_usable_with_caveat",
    "thei-theih": "dossier_only",
    "piang-pian": "dossier_only",
    "ngai-ngaih": "dossier_only",
    "honkhia-honkhiat": "exclude_for_now",
    "hu-huh": "exclude_for_now",
}

LEXICAL_PAIR_STATUS_OVERRIDES = {
    "mu-muh": "established_pair",
    "ne-nek": "established_pair",
    "nei-neih": "established_pair",
    "za-zak": "established_pair",
    "pia-piak": "established_pair",
    "nusia-nusiat": "likely_pair",
    "thei-theih": "established_pair",
    "piang-pian": "likely_pair",
    "ngai-ngaih": "likely_pair",
    "honkhia-honkhiat": "lexicalized_or_category_mixed",
    "hu-huh": "lexicalized_or_category_mixed",
}

GRAMMAR_TREATMENT_OVERRIDES = {
    "mu-muh": "core_paradigm_example",
    "ne-nek": "core_paradigm_example",
    "nei-neih": "core_paradigm_example",
    "za-zak": "ordinary_inventory_entry",
    "pia-piak": "ordinary_inventory_entry",
    "nusia-nusiat": "ordinary_inventory_entry",
    "thei-theih": "discuss_under_modal_or_constructional_complexity",
    "piang-pian": "discuss_under_nominalization_or_dependent_clauses",
    "ngai-ngaih": "discuss_under_lexicalized_or_excluded_forms",
    "honkhia-honkhiat": "discuss_under_lexicalized_or_excluded_forms",
    "hu-huh": "discuss_under_lexicalized_or_excluded_forms",
}

PRINT_STATUS_RANK = {
    "print_ready": 5,
    "print_usable_with_caveat": 4,
    "dossier_only": 3,
    "needs_analyzer_review": 2,
    "exclude_for_now": 1,
}

ENVIRONMENT_PRIORITY = {
    "finite_main_or_matrix": 9,
    "imperative_or_directive": 8,
    "dependent_temporal_ciangin": 7,
    "dependent_temporal_ni_in": 7,
    "clause_linking_kipan": 7,
    "nominalized_na": 6,
    "relative_or_attributive_mi": 5,
    "possessed_or_genitive_attributive": 5,
    "purpose_nadingin": 4,
    "negative_clause": 3,
    "modal_or_ability": 2,
    "quotative_or_say_complement": 1,
    "unknown_or_needs_review": 0,
    "causative_or_derivational_sak": -1,
    "compound_or_lexicalized": -2,
}

SECONDARY_LITERATURE_PAIR_IDS = {
    "mu-muh",
    "ne-nek",
    "nei-neih",
    "ngai-ngaih",
    "thei-theih",
    "za-zak",
    "pia-piak",
    "piang-pian",
    "nusia-nusiat",
    "honkhia-honkhiat",
    "hu-huh",
    "pai-pai",
    "si-sit",
}

# These source maps are intentionally conservative. The repository does not
# currently contain an exhaustive extracted Tedim pair list from Henderson or
# Zam Ngaih Cing; mark a pair "yes" only when the in-repo literature review
# aligns it directly, and prefer "unverified" over implying complete coverage.
HENDERSON_SOURCE_STATUS = {
    "mu-muh": "yes",
    "ne-nek": "yes",
    "ci-cih": "yes",
    "hi-hih": "yes",
    "thei-theih": "yes",
    "si-sit": "unverified",
}

ZAM_SOURCE_STATUS = {
    "mu-muh": "yes",
    "pai-pai": "yes",
    "hoih-hoih": "yes",
}

LEXICAL_CATEGORY_OVERRIDES = {
    "mu-muh": "lexical_verb",
    "ne-nek": "lexical_verb",
    "nei-neih": "lexical_verb",
    "za-zak": "lexical_verb",
    "pia-piak": "lexical_verb",
    "nusia-nusiat": "lexical_verb",
    "bia-biak": "lexical_verb",
    "thei-theih": "lexical_verb",
    "piang-pian": "lexical_verb",
    "kho-khoh": "lexical_verb",
    "ngai-ngaih": "lexicalized_or_category_mixed",
    "honkhia-honkhiat": "lexicalized_or_category_mixed",
    "hu-huh": "lexicalized_or_category_mixed",
    "pua-puak": "lexicalized_or_category_mixed",
    "ci-cih": "auxiliary_or_functional_verb",
    "hi-hih": "auxiliary_or_functional_verb",
    "om-omh": "auxiliary_or_functional_verb",
    "no-noh": "stative_or_adjectival_predicate",
    "mual-mualh": "noun_or_nominal_compound",
    "sum-sumh": "noun_or_nominal_compound",
    "thu-thuh": "noun_or_nominal_compound",
    "lampi-lampih": "noun_or_nominal_compound",
    "khua-khuat": "noun_or_nominal_compound",
    "gamla-gamlat": "noun_or_nominal_compound",
    "mu-muk": "analyzer_only_uncertain",
    "ne-neh": "analyzer_only_uncertain",
    "pai-paih": "analyzer_only_uncertain",
    "pua-puah": "analyzer_only_uncertain",
    "tua-tuak": "analyzer_only_uncertain",
    "tua-tuah": "analyzer_only_uncertain",
    "kho-khot": "analyzer_only_uncertain",
}

BASELINE_PROMOTION_STATUS_OVERRIDES = {
    "mu-muh": "promote_to_main_grammar",
    "ne-nek": "promote_to_main_grammar",
    "nei-neih": "promote_to_main_grammar",
    "za-zak": "promote_with_caveat",
    "pia-piak": "promote_with_caveat",
    "nusia-nusiat": "promote_with_caveat",
    "bia-biak": "promote_with_caveat",
    "thei-theih": "discuss_as_difficult_case",
    "piang-pian": "discuss_as_difficult_case",
    "ngai-ngaih": "discuss_as_difficult_case",
    "honkhia-honkhiat": "discuss_as_difficult_case",
    "hu-huh": "discuss_as_difficult_case",
    "mu-muk": "discuss_as_difficult_case",
    "pua-puak": "discuss_as_difficult_case",
    "pua-puah": "discuss_as_difficult_case",
    "tua-tuak": "discuss_as_difficult_case",
    "tua-tuah": "discuss_as_difficult_case",
    "pai-paih": "mention_in_inventory_only",
    "kho-khoh": "mention_in_inventory_only",
    "ci-cih": "mention_in_inventory_only",
    "hi-hih": "mention_in_inventory_only",
    "om-omh": "block_from_verb_inventory_pending_review",
    "mual-mualh": "block_from_verb_inventory_pending_review",
    "sum-sumh": "block_from_verb_inventory_pending_review",
    "thu-thuh": "block_from_verb_inventory_pending_review",
    "lampi-lampih": "block_from_verb_inventory_pending_review",
    "khua-khuat": "block_from_verb_inventory_pending_review",
    "gamla-gamlat": "block_from_verb_inventory_pending_review",
    "no-noh": "mention_in_inventory_only",
}

PROMOTION_STATUS_OVERRIDES = {
    **BASELINE_PROMOTION_STATUS_OVERRIDES,
    "thei-theih": "promote_with_caveat",
    "piang-pian": "promote_with_caveat",
}

PROMOTION_BLOCKER_OVERRIDES = {
    "mu-muh": "none",
    "ne-nek": "none",
    "nei-neih": "none",
    "za-zak": "none",
    "pia-piak": "none",
    "nusia-nusiat": "none",
    "bia-biak": "needs_manual_philological_review",
    "thei-theih": "needs_manual_philological_review",
    "piang-pian": "needs_manual_philological_review",
    "ngai-ngaih": "lexicalized_family_contamination",
    "honkhia-honkhiat": "category_mismatch",
    "hu-huh": "category_mismatch",
    "mual-mualh": "nominal_or_compound_examples_only",
    "sum-sumh": "nominal_or_compound_examples_only",
    "thu-thuh": "nominal_or_compound_examples_only",
    "lampi-lampih": "nominal_or_compound_examples_only",
    "khua-khuat": "nominal_or_compound_examples_only",
    "gamla-gamlat": "nominal_or_compound_examples_only",
    "no-noh": "category_mismatch",
    "ci-cih": "category_mismatch",
    "hi-hih": "category_mismatch",
    "om-omh": "no_clean_form_ii_verb_example",
    "pai-paih": "needs_manual_philological_review",
    "pua-puak": "homophone_risk",
    "pua-puah": "analyzer_pair_only",
    "tua-tuak": "category_mismatch",
    "tua-tuah": "category_mismatch",
    "kho-khoh": "needs_manual_philological_review",
    "mu-muk": "analyzer_pair_only",
    "ne-neh": "analyzer_pair_only",
    "kho-khot": "analyzer_pair_only",
}

MANUAL_PROMOTION_REVIEW_TARGETS = {
    "mu-muh",
    "ne-nek",
    "nei-neih",
    "za-zak",
    "pia-piak",
    "nusia-nusiat",
    "bia-biak",
    "thei-theih",
    "piang-pian",
    "ngai-ngaih",
    "zui-zuih",
    "khial-khialh",
    "kia-kiak",
    "sawlkhia-sawlkhiat",
    "bawl-bawlh",
    "dipkua-dipkuat",
    "gen-genh",
    "hawlkhia-hawlkhiat",
    "husia-husiat",
    "kho-khoh",
    "kido-kidot",
    "lua-luah",
    "tu-tuh",
    "tuahpha-tuahphat",
    "vial-vialh",
    "pai-paih",
    "pua-puak",
    "pua-puah",
    "tua-tuak",
    "tua-tuah",
    "khai-khaih",
    "sia-siah",
    "tan-tanh",
    "keu-keuh",
}

MANUAL_REVIEW_OVERRIDES = {
    "mu-muh": {
        "manual_review_decision": "promote_now",
        "recommended_grammar_location": "main_promoted_verbal_inventory",
        "main_obstacle": "none",
        "decision_rationale": "Stable paired finite and derived evidence still makes this the clearest Tedim showcase pair.",
        "next_manual_check": "Keep the existing exact candidate-token examples.",
    },
    "ne-nek": {
        "manual_review_decision": "promote_now",
        "recommended_grammar_location": "main_promoted_verbal_inventory",
        "main_obstacle": "none",
        "decision_rationale": "Genesis 2:17 still provides the cleanest same-verse Form I/Form II contrast in the packet.",
        "next_manual_check": "Retain the same-verse contrast as the lead pedagogical example.",
    },
    "nei-neih": {
        "manual_review_decision": "promote_now",
        "recommended_grammar_location": "main_promoted_verbal_inventory",
        "main_obstacle": "none",
        "decision_rationale": "Both forms remain robust and easy to explain without major lexical contamination.",
        "next_manual_check": "Prefer an exact finite Form I plus attributable or nominalized Form II pairing.",
    },
    "za-zak": {
        "manual_review_decision": "promote_with_caveat_now",
        "recommended_grammar_location": "caveated_promoted_verbal_inventory",
        "main_obstacle": "Form II has broad lexical and environmental spread that still needs careful verse choice",
        "decision_rationale": "The pair is genuine and Bible-attested on both sides, but the grammar should keep the examples conservative because `zak` ranges more widely than the core showcase verbs.",
        "next_manual_check": "Keep choosing Form II tokens from transparent dependent or clause-linking contexts.",
    },
    "pia-piak": {
        "manual_review_decision": "promote_with_caveat_now",
        "recommended_grammar_location": "caveated_promoted_verbal_inventory",
        "main_obstacle": "report noise and derivational crowding around related `-sak` material",
        "decision_rationale": "Both forms have abundant clean verbal evidence, so the pair belongs in the promoted inventory, but the quoted examples still need filtering away from derivational neighbors.",
        "next_manual_check": "Prefer exact `pia`/`piak` rows that stay away from nearby causative morphology.",
    },
    "nusia-nusiat": {
        "manual_review_decision": "promote_with_caveat_now",
        "recommended_grammar_location": "caveated_promoted_verbal_inventory",
        "main_obstacle": "Form II is clearest in dependent and clause-linking environments rather than in a neat finite contrast",
        "decision_rationale": "The pair is already packet-worthy, but the grammar should frame it as a caveated promotion whose best evidence comes from non-final syntax rather than from a simple finite paradigm.",
        "next_manual_check": "Keep pairing the lexical inventory with dependent or clause-linking Form II examples.",
    },
    "bia-biak": {
        "manual_review_decision": "promote_with_caveat_now",
        "recommended_grammar_location": "caveated_promoted_verbal_inventory",
        "main_obstacle": "Form II is heavily clustered in worship, offering, and nominalized material",
        "decision_rationale": "Both forms survive as genuine verbal evidence, so the pair belongs in the promoted inventory, but the grammar should keep noting that the Form II distribution is domain-specific.",
        "next_manual_check": "Prefer a finite or purpose-context Form II token that avoids sacrificial lexical crowding.",
    },
    "thei-theih": {
        "manual_review_decision": "promote_with_caveat_now",
        "recommended_grammar_location": "caveated_promoted_verbal_inventory",
        "main_obstacle": "Form II is especially strong in modal, ability, purposive, and nominalized environments rather than in a neat finite pedagogical contrast",
        "decision_rationale": "Both forms are cleanly and abundantly attested. The grammar should now promote `thei ~ theih`, but explicitly under a modal or ability subsection rather than as if every Form II token were a plain finite alternant.",
        "next_manual_check": "Choose a tight modal or purposive Form II verse that does not rely only on nominalization.",
    },
    "piang-pian": {
        "manual_review_decision": "promote_with_caveat_now",
        "recommended_grammar_location": "caveated_promoted_verbal_inventory",
        "main_obstacle": "Form II competes with a large derived `piangsak` family and is easiest to show in eventive or dependent environments",
        "decision_rationale": "Exact `piang` and `pian` rows survive after filtering, so this pair deserves promotion. The prose should treat it as an eventive or intransitive caveated verb rather than as a simple mechanical alternation.",
        "next_manual_check": "Prefer an exact `pian` row that is eventive and clearly distinct from `piangsak` material.",
    },
    "ngai-ngaih": {
        "manual_review_decision": "retain_as_difficult_case",
        "recommended_grammar_location": "difficult_cases",
        "main_obstacle": "clean `ngai/ngaih` rows coexist with heavy lexical-family contamination from `ngaihsun/ngaihsut/ngaihsutna`",
        "decision_rationale": "The review should now state explicitly that clean exact verbal `ngai`/`ngaih` rows exist on both sides. Even so, the family contamination is still strong enough that this pair belongs in difficult cases rather than in the promoted inventory.",
        "next_manual_check": "Separate exact `ngai/ngaih` rows from `ngaihs-` family material in any future quotation shortlist.",
    },
    "zui-zuih": {
        "manual_review_decision": "promote_with_caveat_now",
        "recommended_grammar_location": "caveated_promoted_verbal_inventory",
        "main_obstacle": "derived `zuihsak` material and the need for a transparent Form II quotation context",
        "decision_rationale": "Both forms are cleanly attested and lexically coherent. `zui ~ zuih` should be promoted as a real caveated lexical verb rather than left implicit in the wider inventory.",
        "next_manual_check": "Prefer a Form II row that is exact and not crowded by causative or benefactive morphology.",
    },
    "khial-khialh": {
        "manual_review_decision": "promote_with_caveat_now",
        "recommended_grammar_location": "caveated_promoted_verbal_inventory",
        "main_obstacle": "the `khialsak` family still creates derivational noise around otherwise clean rows",
        "decision_rationale": "Both forms have enough clean verbal evidence for grammar discussion, so this pair should stay promoted with caveat.",
        "next_manual_check": "Prefer exact rows that stay away from `khialsak` and related causative material.",
    },
    "kia-kiak": {
        "manual_review_decision": "promote_with_caveat_now",
        "recommended_grammar_location": "caveated_promoted_verbal_inventory",
        "main_obstacle": "Form II is comparatively sparse and must be kept distinct from `kiasak`-family noise",
        "decision_rationale": "The surviving Form II evidence is thinner than for the best pairs, but it is still real verbal evidence, so the pair now belongs in the caveated promoted inventory.",
        "next_manual_check": "Keep the Form II citation exact and avoid nearby derivational morphology.",
    },
    "sawlkhia-sawlkhiat": {
        "manual_review_decision": "promote_with_caveat_now",
        "recommended_grammar_location": "caveated_promoted_verbal_inventory",
        "main_obstacle": "clean Form II examples are few and semantically crowded by expulsion or sending contexts",
        "decision_rationale": "The pair is lexically coherent and both forms are attested, but it should stay caveated until a cleaner Form II example set is isolated.",
        "next_manual_check": "Prefer a transparent non-negative Form II token with stable verbal POS.",
    },
    "bawl-bawlh": {
        "manual_review_decision": "retain_inventory_only",
        "recommended_grammar_location": "difficult_cases",
        "main_obstacle": "Bible evidence is effectively one-sided because the questionnaire control `bawl ~ bawl` already covers the overt written form",
        "decision_rationale": "The lexical verb remains relevant to the inventory, but there is still no clean overt Form II evidence to justify promotion into the alternating-verb table.",
        "next_manual_check": "Keep it in the one-sided inventory unless exact `bawlh` verbal rows appear.",
    },
    "dipkua-dipkuat": {
        "manual_review_decision": "retain_inventory_only",
        "recommended_grammar_location": "difficult_cases",
        "main_obstacle": "Form II currently survives only in nominalized or otherwise complex material",
        "decision_rationale": "The lexical item is probably real, but the current Bible evidence is too constructionally narrow for promotion.",
        "next_manual_check": "Look for an exact non-nominalized `dipkuat` verbal token before promoting it.",
    },
    "gen-genh": {
        "manual_review_decision": "retain_inventory_only",
        "recommended_grammar_location": "difficult_cases",
        "main_obstacle": "no clean verbal Form II evidence has survived the current audit",
        "decision_rationale": "The Bible strongly attests Form I, but promotion should wait until a defensible exact `genh` verbal token is isolated.",
        "next_manual_check": "Treat any future `genh` candidate as a manual philology item rather than auto-promoting it.",
    },
    "hawlkhia-hawlkhiat": {
        "manual_review_decision": "retain_inventory_only",
        "recommended_grammar_location": "difficult_cases",
        "main_obstacle": "current Form II candidates drift toward non-verbal or lemma-unstable readings",
        "decision_rationale": "The lexeme deserves inventory coverage, but the present Form II evidence is not yet clean enough for promotion.",
        "next_manual_check": "Require an exact verbal `hawlkhiat` token with stable lemma and POS before promotion.",
    },
    "kho-khoh": {
        "manual_review_decision": "retain_inventory_only",
        "recommended_grammar_location": "difficult_cases",
        "main_obstacle": "Form II remains effectively unattested as a clean verbal row, and the base overlaps with `kho-khot`",
        "decision_rationale": "The Form I side looks verbal enough to keep in the inventory, but the pair is still too one-sided for promotion.",
        "next_manual_check": "Review `khoh` against `kho-khot` and nominal uses before revisiting promotion.",
    },
    "pai-paih": {
        "manual_review_decision": "needs_more_manual_review",
        "recommended_grammar_location": "analyzer_only_uncertain",
        "main_obstacle": "the analyzer pair competes with the same-form questionnaire control `pai ~ pai`, and clean Form II evidence is sparse",
        "decision_rationale": "Exact `paih` verbal rows do exist, but the shared-base problem is still unresolved enough that the grammar should keep this under analyzer-only uncertainty rather than promote it.",
        "next_manual_check": "Do a dedicated philological pass on `pai`, `paih`, and the same-form questionnaire control before changing category or promotion status.",
    },
    "pua-puak": {
        "manual_review_decision": "retain_as_difficult_case",
        "recommended_grammar_location": "difficult_cases",
        "main_obstacle": "shared Form I base, gloss mismatch, and homophone risk across `pua ~ puak` and `pua ~ puah`",
        "decision_rationale": "Clean verbal rows exist for `pua` and `puak`, so the pair stays central to the discussion. But the overlap with other `pua` families is still too strong for routine promotion.",
        "next_manual_check": "Separate the 'spill' reading from questionnaire-style 'carry on back' material before any promotion change.",
    },
    "pua-puah": {
        "manual_review_decision": "needs_more_manual_review",
        "recommended_grammar_location": "analyzer_only_uncertain",
        "main_obstacle": "only the Form II side is cleanly verbal, and it shares its Form I base with `pua ~ puak`",
        "decision_rationale": "The current evidence is too one-sided to treat `pua ~ puah` as an independent promoted pair.",
        "next_manual_check": "Require exact verbal Form I evidence before revisiting this analyzer pair.",
    },
    "tua-tuak": {
        "manual_review_decision": "needs_more_manual_review",
        "recommended_grammar_location": "analyzer_only_uncertain",
        "main_obstacle": "the Form I base is overwhelmingly determiner-like, not verbal, and the shared-base mapping remains unstable",
        "decision_rationale": "This row is useful as a warning about analyzer overgeneration, but it should stay out of the promoted verb grammar.",
        "next_manual_check": "Do not promote unless both sides can be shown with stable verbal POS and lemma control.",
    },
    "tua-tuah": {
        "manual_review_decision": "needs_more_manual_review",
        "recommended_grammar_location": "analyzer_only_uncertain",
        "main_obstacle": "only the Form II side is currently cleanly verbal, while the Form I base remains category-mixed",
        "decision_rationale": "The pair remains interesting for analyzer review, but it is still too one-sided for promotion.",
        "next_manual_check": "Require exact verbal Form I evidence distinct from determiner or discourse uses of `tua`.",
    },
    "keu-keuh": {
        "manual_review_decision": "block_nonverbal",
        "recommended_grammar_location": "blocked_nonverbal_appendix",
        "main_obstacle": "current Bible hits are nominal rather than verbal on both sides",
        "decision_rationale": "This is the kind of analyzer pair the manual review is meant to keep out of the verb-stem alternation grammar.",
        "next_manual_check": "Leave blocked unless a clean verbal reading is documented for both forms.",
    },
}

VERBAL_ENVIRONMENTS = {
    "finite_main_or_matrix",
    "imperative_or_directive",
    "negative_clause",
    "dependent_temporal_ciangin",
    "dependent_temporal_ni_in",
    "clause_linking_kipan",
    "purpose_nadingin",
    "modal_or_ability",
    "quotative_or_say_complement",
}

ALLOWED_PREDICATIVE_NONV_POS = {
    "om-omh": {"ADJ"},
    "thei-theih": {"ADJ"},
}

SUPPLEMENTAL_PACKET_PAIRS = {
    "piang-pian": ("piang", "pian", "be.born"),
    "hu-huh": ("hu", "huh", "help"),
}

CANDIDATE_ALIASES = {
    "pia-piak-report-noise": "pia-piak",
    "ngai-ngaih-family": "ngai-ngaih",
}

NOISY_FORM_OVERRIDES = {
    "piangsak": "piang-pian",
    "piangkhiasak": "piang-pian",
    "piangsakin": "piang-pian",
    "ngaihsun": "ngai-ngaih",
    "ngaihsut": "ngai-ngaih",
    "ngaihsutna": "ngai-ngaih",
    "ngaihsutna-in": "ngai-ngaih",
    "neihsak": "nei-neih",
}

FORM_I_NOTE_PRIORITY = {
    "mu-muh": 10,
    "ne-nek": 10,
    "za-zak": 9,
    "pia-piak": 9,
    "nusia-nusiat": 9,
}


@dataclass(frozen=True)
class PairMeta:
    pair_id: str
    form_i: str
    form_ii: str
    gloss: str
    alternation_type: str
    analyzer_status: str
    used_in_print_packet: bool
    in_candidate_tsv: bool
    candidate_statuses: tuple[str, ...]
    publication_status: str
    notes: str


def require_tokens_export() -> None:
    if TOKENS_PATH.exists():
        return
    raise SystemExit(
        "Missing data/ctd_analysis/tokens.tsv. Run `python3 scripts/export_tedim_analysis.py` "
        "before building the stem alternation corpus audit."
    )


def clean(text: str) -> str:
    return text.lower().strip("“”\"'.,;:!?()[]{}")


def split_chain(text: str) -> list[str]:
    return [part for part in clean(text).split("-") if part]


def alternation_type(form_i: str, form_ii: str) -> str:
    if form_ii == f"{form_i}h":
        return "+h"
    if form_ii == f"{form_i}k":
        return "+k"
    if form_ii == f"{form_i}t":
        return "+t"
    if form_i.endswith("ng") and form_ii == form_i[:-1]:
        return "-ng > -n"
    return "other / irregular / uncertain"


def load_candidate_statuses() -> tuple[
    dict[str, set[str]],
    dict[str, bool],
    dict[str, set[str]],
    dict[str, dict[str, set[str]]],
]:
    statuses: dict[str, set[str]] = defaultdict(set)
    present: dict[str, bool] = defaultdict(bool)
    references: dict[str, set[str]] = defaultdict(set)
    reference_statuses: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    if not CANDIDATES_PATH.exists():
        return statuses, present, references, reference_statuses

    with CANDIDATES_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            construction_id = row["construction_id"]
            pair_id = CANDIDATE_ALIASES.get(construction_id, construction_id)
            if "~" in pair_id:
                pair_id = pair_id.replace(" ~ ", "-").replace("~", "-")
            if pair_id in {"mu-muh", "ne-nek", "nei-neih", "pia-piak", "za-zak", "nusia-nusiat", "thei-theih", "piang-pian", "ngai-ngaih", "honkhia-honkhiat"}:
                present[pair_id] = True
                statuses[pair_id].add(row["candidate_status"])
                references[pair_id].add(row["reference"])
                reference_statuses[pair_id][row["reference"]].add(row["candidate_status"])
    return statuses, present, references, reference_statuses


def load_print_packet_text() -> str:
    text_parts = []
    for path in (GRAMMAR_PACKET_PATH, DICTIONARY_PACKET_PATH, REVIEW_NOTES_PATH):
        text_parts.append(path.read_text(encoding="utf-8") if path.exists() else "")
    return "\n".join(text_parts)


def load_review_bundle_text() -> str:
    text_parts = []
    for path in (DOSSIER_PATH, GRAMMAR_PACKET_PATH, DICTIONARY_PACKET_PATH, REVIEW_NOTES_PATH):
        text_parts.append(path.read_text(encoding="utf-8") if path.exists() else "")
    return "\n".join(text_parts)


def extract_exact_review_references(text: str) -> set[str]:
    references = set()
    with VERSES_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            reference = row["reference"]
            if re.search(rf"(?<![0-9A-Za-z]){re.escape(reference)}(?![0-9])", text):
                references.add(reference)
    return references


def build_pair_inventory() -> dict[str, PairMeta]:
    candidate_statuses, in_candidate, _, _ = load_candidate_statuses()
    print_packet_text = load_print_packet_text()

    pairs: dict[str, PairMeta] = {}

    for form_ii, (form_i, gloss) in sorted(VERB_STEM_PAIRS.items()):
        pair_id = f"{form_i}-{form_ii}"
        pair_phrase = f"`{form_i} ~ {form_ii}`"
        publication_status = MANUAL_PUBLICATION_STATUS.get(pair_id, "needs_analyzer_review")
        pairs[pair_id] = PairMeta(
            pair_id=pair_id,
            form_i=form_i,
            form_ii=form_ii,
            gloss=gloss,
            alternation_type=alternation_type(form_i, form_ii),
            analyzer_status="known_to_analyzer",
            used_in_print_packet=pair_phrase in print_packet_text,
            in_candidate_tsv=in_candidate.get(pair_id, False),
            candidate_statuses=tuple(sorted(candidate_statuses.get(pair_id, set()))),
            publication_status=publication_status,
            notes="",
        )

    for pair_id, (form_i, form_ii, gloss) in SUPPLEMENTAL_PACKET_PAIRS.items():
        if pair_id in pairs:
            continue
        pair_phrase = f"`{form_i} ~ {form_ii}`"
        pairs[pair_id] = PairMeta(
            pair_id=pair_id,
            form_i=form_i,
            form_ii=form_ii,
            gloss=gloss,
            alternation_type=alternation_type(form_i, form_ii),
            analyzer_status="packet_pair_not_in_VERB_STEM_PAIRS",
            used_in_print_packet=pair_phrase in print_packet_text,
            in_candidate_tsv=in_candidate.get(pair_id, False),
            candidate_statuses=tuple(sorted(candidate_statuses.get(pair_id, set()))),
            publication_status=MANUAL_PUBLICATION_STATUS.get(pair_id, "needs_analyzer_review"),
            notes="Present in the stem packet, but absent from VERB_STEM_PAIRS.",
        )

    return pairs


def load_verse_metadata() -> dict[str, dict[str, str]]:
    csv.field_size_limit(10**7)
    verses: dict[str, dict[str, str]] = {}
    with VERSES_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            verses[row["verse_id"]] = {
                "reference": row["reference"],
                "tedim": row["ctd_Tedim Chin"],
                "kjv": row["eng_King James Version"],
            }
    return verses


def iter_tokens_by_verse():
    csv.field_size_limit(10**7)
    with TOKENS_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        current_verse = None
        bucket: list[dict[str, str]] = []
        for row in reader:
            verse_id = row["verse_id"]
            if current_verse is None:
                current_verse = verse_id
            if verse_id != current_verse:
                yield current_verse, bucket
                current_verse = verse_id
                bucket = []
            bucket.append(row)
        if current_verse is not None:
            yield current_verse, bucket


def count_form_ii_hits(pairs: dict[str, PairMeta]) -> Counter:
    counts: Counter = Counter()
    form_ii_index = {meta.form_ii: meta.pair_id for meta in pairs.values()}
    for _, verse_tokens in iter_tokens_by_verse():
        for row in verse_tokens:
            normalized = clean(row["normalized_form"])
            stem = clean(row["stem_form"])
            seg_parts = split_chain(row["segmentation"])
            compact = "".join(seg_parts)
            for candidate in {normalized, stem, compact, *seg_parts}:
                pair_id = form_ii_index.get(candidate)
                if pair_id:
                    counts[pair_id] += 1
                    break
    return counts


def build_indexes(pairs: dict[str, PairMeta], form_ii_counts: Counter):
    form_i_index: dict[str, list[str]] = defaultdict(list)
    form_ii_index: dict[str, str] = {}
    for pair_id, meta in pairs.items():
        form_i_index[meta.form_i].append(pair_id)
        form_ii_index[meta.form_ii] = pair_id

    canonical_by_form_i: dict[str, str] = {}
    for form_i, pair_ids in form_i_index.items():
        if len(pair_ids) == 1:
            canonical_by_form_i[form_i] = pair_ids[0]
            continue
        canonical_by_form_i[form_i] = max(
            pair_ids,
            key=lambda pair_id: (
                form_ii_counts[pair_id],
                FORM_I_NOTE_PRIORITY.get(pair_id, 0),
                pair_id,
            ),
        )
    return form_i_index, form_ii_index, canonical_by_form_i


def pair_override_for_row(row: dict[str, str]) -> str | None:
    normalized = clean(row["normalized_form"])
    if normalized in NOISY_FORM_OVERRIDES:
        return NOISY_FORM_OVERRIDES[normalized]
    if normalized.startswith("ngaihs"):
        return "ngai-ngaih"
    if normalized.startswith("piangsak") or normalized.startswith("piangkhia"):
        return "piang-pian"
    if normalized.startswith("neihsak"):
        return "nei-neih"
    return None


def resolve_pair_id(
    row: dict[str, str],
    form_i_index: dict[str, list[str]],
    form_ii_index: dict[str, str],
    canonical_by_form_i: dict[str, str],
) -> tuple[str | None, str]:
    override = pair_override_for_row(row)
    if override:
        return override, "pair inferred from known noisy or derived family."

    normalized = clean(row["normalized_form"])
    stem = clean(row["stem_form"])
    lemma = clean(row["lemma"])
    seg_parts = split_chain(row["segmentation"])
    compact = "".join(seg_parts)

    for candidate in (stem, normalized, compact, *seg_parts):
        pair_id = form_ii_index.get(candidate)
        if pair_id:
            return pair_id, ""

    for candidate in (stem, normalized, lemma, compact, *seg_parts):
        pair_ids = form_i_index.get(candidate, [])
        if not pair_ids:
            continue
        if len(pair_ids) == 1:
            return pair_ids[0], ""
        canonical = canonical_by_form_i[candidate]
        others = sorted(pair_id for pair_id in pair_ids if pair_id != canonical)
        note = (
            f"Form I stem `{candidate}` participates in multiple analyzer pairs "
            f"({', '.join(pair_ids)}); counted under canonical pair {canonical}."
        )
        if others:
            note += f" Alternate Form II analyses remain visible in pair summary notes: {', '.join(others)}."
        return canonical, note

    return None, ""


def infer_attested_form(row: dict[str, str], pair: PairMeta) -> tuple[str, str, str]:
    normalized = clean(row["normalized_form"])
    stem = clean(row["stem_form"])
    seg_parts = split_chain(row["segmentation"])
    compact = "".join(seg_parts)
    suffix_parts = split_chain(row["suffix_chain"])
    export_alt = row["stem_alternation"].strip()

    if pair.form_ii in {normalized, stem, compact, *seg_parts}:
        return pair.form_ii, export_alt or "II", ""

    if pair.alternation_type in {"+h", "+k", "+t"} and stem == pair.form_i and suffix_parts:
        added = pair.form_ii[len(pair.form_i):]
        if suffix_parts[0] == added and normalized.startswith(pair.form_ii):
            return pair.form_ii, export_alt or "II", "stem alternation inferred from suffix chain."

    if pair.form_i in {normalized, stem, compact, *seg_parts}:
        return pair.form_i, export_alt or "I", ""

    if export_alt == "II":
        return pair.form_ii, "II", "stem alternation inferred from export metadata."
    if export_alt == "I":
        return pair.form_i, "I", "stem alternation inferred from export metadata."

    return normalized or stem, export_alt, "token belongs to the pair family but is not a simple Form I/II token."


def local_context(tokens: list[dict[str, str]], index: int, width: int = 3) -> str:
    start = max(0, index - width)
    end = min(len(tokens), index + width + 1)
    parts = []
    for offset, row in enumerate(tokens[start:end], start=start):
        token = row["surface_form"]
        if offset == index:
            parts.append(f"[{token}]")
        else:
            parts.append(token)
    return " ".join(parts)


def token_normalized(tokens: list[dict[str, str]], index: int) -> str:
    if 0 <= index < len(tokens):
        return clean(tokens[index]["normalized_form"])
    return ""


def token_pos(tokens: list[dict[str, str]], index: int) -> str:
    if 0 <= index < len(tokens):
        return tokens[index]["pos"]
    return ""


def infer_environment(
    tokens: list[dict[str, str]],
    index: int,
    pair: PairMeta,
    row: dict[str, str],
) -> tuple[str, str, str]:
    normalized = clean(row["normalized_form"])
    segmentation = row["segmentation"].lower()
    suffix_parts = split_chain(row["suffix_chain"])
    prev2 = token_normalized(tokens, index - 2)
    prev1 = token_normalized(tokens, index - 1)
    next1 = token_normalized(tokens, index + 1)
    next2 = token_normalized(tokens, index + 2)

    if normalized in {"ngaihsun", "ngaihsut", "ngaihsutna", "ngaihsutna-in"} or normalized.startswith("ngaihs"):
        return "compound_or_lexicalized", "high", "The dossier treats the `ngaihsun/ngaihsut` family as lexical-family contamination rather than clean `ngaih` evidence."

    if pair.pair_id in {"honkhia-honkhiat", "hu-huh"}:
        return "compound_or_lexicalized", "high", "This pair is currently treated as lexicalized or category-mixed rather than as simple stem evidence."

    if "sak" in suffix_parts or normalized.endswith("sak") or normalized.endswith("sakin") or "-sak" in segmentation:
        return "causative_or_derivational_sak", "high", "Causative or derivational `sak` blocks promotion as simple stem-alternation evidence."

    if next1 in {"ciangin", "ciang-in"}:
        return "dependent_temporal_ciangin", "high", "Immediate following `ciangin` provides a conservative dependent-temporal cue."

    if next1 in {"ni-in", "niin"} or (next1 == "ni" and next2 == "in"):
        return "dependent_temporal_ni_in", "high", "Immediate following `ni-in` provides a conservative dependent-temporal cue."

    if next1 == "kipan" or (next1 == "a" and next2 == "kipan"):
        return "clause_linking_kipan", "high", "Local `a kipan` sequence marks a clause-linking or source/beginning environment."

    if normalized in {"nadingin", "dinga", "dingin"} or next1 in {"nadingin", "dinga", "dingin"} or next2 == "nadingin":
        return "purpose_nadingin", "medium", "Local `ding` or `nadingin` material suggests a purpose or irrealis-heavy environment."

    if "na" in suffix_parts or segmentation.endswith("-na") or "-na-" in segmentation:
        return "nominalized_na", "high", "Suffixal `-na` in the analyzer segmentation supports a nominalized environment."

    if next1 == "mi" and token_pos(tokens, index - 1) in {"PROP", "PRON", "N"}:
        return "possessed_or_genitive_attributive", "medium", "A following `mi` plus a preceding possessor-like token suggests an attributive or possessed nominal environment."

    if next1 == "mi":
        return "relative_or_attributive_mi", "medium", "A following `mi` suggests a relative-like or attributive nominal environment."

    if any(token in {"lo", "loh", "kei"} for token in (prev2, prev1, next1, next2)):
        return "negative_clause", "medium", "Nearby negative material marks a negative or irrealis-heavy clause."

    if pair.pair_id == "thei-theih" and (next1 in {"ding", "lo", "mi"} or next2 in {"ding", "nadingin"}):
        return "modal_or_ability", "medium", "The `thei/theih` pair often surfaces in modal or ability-heavy contexts."

    if any(token in {"ci", "ci-in", "cih", "leh"} for token in (prev1, next1, next2)):
        return "quotative_or_say_complement", "low", "Nearby quotative material suggests embedded or reported-speech structure."

    if next1 in {"un", "in"}:
        return "imperative_or_directive", "low", "A following imperative-like particle may indicate directive force."

    if row["pos"] in {"V", "FUNC"} or next1 in {"hi", "uh", "ding"}:
        return "finite_main_or_matrix", "medium", "No stronger local cue was found, so the token is kept in a conservative finite or matrix bucket."

    return "unknown_or_needs_review", "low", "No conservative local environment rule fired for this token."

def recommendation_for_pair(
    pair: PairMeta,
    form_i_total: int,
    form_ii_total: int,
    dominant_form_ii_envs: list[str],
) -> str:
    if pair.publication_status in {"print_ready", "print_usable_with_caveat", "dossier_only", "exclude_for_now"}:
        if pair.publication_status == "dossier_only":
            return "interpretive_revision_of_slice"
        if pair.publication_status == "exclude_for_now":
            return "keep_excluded"
        return "interpretive_revision_of_slice"
    if pair.analyzer_status == "packet_pair_not_in_VERB_STEM_PAIRS":
        return "needs_analyzer_review"
    if form_ii_total == 0:
        return "needs_analyzer_review"
    if dominant_form_ii_envs and all(env in {"compound_or_lexicalized", "causative_or_derivational_sak"} for env in dominant_form_ii_envs):
        return "exclude_for_now"
    if form_i_total > 0 and form_ii_total > 0:
        return "candidate_for_expansion"
    return "needs_analyzer_review"


def join_top(counter: Counter, limit: int = 3) -> str:
    if not counter:
        return ""
    return "; ".join(f"{name}:{count}" for name, count in counter.most_common(limit))


def analysis_clarity_score(row: dict[str, str]) -> int:
    score = 0
    if row["segmentation"].strip() and row["segmentation"] not in {"?", "-"}:
        score += 1
    if row["lemma"].strip() and row["lemma"] not in {"?", "-"}:
        score += 1
    if row["pos"].strip() and row["pos"] not in {"UNK", "X", "?"}:
        score += 1
    if "inferred from export metadata" not in row["notes"] and "token belongs to the pair family" not in row["notes"]:
        score += 1
    return score


def selection_priority(
    row: dict[str, str],
    accepted_candidate_row_keys: set[tuple[str, str, str]],
    review_references: set[str],
    order_index: int,
) -> tuple[int, int, int, int, int]:
    row_key = (row["pair_id"], row["verse_id"], row["token_index"])
    return (
        1 if row["environment"] != "unknown_or_needs_review" else 0,
        analysis_clarity_score(row),
        2 if row_key in accepted_candidate_row_keys else 1 if row_key in MANUAL_REVIEW_ROW_ALLOWLIST or row["reference"] in review_references else 0,
        -len(row["local_context"].split()),
        -order_index,
    )


def build_selection_reason(
    row: dict[str, str],
    candidate_row_keys: set[tuple[str, str, str]],
    review_references: set[str],
) -> str:
    reasons = []
    row_key = (row["pair_id"], row["verse_id"], row["token_index"])
    if row_key in candidate_row_keys:
        reasons.append("preferred because this exact token is already part of an accepted candidate TSV row")
    elif row_key in MANUAL_REVIEW_ROW_ALLOWLIST:
        reasons.append("preferred because this exact row is manually retained as caveated evidence in the packet")
    elif row["reference"] in review_references:
        reasons.append("preferred because this verse is already cited in the dossier or packet")

    if row["environment"] == "unknown_or_needs_review":
        reasons.append("retained as the clearest available review-bucket example for this pair and stem side")
    else:
        reasons.append("kept as the clearest analyzed example for this pair, stem side, and environment")

    if analysis_clarity_score(row) >= 3:
        reasons.append("analyzer segmentation and POS are explicit enough for write-up use")

    return "; ".join(reasons)


def row_has_obvious_contamination(pair: PairMeta, row: dict[str, str]) -> tuple[bool, str]:
    normalized = clean(row["normalized_form"])
    surface = clean(row["surface_form"])
    segmentation = clean(row["segmentation"])
    if normalized in OBVIOUS_NOISY_ROW_FORMS or surface in OBVIOUS_NOISY_ROW_FORMS:
        return True, "Surface form belongs to a noisy lexicalized or compound family rather than to a clean print-safe stem token."
    if normalized.startswith("ngaihs") or normalized.startswith("piangsak") or normalized.startswith("piangkhia"):
        return True, "Surface form belongs to a derived or lexical-family cluster rather than to a clean stem alternation example."
    if pair.pair_id == "mu-muh" and ("muh-dah" in segmentation or "lui-mu" in segmentation):
        return True, "This `mu/muh` family row is lexicalized or compounded rather than a clean print-safe stem token."
    if "pair inferred from known noisy or derived family." in row["notes"]:
        return True, "Row was attached to the pair through a known noisy or derived-family override."
    if "token belongs to the pair family but is not a simple Form I/II token." in row["notes"]:
        return True, "Row belongs to the stem family, but not as a simple Form I or Form II token."
    return False, ""


def load_accepted_candidate_row_keys(pairs: dict[str, PairMeta]) -> set[tuple[str, str, str]]:
    accepted_keys: set[tuple[str, str, str]] = set()
    if not CANDIDATES_PATH.exists():
        return accepted_keys

    token_lookup: dict[tuple[str, str], dict[str, str]] = {}
    for _, verse_tokens in iter_tokens_by_verse():
        for token_row in verse_tokens:
            token_lookup[(token_row["verse_id"], token_row["token_index"])] = token_row

    with CANDIDATES_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            if row["candidate_status"] != "accepted":
                continue
            pair_id = CANDIDATE_ALIASES.get(row["construction_id"], row["construction_id"])
            if "~" in pair_id:
                pair_id = pair_id.replace(" ~ ", "-").replace("~", "-")
            pair = pairs.get(pair_id)
            if pair is None:
                continue
            for token_index in [part.strip() for part in row["token_indices"].split(",") if part.strip()]:
                token_row = token_lookup.get((row["verse_id"], token_index))
                if token_row is None:
                    continue
                attested_form, stem_alt, attested_note = infer_attested_form(token_row, pair)
                if stem_alt in {"I", "II"} and attested_form in {pair.form_i, pair.form_ii} and not attested_note:
                    accepted_keys.add((pair_id, row["verse_id"], token_index))
    return accepted_keys


def merge_notes(*parts: str) -> str:
    merged = []
    seen = set()
    for part in parts:
        text = part.strip()
        if not text or text in seen:
            continue
        seen.add(text)
        merged.append(text)
    return " ".join(merged)


def load_tsv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_questionnaire_inventory() -> dict[str, dict[str, str]]:
    inventory: dict[str, dict[str, str]] = {}
    for psc_label, (form_i, form_ii, gloss) in sorted(PSC_TO_TEDIM.items()):
        pair_id = f"{form_i}-{form_ii}"
        inventory[pair_id] = {
            "pair_id": pair_id,
            "psc_label": psc_label,
            "form_i": form_i,
            "form_ii": form_ii,
            "gloss": gloss,
        }
    return inventory


def exact_match_candidates(row: dict[str, str]) -> set[str]:
    segmentation_compact = "".join(split_chain(row.get("segmentation", "")))
    return {
        clean(row.get("normalized_form", "")),
        segmentation_compact,
    } - {""}


def row_matches_exact_form(row: dict[str, str], form: str) -> bool:
    return form in exact_match_candidates(row)


def is_clean_bare_stem_row(row: dict[str, str], form: str) -> bool:
    if clean(row.get("attested_form", "")) != form:
        return False
    if row.get("stem_alternation", "") not in {"I", "II"}:
        return False
    if row.get("inferred_environment", "") in {"causative_or_derivational_sak", "compound_or_lexicalized"}:
        return False
    notes = row.get("notes", "")
    if "pair inferred from known noisy or derived family." in notes:
        return False
    if "token belongs to the pair family but is not a simple Form I/II token." in notes:
        return False
    return row_matches_exact_form(row, form)


def inventory_row_priority(row: dict[str, str], form: str) -> tuple[int, int, int, int, str, int]:
    return (
        PRINT_STATUS_RANK.get(row.get("print_status", ""), 0),
        1 if is_clean_bare_stem_row(row, form) else 0,
        ENVIRONMENT_PRIORITY.get(row.get("inferred_environment", ""), -3),
        analysis_clarity_score(row),
        row.get("reference", ""),
        -int(row.get("token_index", "0") or 0),
    )


def format_inventory_example(row: dict[str, str]) -> str:
    form = row.get("surface_form") or row.get("attested_form") or row.get("normalized_form")
    environment = row.get("inferred_environment", "")
    status = row.get("print_status", "")
    return f"{row.get('reference', '')} `{form}` [{environment}; {status}]"


def choose_inventory_examples(
    rows: list[dict[str, str]],
    form: str,
    *,
    stem_alts: set[str] | None = None,
    environments: set[str] | None = None,
    row_filter=None,
    limit: int = 3,
) -> str:
    filtered = []
    for row in rows:
        if stem_alts and row.get("stem_alternation", "") not in stem_alts:
            continue
        if environments and row.get("inferred_environment", "") not in environments:
            continue
        if form and clean(row.get("attested_form", "")) not in {form, ""} and not row_matches_exact_form(row, form):
            continue
        if row_filter is not None and not row_filter(row):
            continue
        filtered.append(row)

    ordered = sorted(filtered, key=lambda item: inventory_row_priority(item, form), reverse=True)
    seen = set()
    chosen = []
    for row in ordered:
        key = (row.get("reference", ""), row.get("token_index", ""))
        if key in seen:
            continue
        seen.add(key)
        chosen.append(format_inventory_example(row))
        if len(chosen) >= limit:
            break
    return "; ".join(chosen)


def source_status(source_map: dict[str, str], pair_id: str) -> str:
    return source_map.get(pair_id, "no")


def pair_is_discussed_in_project_review(pair_id: str, form_i: str, form_ii: str) -> bool:
    pair_phrase = f"`{form_i} ~ {form_ii}`"
    for path in (DOSSIER_PATH, REVIEW_NOTES_PATH, DICTIONARY_PACKET_PATH):
        if path.exists() and pair_phrase in path.read_text(encoding="utf-8"):
            return True
    return False


def summarize_pos_counts(rows: list[dict[str, str]], limit: int = 3) -> str:
    counts = Counter(row.get("pos", "") for row in rows)
    return ", ".join(f"{pos}:{count}" for pos, count in counts.most_common(limit) if pos)


def infer_lexical_category(
    pair_id: str,
    form_i: str,
    form_ii: str,
    pair_rows: list[dict[str, str]],
    questionnaire_entry: dict[str, str] | None,
    pair: PairMeta | None,
) -> str:
    if pair_id in LEXICAL_CATEGORY_OVERRIDES:
        return LEXICAL_CATEGORY_OVERRIDES[pair_id]
    if questionnaire_entry is not None and form_i == form_ii and pair is None:
        return "same_form_questionnaire_control"
    pos_counts = Counter(row.get("pos", "") for row in pair_rows)
    nominalish = pos_counts["N"] + pos_counts["DET"] + pos_counts["PROP"]
    verbalish = pos_counts["V"] + pos_counts["FUNC"] + pos_counts["ADJ"]
    if nominalish > max(verbalish * 2, 20):
        return "noun_or_nominal_compound"
    if pos_counts["ADJ"] > max(pos_counts["V"] * 2, 50):
        return "stative_or_adjectival_predicate"
    if pair is not None and pair.gloss in {"be", "say", "exist"}:
        return "auxiliary_or_functional_verb"
    if pair is not None and pair.analyzer_status == "known_to_analyzer":
        return "lexical_verb"
    return "analyzer_only_uncertain"


def is_clean_verbal_row(
    row: dict[str, str],
    form: str,
    pair_id: str,
    lexical_category: str,
) -> bool:
    if not is_clean_bare_stem_row(row, form):
        return False
    if row.get("inferred_environment", "") not in VERBAL_ENVIRONMENTS:
        return False
    pos = row.get("pos", "")
    if pos == "V":
        return True
    if lexical_category == "auxiliary_or_functional_verb" and pos == "FUNC":
        return True
    if pos in ALLOWED_PREDICATIVE_NONV_POS.get(pair_id, set()):
        return True
    return False


def infer_category_evidence(
    pair_rows: list[dict[str, str]],
    lexical_category: str,
    clean_verb_form_i_count: int,
    clean_verb_form_ii_count: int,
) -> str:
    pos_summary = summarize_pos_counts(pair_rows)
    note = f"POS profile {pos_summary or 'none'}; clean verbal exact rows I={clean_verb_form_i_count}, II={clean_verb_form_ii_count}."
    if lexical_category == "noun_or_nominal_compound":
        note += " Current Bible hits are predominantly nominal, locative, or compound-like rather than verbal."
    elif lexical_category == "same_form_questionnaire_control":
        note += " Bible hits confirm the questionnaire control form, but not an overt written alternation."
    elif lexical_category == "auxiliary_or_functional_verb":
        note += " The pair behaves mainly as copular, quotative, existential, or otherwise functional material."
    elif lexical_category == "stative_or_adjectival_predicate":
        note += " The surviving evidence looks chiefly predicative or adjectival rather than like a lexical action verb."
    elif lexical_category == "lexicalized_or_category_mixed":
        note += " The family mixes lexicalized, derivational, or category-shifting material."
        if clean_verb_form_i_count > 0 or clean_verb_form_ii_count > 0:
            note += " Clean exact verbal rows still survive apart from the blocked family material."
    elif lexical_category == "analyzer_only_uncertain":
        note += " The analyzer proposes the pair, but the Bible evidence still needs philological review."
    elif clean_verb_form_i_count > 0 or clean_verb_form_ii_count > 0:
        note += " Exact verbal evidence survives after lexical-category filtering."
    return note


def infer_promotion_status_with_overrides(
    pair_id: str,
    lexical_category: str,
    clean_verb_form_i_count: int,
    clean_verb_form_ii_count: int,
    overrides: dict[str, str],
) -> str:
    if pair_id in overrides:
        return overrides[pair_id]
    if lexical_category == "same_form_questionnaire_control":
        return "mention_as_questionnaire_control"
    if lexical_category == "noun_or_nominal_compound":
        return "block_from_verb_inventory_pending_review"
    if lexical_category in {"lexicalized_or_category_mixed", "analyzer_only_uncertain"}:
        return "mention_in_inventory_only"
    if lexical_category in {"auxiliary_or_functional_verb", "stative_or_adjectival_predicate"}:
        return "mention_in_inventory_only"
    if clean_verb_form_i_count > 0 and clean_verb_form_ii_count > 0:
        return "promote_with_caveat"
    if clean_verb_form_i_count > 0 or clean_verb_form_ii_count > 0:
        return "mention_in_inventory_only"
    return "block_from_verb_inventory_pending_review"


def infer_promotion_status(
    pair_id: str,
    lexical_category: str,
    clean_verb_form_i_count: int,
    clean_verb_form_ii_count: int,
) -> str:
    return infer_promotion_status_with_overrides(
        pair_id,
        lexical_category,
        clean_verb_form_i_count,
        clean_verb_form_ii_count,
        PROMOTION_STATUS_OVERRIDES,
    )


def infer_baseline_promotion_status(
    pair_id: str,
    lexical_category: str,
    clean_verb_form_i_count: int,
    clean_verb_form_ii_count: int,
) -> str:
    return infer_promotion_status_with_overrides(
        pair_id,
        lexical_category,
        clean_verb_form_i_count,
        clean_verb_form_ii_count,
        BASELINE_PROMOTION_STATUS_OVERRIDES,
    )


def infer_promotion_blocker(
    pair_id: str,
    lexical_category: str,
    clean_verb_form_i_count: int,
    clean_verb_form_ii_count: int,
) -> str:
    if pair_id in PROMOTION_BLOCKER_OVERRIDES:
        return PROMOTION_BLOCKER_OVERRIDES[pair_id]
    if lexical_category == "same_form_questionnaire_control":
        return "same_written_form_no_overt_alternation"
    if lexical_category == "noun_or_nominal_compound":
        return "nominal_or_compound_examples_only"
    if lexical_category == "lexicalized_or_category_mixed":
        return "lexicalized_family_contamination"
    if lexical_category in {"auxiliary_or_functional_verb", "stative_or_adjectival_predicate"}:
        return "category_mismatch"
    if clean_verb_form_i_count == 0:
        return "no_clean_form_i_verb_example"
    if clean_verb_form_ii_count == 0:
        return "no_clean_form_ii_verb_example"
    return "needs_manual_philological_review"


def promotable_example_priority(
    row: dict[str, str],
    *,
    form: str,
    pair_id: str,
    lexical_category: str,
) -> tuple[int, int, int, int, str, int]:
    return (
        2 if is_clean_verbal_row(row, form, pair_id, lexical_category) else 1 if is_clean_bare_stem_row(row, form) else 0,
        PRINT_STATUS_RANK.get(row.get("print_status", ""), 0),
        ENVIRONMENT_PRIORITY.get(row.get("inferred_environment", ""), -3),
        analysis_clarity_score(row),
        row.get("reference", ""),
        -int(row.get("token_index", "0") or 0),
    )


def choose_promotable_example_row(
    rows: list[dict[str, str]],
    *,
    form: str,
    stem_alt: str,
    pair_id: str,
    lexical_category: str,
) -> dict[str, str] | None:
    filtered = [row for row in rows if row.get("stem_alternation", "") == stem_alt and (clean(row.get("attested_form", "")) == form or row_matches_exact_form(row, form))]
    if not filtered:
        return None
    ordered = sorted(
        filtered,
        key=lambda item: promotable_example_priority(
            item,
            form=form,
            pair_id=pair_id,
            lexical_category=lexical_category,
        ),
        reverse=True,
    )
    return ordered[0]


def example_quality_for_row(
    row: dict[str, str],
    *,
    form: str,
    pair_id: str,
    lexical_category: str,
    promotion_status: str,
) -> str:
    if promotion_status == "mention_as_questionnaire_control":
        return "questionnaire_control"
    if lexical_category == "noun_or_nominal_compound":
        return "blocked_nonverbal"
    if row.get("inferred_environment", "") in {"causative_or_derivational_sak", "compound_or_lexicalized"}:
        return "blocked_noise"
    if lexical_category == "lexicalized_or_category_mixed":
        return "needs_manual_review" if is_clean_verbal_row(row, form, pair_id, lexical_category) else "blocked_noise"
    if row.get("print_status", "") in {"print_ready", "print_usable_with_caveat"}:
        return row["print_status"]
    if is_clean_verbal_row(row, form, pair_id, lexical_category):
        if promotion_status == "promote_to_main_grammar":
            return "descriptive_clean"
        return "descriptive_with_caveat"
    if is_clean_bare_stem_row(row, form):
        return "descriptive_with_caveat"
    return "needs_manual_review"


def scan_questionnaire_only_rows(
    entries: dict[str, dict[str, str]],
    verses: dict[str, dict[str, str]],
) -> dict[str, list[dict[str, str]]]:
    if not entries:
        return {}

    form_index: dict[str, list[tuple[str, str]]] = defaultdict(list)
    pseudo_pairs: dict[str, PairMeta] = {}
    for pair_id, entry in entries.items():
        pseudo_pairs[pair_id] = PairMeta(
            pair_id=pair_id,
            form_i=entry["form_i"],
            form_ii=entry["form_ii"],
            gloss=entry["gloss"],
            alternation_type=alternation_type(entry["form_i"], entry["form_ii"]),
            analyzer_status="questionnaire_only",
            used_in_print_packet=False,
            in_candidate_tsv=False,
            candidate_statuses=(),
            publication_status="needs_analyzer_review",
            notes="Questionnaire-only exact-form scan; not part of the analyzer pair inventory.",
        )
        form_index[entry["form_i"]].append((pair_id, "I"))
        if entry["form_ii"] != entry["form_i"]:
            form_index[entry["form_ii"]].append((pair_id, "II"))

    rows_by_pair: dict[str, list[dict[str, str]]] = defaultdict(list)
    for verse_id, verse_tokens in iter_tokens_by_verse():
        verse_meta = verses.get(verse_id)
        if verse_meta is None:
            continue

        for index, row in enumerate(verse_tokens):
            candidates = exact_match_candidates(row)
            if not candidates:
                continue

            hits: dict[str, str] = {}
            for candidate in candidates:
                for pair_id, stem_alt in form_index.get(candidate, []):
                    if stem_alt == "II" or pair_id not in hits:
                        hits[pair_id] = stem_alt

            for pair_id, stem_alt in hits.items():
                pair = pseudo_pairs[pair_id]
                environment, env_confidence, env_note = infer_environment(verse_tokens, index, pair, row)
                print_status = "exclude_for_now" if environment in {"causative_or_derivational_sak", "compound_or_lexicalized"} else "needs_analyzer_review"
                rows_by_pair[pair_id].append(
                    {
                        "pair_id": pair_id,
                        "form_i": pair.form_i,
                        "form_ii": pair.form_ii,
                        "attested_form": pair.form_i if stem_alt == "I" else pair.form_ii,
                        "stem_form": row["stem_form"],
                        "verse_id": verse_id,
                        "reference": verse_meta["reference"],
                        "token_index": row["token_index"],
                        "surface_form": row["surface_form"],
                        "normalized_form": row["normalized_form"],
                        "segmentation": row["segmentation"],
                        "gloss": row["gloss"],
                        "lemma": row["lemma"],
                        "pos": row["pos"],
                        "stem_alternation": stem_alt,
                        "prefix_chain": row["prefix_chain"],
                        "suffix_chain": row["suffix_chain"],
                        "usage_type": row["usage_type"],
                        "function_type": row["function_type"],
                        "local_context": local_context(verse_tokens, index),
                        "kjv": verse_meta["kjv"],
                        "inferred_environment": environment,
                        "environment_confidence": env_confidence,
                        "print_status": print_status,
                        "notes": merge_notes(
                            pair.notes,
                            env_note,
                            "Questionnaire maps the same surface form to both slots." if pair.form_i == pair.form_ii else "",
                        ),
                    }
                )
    return rows_by_pair


def source_notes_for_inventory_entry(
    pair_id: str,
    form_i: str,
    form_ii: str,
    questionnaire_entry: dict[str, str] | None,
    pair: PairMeta | None,
    form_i_index: dict[str, list[str]],
) -> str:
    notes = []
    if questionnaire_entry is not None:
        notes.append(
            "Questionnaire evidence comes from the in-repo Zakaria/VSA materials; no separate Karius/Kariuss/Karias questionnaire file is present."
        )
        notes.append(f"{questionnaire_entry['psc_label']} -> {form_i}/{form_ii}.")
        if form_i == form_ii:
            notes.append("The questionnaire uses the same written form in both slots.")
        sibling_pairs = sorted(other for other in form_i_index.get(form_i, []) if other != pair_id)
        if sibling_pairs:
            notes.append(f"Analyzer inventory also maps the same Form I base to {', '.join(sibling_pairs)}.")
    if pair is not None and pair.analyzer_status == "packet_pair_not_in_VERB_STEM_PAIRS":
        notes.append("Present in the publication-review packet, but absent from VERB_STEM_PAIRS.")
    if source_status(HENDERSON_SOURCE_STATUS, pair_id) == "yes":
        notes.append("`source_henderson=yes` means the in-repo literature review aligns this pair directly to Henderson; it does not claim an exhaustive extracted Henderson pair list.")
    if source_status(HENDERSON_SOURCE_STATUS, pair_id) == "unverified":
        notes.append("Henderson is only indirectly aligned to this pair in current project materials, not through a direct in-repo Tedim pair list.")
    if source_status(ZAM_SOURCE_STATUS, pair_id) == "yes":
        notes.append("`source_zam_ngaih_cing=yes` means the in-repo literature review aligns this pair directly to Zam Ngaih Cing; it does not claim an exhaustive extracted Stem 1/2 list.")
    if source_status(ZAM_SOURCE_STATUS, pair_id) == "unverified":
        notes.append("Zam Ngaih Cing is only indirectly aligned to this pair in current project materials, not through a direct in-repo pair list.")
    if pair_is_discussed_in_project_review(pair_id, form_i, form_ii):
        notes.append("This pair is discussed in current project review materials.")
    if questionnaire_entry is not None and pair is not None and questionnaire_entry["gloss"] != pair.gloss:
        notes.append(f"Questionnaire gloss `{questionnaire_entry['gloss']}` and analyzer gloss `{pair.gloss}` differ.")
    return merge_notes(*notes)


def format_manual_review_example(row: dict[str, str] | None) -> str:
    if row is None:
        return ""
    form = row.get("normalized_form") or row.get("surface_form", "")
    environment = row.get("inferred_environment", "")
    pos = row.get("pos", "")
    return f"{row.get('reference', '')} `{form}` [{environment}; {pos}]"


def summarize_environment_distribution(rows: list[dict[str, str]], form_i: str, form_ii: str) -> str:
    counter = Counter()
    for row in rows:
        if row_matches_exact_form(row, form_i) or row_matches_exact_form(row, form_ii):
            counter[row.get("inferred_environment", "")] += 1
    return "; ".join(f"{environment}:{count}" for environment, count in counter.most_common(6) if environment)


def default_manual_review_decision(
    lexical_category: str,
    recommended_status: str,
) -> str:
    if recommended_status == "promote_to_main_grammar":
        return "promote_now"
    if recommended_status == "promote_with_caveat":
        return "promote_with_caveat_now"
    if recommended_status == "discuss_as_difficult_case":
        return "retain_as_difficult_case"
    if lexical_category == "same_form_questionnaire_control":
        return "retain_questionnaire_control"
    if lexical_category == "noun_or_nominal_compound":
        return "block_nonverbal"
    if lexical_category == "lexicalized_or_category_mixed":
        return "retain_as_difficult_case"
    if lexical_category == "analyzer_only_uncertain":
        return "needs_more_manual_review"
    if recommended_status == "block_from_verb_inventory_pending_review":
        return "block_noise"
    return "retain_inventory_only"


def default_grammar_location(
    lexical_category: str,
    recommended_status: str,
) -> str:
    if recommended_status == "promote_to_main_grammar":
        return "main_promoted_verbal_inventory"
    if recommended_status == "promote_with_caveat":
        return "caveated_promoted_verbal_inventory"
    if lexical_category == "same_form_questionnaire_control":
        return "same_form_questionnaire_controls"
    if lexical_category == "auxiliary_or_functional_verb":
        return "functional_predicates"
    if lexical_category == "stative_or_adjectival_predicate":
        return "stative_predicates"
    if lexical_category == "noun_or_nominal_compound":
        return "blocked_nonverbal_appendix"
    if lexical_category == "analyzer_only_uncertain":
        return "analyzer_only_uncertain"
    return "difficult_cases"


def default_manual_review_rationale(
    pair_id: str,
    lexical_category: str,
    manual_review_decision: str,
    main_obstacle: str,
) -> str:
    if manual_review_decision == "promote_now":
        return "Manual review confirms that the pair is still a stable promoted showcase verb."
    if manual_review_decision == "promote_with_caveat_now":
        return f"Both forms have enough lexical evidence for grammar discussion, but {main_obstacle.lower()}."
    if manual_review_decision == "retain_as_difficult_case":
        return f"The pair stays visible because it is grammatically important, but {main_obstacle.lower()}."
    if manual_review_decision == "retain_questionnaire_control":
        return "The row remains a same-form questionnaire control rather than a promoted alternating pair."
    if manual_review_decision == "block_nonverbal":
        return "Current Bible hits are non-verbal enough that the pair should stay out of the promoted verb discussion."
    if manual_review_decision == "block_noise":
        return "Current evidence is too noisy or too weakly verbal for promotion."
    if lexical_category == "analyzer_only_uncertain":
        return "The analyzer suggests the pair, but the current Bible evidence still needs manual philological review."
    return f"Keep the row in the broader inventory for now because {main_obstacle.lower()}."


def default_next_manual_check(
    manual_review_decision: str,
    recommended_status: str,
) -> str:
    if recommended_status in {"promote_to_main_grammar", "promote_with_caveat"}:
        return "Keep choosing exact citation rows that match the promoted grammar discussion."
    if manual_review_decision in {"retain_as_difficult_case", "needs_more_manual_review"}:
        return "Revisit only with a narrower philological pass on exact token families."
    if manual_review_decision in {"block_nonverbal", "block_noise"}:
        return "Leave blocked unless new exact verbal evidence is found."
    return "Retain in the wider inventory until cleaner evidence appears."


def infer_bible_attestation_profile(
    form_i_attested: bool,
    form_ii_attested: bool,
    form_i_clean: int,
    form_ii_clean: int,
    rows: list[dict[str, str]],
) -> str:
    environments = {row.get("inferred_environment", "") for row in rows}
    if not form_i_attested and not form_ii_attested:
        return "not_attested_in_bible"
    if form_i_attested and form_ii_attested:
        if form_i_clean > 0 and form_ii_clean > 0:
            return "both_forms_cleanly_attested"
        if environments <= {"causative_or_derivational_sak", "compound_or_lexicalized"}:
            return "only_noisy_or_lexicalized_attested"
        if environments & {
            "nominalized_na",
            "dependent_temporal_ciangin",
            "dependent_temporal_ni_in",
            "clause_linking_kipan",
            "purpose_nadingin",
            "relative_or_attributive_mi",
            "possessed_or_genitive_attributive",
            "modal_or_ability",
        }:
            return "both_forms_attested_but_complex"
        return "both_forms_attested_but_complex"
    if form_i_attested:
        if form_i_clean > 0:
            return "form_i_only_attested"
        if environments & {"nominalized_na", "purpose_nadingin", "relative_or_attributive_mi", "possessed_or_genitive_attributive"}:
            return "only_derived_or_nominalized_attested"
        return "only_noisy_or_lexicalized_attested"
    if form_ii_clean > 0:
        return "form_ii_only_attested"
    if environments & {
        "nominalized_na",
        "dependent_temporal_ciangin",
        "dependent_temporal_ni_in",
        "clause_linking_kipan",
        "purpose_nadingin",
        "relative_or_attributive_mi",
        "possessed_or_genitive_attributive",
        "modal_or_ability",
    }:
        return "only_derived_or_nominalized_attested"
    return "only_noisy_or_lexicalized_attested"


def infer_lexical_pair_status(
    pair_id: str,
    *,
    source_secondary: bool,
    source_vsa: bool,
    source_analyzer: bool,
    form_i_attested: bool,
    form_ii_attested: bool,
    bible_profile: str,
    form_i: str,
    form_ii: str,
) -> str:
    if pair_id in LEXICAL_PAIR_STATUS_OVERRIDES:
        return LEXICAL_PAIR_STATUS_OVERRIDES[pair_id]
    if bible_profile == "only_noisy_or_lexicalized_attested":
        return "homophone_or_noise_only"
    if form_i == form_ii and source_vsa:
        return "questionnaire_pair_bible_one_sided" if (form_i_attested or form_ii_attested) else "analyzer_pair_needs_review"
    if source_vsa and form_i_attested != form_ii_attested:
        return "questionnaire_pair_bible_one_sided"
    if source_secondary and form_i_attested != form_ii_attested:
        return "literature_pair_bible_one_sided"
    if source_secondary or source_vsa:
        if bible_profile in {"both_forms_cleanly_attested", "both_forms_attested_but_complex"}:
            return "established_pair"
        return "likely_pair"
    if source_analyzer and bible_profile in {"both_forms_cleanly_attested", "both_forms_attested_but_complex"}:
        return "likely_pair"
    if source_analyzer:
        return "analyzer_pair_needs_review"
    return "likely_pair"


def infer_grammar_treatment(
    pair_id: str,
    *,
    lexical_category: str,
    lexical_pair_status: str,
    bible_profile: str,
    source_secondary: bool,
    source_vsa: bool,
    rows: list[dict[str, str]],
) -> str:
    if pair_id in GRAMMAR_TREATMENT_OVERRIDES:
        return GRAMMAR_TREATMENT_OVERRIDES[pair_id]
    if lexical_category == "same_form_questionnaire_control":
        return "mention_as_literature_or_questionnaire_only"
    if lexical_category in {"noun_or_nominal_compound", "auxiliary_or_functional_verb", "stative_or_adjectival_predicate"}:
        return "discuss_under_lexicalized_or_excluded_forms"
    if lexical_pair_status in {"lexicalized_or_category_mixed", "homophone_or_noise_only"} or bible_profile == "only_noisy_or_lexicalized_attested":
        return "discuss_under_lexicalized_or_excluded_forms"
    if bible_profile == "not_attested_in_bible":
        return "mention_as_literature_or_questionnaire_only" if (source_secondary or source_vsa) else "omit_pending_evidence"
    if bible_profile in {"form_i_only_attested", "form_ii_only_attested"}:
        return "mention_as_literature_or_questionnaire_only" if (source_secondary or source_vsa) else "omit_pending_evidence"
    if any(row.get("inferred_environment", "") == "modal_or_ability" for row in rows):
        return "discuss_under_modal_or_constructional_complexity"
    if any(
        row.get("inferred_environment", "") in {
            "nominalized_na",
            "dependent_temporal_ciangin",
            "dependent_temporal_ni_in",
            "clause_linking_kipan",
            "purpose_nadingin",
            "relative_or_attributive_mi",
            "possessed_or_genitive_attributive",
        }
        for row in rows
    ):
        return "discuss_under_nominalization_or_dependent_clauses"
    return "ordinary_inventory_entry"


def best_available_print_status(pair: PairMeta | None, rows: list[dict[str, str]]) -> str:
    if pair is not None:
        return pair.publication_status
    best = "needs_analyzer_review"
    for row in rows:
        if PRINT_STATUS_RANK.get(row.get("print_status", ""), 0) > PRINT_STATUS_RANK.get(best, 0):
            best = row["print_status"]
    return best


def homophone_or_noise_notes(
    pair_id: str,
    rows: list[dict[str, str]],
    questionnaire_entry: dict[str, str] | None,
    pair: PairMeta | None,
) -> str:
    notes = []
    if pair_id == "ngai-ngaih":
        notes.append("`ngaihsun/ngaihsut/ngaihsutna` remain lexical-family contamination unless a row can be justified independently.")
    if pair_id == "piang-pian":
        notes.append("`piangsak` and related derived rows must not be counted as clean bare Form II evidence.")
    if pair_id in {"honkhia-honkhiat", "hu-huh"}:
        notes.append("Current evidence behaves as lexicalized or category-mixed rather than as a clean pedagogical stem pair.")
    if questionnaire_entry is not None and questionnaire_entry["form_i"] == questionnaire_entry["form_ii"]:
        notes.append("Questionnaire uses a same-form mapping, so Bible tokens do not independently prove a distinct written Form II.")
    blocked_forms = Counter(
        clean(row.get("normalized_form", ""))
        for row in rows
        if row.get("inferred_environment", "") in {"causative_or_derivational_sak", "compound_or_lexicalized"}
    )
    if blocked_forms:
        notes.append(f"Blocked noisy material includes {', '.join(name for name, _ in blocked_forms.most_common(4))}.")
    if pair is not None and pair.form_i == "pua" and pair.form_ii == "puak":
        notes.append("Questionnaire glosses this base as 'carry.on.back', while the analyzer gloss is 'spill'.")
    return merge_notes(*notes)


def write_lexical_inventory(
    pairs: dict[str, PairMeta],
    form_i_index: dict[str, list[str]],
    verses: dict[str, dict[str, str]],
) -> None:
    questionnaire_inventory = load_questionnaire_inventory()
    audit_rows = load_tsv_rows(CORPUS_AUDIT_PATH)
    rows_by_pair: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in audit_rows:
        rows_by_pair[row["pair_id"]].append(row)

    questionnaire_only = {
        pair_id: entry
        for pair_id, entry in questionnaire_inventory.items()
        if pair_id not in pairs
    }
    for pair_id, extra_rows in scan_questionnaire_only_rows(questionnaire_only, verses).items():
        rows_by_pair[pair_id].extend(extra_rows)

    inventory_rows = []
    promotable_rows = []
    manual_review_rows = []
    all_pair_ids = sorted(set(pairs) | set(questionnaire_inventory))
    for pair_id in all_pair_ids:
        pair = pairs.get(pair_id)
        questionnaire_entry = questionnaire_inventory.get(pair_id)
        form_i = pair.form_i if pair is not None else questionnaire_entry["form_i"]
        form_ii = pair.form_ii if pair is not None else questionnaire_entry["form_ii"]
        gloss_parts = []
        if pair is not None and pair.gloss:
            gloss_parts.append(pair.gloss)
        if questionnaire_entry is not None and questionnaire_entry["gloss"] and questionnaire_entry["gloss"] not in gloss_parts:
            gloss_parts.append(questionnaire_entry["gloss"])
        gloss = " / ".join(gloss_parts)

        pair_rows = rows_by_pair.get(pair_id, [])
        form_i_rows = [row for row in pair_rows if row.get("stem_alternation", "") == "I"]
        form_ii_rows = [row for row in pair_rows if row.get("stem_alternation", "") == "II"]
        lexical_category = infer_lexical_category(pair_id, form_i, form_ii, pair_rows, questionnaire_entry, pair)
        form_i_clean = sum(1 for row in form_i_rows if is_clean_bare_stem_row(row, form_i))
        form_ii_clean = sum(1 for row in form_ii_rows if is_clean_bare_stem_row(row, form_ii))
        clean_verb_form_i_count = sum(1 for row in form_i_rows if is_clean_verbal_row(row, form_i, pair_id, lexical_category))
        clean_verb_form_ii_count = sum(1 for row in form_ii_rows if is_clean_verbal_row(row, form_ii, pair_id, lexical_category))
        form_i_family = len(form_i_rows)
        form_ii_family = len(form_ii_rows)
        form_i_attested = form_i_family > 0
        form_ii_attested = form_ii_family > 0 and not (questionnaire_entry is not None and form_i == form_ii and pair is None)

        bible_profile = infer_bible_attestation_profile(
            form_i_attested,
            form_ii_attested,
            form_i_clean,
            form_ii_clean,
            pair_rows,
        )
        source_henderson = source_status(HENDERSON_SOURCE_STATUS, pair_id)
        source_zam = source_status(ZAM_SOURCE_STATUS, pair_id)
        source_secondary = source_henderson == "yes" or source_zam == "yes"
        source_vsa = questionnaire_entry is not None
        source_analyzer = pair is not None and pair.analyzer_status == "known_to_analyzer"
        source_bible = bool(pair_rows)
        source_project_review = pair_is_discussed_in_project_review(pair_id, form_i, form_ii)
        lexical_status = infer_lexical_pair_status(
            pair_id,
            source_secondary=source_secondary,
            source_vsa=source_vsa,
            source_analyzer=source_analyzer,
            form_i_attested=form_i_attested,
            form_ii_attested=form_ii_attested,
            bible_profile=bible_profile,
            form_i=form_i,
            form_ii=form_ii,
        )
        grammar_treatment = infer_grammar_treatment(
            pair_id,
            lexical_category=lexical_category,
            lexical_pair_status=lexical_status,
            bible_profile=bible_profile,
            source_secondary=source_secondary,
            source_vsa=source_vsa,
            rows=pair_rows,
        )
        print_status = best_available_print_status(pair, pair_rows)
        category_evidence = infer_category_evidence(
            pair_rows,
            lexical_category,
            clean_verb_form_i_count,
            clean_verb_form_ii_count,
        )
        promotion_status = infer_promotion_status(
            pair_id,
            lexical_category,
            clean_verb_form_i_count,
            clean_verb_form_ii_count,
        )
        baseline_promotion_status = infer_baseline_promotion_status(
            pair_id,
            lexical_category,
            clean_verb_form_i_count,
            clean_verb_form_ii_count,
        )
        promotion_blocker = infer_promotion_blocker(
            pair_id,
            lexical_category,
            clean_verb_form_i_count,
            clean_verb_form_ii_count,
        )
        notes = []
        siblings = sorted(other for other in form_i_index.get(form_i, []) if other != pair_id)
        if siblings:
            notes.append(f"Shared Form I base with {', '.join(siblings)}.")
        if source_vsa and questionnaire_entry is not None and questionnaire_entry["form_i"] == questionnaire_entry["form_ii"] and pair is None:
            notes.append("Questionnaire keeps the same written form in both slots, so this row is treated as Form I only for Bible-attestation purposes.")
        if bible_profile == "both_forms_attested_but_complex":
            notes.append("Both forms are attested, but at least one side is clearest in dependent, nominalized, or otherwise non-bare environments.")
        if bible_profile in {"form_i_only_attested", "form_ii_only_attested"}:
            notes.append("Only one stem side is currently attested cleanly in the Bible corpus.")
        if bible_profile == "only_noisy_or_lexicalized_attested":
            notes.append("Current Bible evidence is limited to noisy, lexicalized, or heavily derived material.")

        inventory_rows.append(
            {
                "lexeme_id": pair_id,
                "form_i": form_i,
                "form_ii": form_ii,
                "gloss": gloss,
                "alternation_type": alternation_type(form_i, form_ii),
                "source_henderson": source_henderson,
                "source_zam_ngaih_cing": source_zam,
                "source_vsa_questionnaire": "yes" if source_vsa else "no",
                "source_analyzer_inventory": "yes" if source_analyzer else "no",
                "source_bible_audit": "yes" if source_bible else "no",
                "source_project_review": "yes" if source_project_review else "no",
                "source_notes": source_notes_for_inventory_entry(pair_id, form_i, form_ii, questionnaire_entry, pair, form_i_index),
                "lexical_category": lexical_category,
                "category_evidence": category_evidence,
                "form_i_bible_attested": "yes" if form_i_attested else "no",
                "form_ii_bible_attested": "yes" if form_ii_attested else "no",
                "form_i_clean_token_count": str(form_i_clean),
                "form_ii_clean_token_count": str(form_ii_clean),
                "form_i_family_count": str(form_i_family),
                "form_ii_family_count": str(form_ii_family),
                "clean_verb_form_i_count": str(clean_verb_form_i_count),
                "clean_verb_form_ii_count": str(clean_verb_form_ii_count),
                "best_form_i_examples": choose_inventory_examples(pair_rows, form_i, stem_alts={"I"}),
                "best_form_ii_examples": choose_inventory_examples(pair_rows, form_ii, stem_alts={"II"}),
                "best_clean_verb_form_i_examples": choose_inventory_examples(
                    pair_rows,
                    form_i,
                    stem_alts={"I"},
                    row_filter=lambda row, pair_id=pair_id, lexical_category=lexical_category, form=form_i: is_clean_verbal_row(row, form, pair_id, lexical_category),
                ),
                "best_clean_verb_form_ii_examples": choose_inventory_examples(
                    pair_rows,
                    form_ii,
                    stem_alts={"II"},
                    row_filter=lambda row, pair_id=pair_id, lexical_category=lexical_category, form=form_ii: is_clean_verbal_row(row, form, pair_id, lexical_category),
                ),
                "nominalized_examples": choose_inventory_examples(pair_rows, "", environments={"nominalized_na"}, limit=2),
                "dependent_temporal_examples": choose_inventory_examples(pair_rows, "", environments={"dependent_temporal_ciangin", "dependent_temporal_ni_in", "clause_linking_kipan"}, limit=2),
                "purpose_examples": choose_inventory_examples(pair_rows, "", environments={"purpose_nadingin"}, limit=2),
                "relative_or_attributive_examples": choose_inventory_examples(pair_rows, "", environments={"relative_or_attributive_mi", "possessed_or_genitive_attributive"}, limit=2),
                "negative_examples": choose_inventory_examples(pair_rows, "", environments={"negative_clause"}, limit=2),
                "finite_predicate_examples": choose_inventory_examples(pair_rows, "", environments={"finite_main_or_matrix", "imperative_or_directive"}, limit=2),
                "derived_or_causative_examples": choose_inventory_examples(pair_rows, "", environments={"causative_or_derivational_sak"}, limit=2),
                "compound_or_lexicalized_examples": choose_inventory_examples(pair_rows, "", environments={"compound_or_lexicalized"}, limit=2),
                "homophone_or_noise_notes": homophone_or_noise_notes(pair_id, pair_rows, questionnaire_entry, pair),
                "bible_attestation_profile": bible_profile,
                "lexical_pair_status": lexical_status,
                "recommended_grammar_treatment": grammar_treatment,
                "print_example_status": print_status,
                "promotion_status": promotion_status,
                "promotion_blocker": promotion_blocker,
                "notes": merge_notes(*notes),
            }
        )

        selected_examples = {"form_i": None, "form_ii": None}
        for stem_alt, form_side, form in (("I", "form_i", form_i), ("II", "form_ii", form_ii)):
            selected = choose_promotable_example_row(
                pair_rows,
                form=form,
                stem_alt=stem_alt,
                pair_id=pair_id,
                lexical_category=lexical_category,
            )
            if selected is None:
                continue
            selected_examples[form_side] = selected
            if promotion_status == "mention_as_questionnaire_control":
                reason_selected = "Best Bible attestation for a same-form questionnaire control."
            elif lexical_category == "noun_or_nominal_compound":
                reason_selected = "Best available audit row for a blocked nominal or compound-like analyzer pair."
            elif lexical_category == "lexicalized_or_category_mixed" and is_clean_verbal_row(selected, form, pair_id, lexical_category):
                reason_selected = "Best clean verbal row from a difficult lexicalized or category-mixed family."
            elif lexical_category == "lexicalized_or_category_mixed":
                reason_selected = "Best available difficult-case row from a lexicalized or category-mixed family."
            elif is_clean_verbal_row(selected, form, pair_id, lexical_category):
                reason_selected = f"Best clean verbal {form_side.replace('_', ' ')} row after lexical-category filtering."
            else:
                reason_selected = "Best currently available audit row pending manual philological review."

            promotable_rows.append(
                {
                    "lexeme_id": pair_id,
                    "form_side": form_side,
                    "reference": selected["reference"],
                    "verse_id": selected["verse_id"],
                    "token_index": selected["token_index"],
                    "surface_form": selected["surface_form"],
                    "normalized_form": selected["normalized_form"],
                    "segmentation": selected["segmentation"],
                    "gloss_span": selected["gloss"],
                    "lemma": selected["lemma"],
                    "pos": selected["pos"],
                    "local_context": selected["local_context"],
                    "kjv": selected["kjv"],
                    "environment": selected["inferred_environment"],
                    "lexical_category": lexical_category,
                    "example_quality": example_quality_for_row(
                        selected,
                        form=form,
                        pair_id=pair_id,
                        lexical_category=lexical_category,
                        promotion_status=promotion_status,
                    ),
                    "reason_selected": reason_selected,
                    "blocking_or_caveat_notes": merge_notes(
                        promotion_blocker if promotion_blocker != "none" else "",
                        homophone_or_noise_notes(pair_id, pair_rows, questionnaire_entry, pair),
                        selected.get("notes", ""),
                    ),
                }
            )

        if (
            pair_id in MANUAL_PROMOTION_REVIEW_TARGETS
            or (lexical_category == "lexical_verb" and baseline_promotion_status != "promote_to_main_grammar")
            or (lexical_category == "lexical_verb" and clean_verb_form_i_count > 0 and clean_verb_form_ii_count > 0)
        ):
            override = MANUAL_REVIEW_OVERRIDES.get(pair_id, {})
            recommended_new_promotion_status = promotion_status
            manual_review_decision = override.get(
                "manual_review_decision",
                default_manual_review_decision(lexical_category, recommended_new_promotion_status),
            )
            recommended_grammar_location = override.get(
                "recommended_grammar_location",
                default_grammar_location(lexical_category, recommended_new_promotion_status),
            )
            main_obstacle = override.get(
                "main_obstacle",
                promotion_blocker.replace("_", " ") if promotion_blocker != "none" else "none",
            )
            manual_review_rows.append(
                {
                    "lexeme_id": pair_id,
                    "form_i": form_i,
                    "form_ii": form_ii,
                    "gloss": gloss,
                    "current_lexical_category": lexical_category,
                    "current_promotion_status": baseline_promotion_status,
                    "current_promotion_blocker": promotion_blocker,
                    "clean_verb_form_i_count": str(clean_verb_form_i_count),
                    "clean_verb_form_ii_count": str(clean_verb_form_ii_count),
                    "best_form_i_review_example": format_manual_review_example(selected_examples["form_i"]),
                    "best_form_ii_review_example": format_manual_review_example(selected_examples["form_ii"]),
                    "environment_distribution_summary": summarize_environment_distribution(pair_rows, form_i, form_ii),
                    "main_obstacle": main_obstacle,
                    "manual_review_decision": manual_review_decision,
                    "recommended_new_promotion_status": recommended_new_promotion_status,
                    "recommended_grammar_location": recommended_grammar_location,
                    "decision_rationale": override.get(
                        "decision_rationale",
                        default_manual_review_rationale(pair_id, lexical_category, manual_review_decision, main_obstacle),
                    ),
                    "next_manual_check": override.get(
                        "next_manual_check",
                        default_next_manual_check(manual_review_decision, recommended_new_promotion_status),
                    ),
                }
            )

    with LEXICAL_INVENTORY_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LEXICAL_INVENTORY_COLUMNS, delimiter="\t")
        writer.writeheader()
        writer.writerows(inventory_rows)

    with PROMOTABLE_EXAMPLES_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PROMOTABLE_EXAMPLES_COLUMNS, delimiter="\t")
        writer.writeheader()
        writer.writerows(
            sorted(
                promotable_rows,
                key=lambda row: (row["lexeme_id"], row["form_side"] != "form_i", row["reference"], int(row["token_index"])),
            )
        )

    with MANUAL_PROMOTION_REVIEW_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANUAL_PROMOTION_REVIEW_COLUMNS, delimiter="\t")
        writer.writeheader()
        writer.writerows(sorted(manual_review_rows, key=lambda row: row["lexeme_id"]))


def display_path(path: Path) -> Path:
    try:
        return path.relative_to(ROOT)
    except ValueError:
        return path


def row_print_status(
    pair: PairMeta,
    row: dict[str, str],
    environment: str,
    accepted_candidate_row_keys: set[tuple[str, str, str]],
) -> tuple[str, str]:
    if environment in {"causative_or_derivational_sak", "compound_or_lexicalized"}:
        return "exclude_for_now", "Derived or lexicalized environments stay excluded at the row level even when the pair is retained for review."
    if environment == "unknown_or_needs_review":
        return "needs_analyzer_review", "Review-bucket rows never count as print-ready evidence."

    contaminated, contamination_note = row_has_obvious_contamination(pair, row)
    if contaminated:
        if pair.publication_status in {"exclude_for_now", "dossier_only"}:
            return pair.publication_status, contamination_note
        return "needs_analyzer_review", contamination_note

    if pair.publication_status in {"exclude_for_now", "dossier_only", "needs_analyzer_review"}:
        return pair.publication_status, "Row status is capped by the pair-level publication status."

    row_key = (pair.pair_id, row["verse_id"], row["token_index"])
    if row_key in accepted_candidate_row_keys:
        return pair.publication_status, "Accepted candidate TSV evidence can inherit the pair's editorial status."

    if (
        row_key in MANUAL_REVIEW_ROW_ALLOWLIST
        and analysis_clarity_score(row) >= 3
        and environment in REVIEW_CITED_SAFE_ENVIRONMENTS
    ):
        return MANUAL_REVIEW_ROW_ALLOWLIST[row_key], "This exact row is a manually checked review example kept as caveated evidence in the packet."

    return "needs_analyzer_review", "Row is useful for matrix review, but it is not strong enough to inherit the pair's print-facing status."


def write_corpus_audit() -> None:
    require_tokens_export()

    pairs = build_pair_inventory()
    verses = load_verse_metadata()
    accepted_candidate_row_keys = load_accepted_candidate_row_keys(pairs)
    review_bundle_text = load_review_bundle_text()
    review_references = extract_exact_review_references(review_bundle_text)
    form_ii_counts = count_form_ii_hits(pairs)
    form_i_index, form_ii_index, canonical_by_form_i = build_indexes(pairs, form_ii_counts)

    pair_counts: dict[str, Counter] = defaultdict(Counter)
    pair_form_env_counts: dict[str, dict[str, Counter]] = defaultdict(lambda: {"I": Counter(), "II": Counter(), "": Counter()})
    example_counts: Counter = Counter()
    best_examples: dict[tuple[str, str, str], dict[str, object]] = {}
    env_summary: dict[tuple[str, str], dict[str, object]] = defaultdict(
        lambda: {
            "form_i_count": 0,
            "form_ii_count": 0,
            "total_count": 0,
            "references": [],
            "notes": Counter(),
        }
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    row_order = 0
    with CORPUS_AUDIT_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CORPUS_COLUMNS, delimiter="\t")
        writer.writeheader()

        for verse_id, verse_tokens in iter_tokens_by_verse():
            verse_meta = verses.get(verse_id)
            if verse_meta is None:
                continue

            for index, row in enumerate(verse_tokens):
                pair_id, pair_note = resolve_pair_id(row, form_i_index, form_ii_index, canonical_by_form_i)
                if not pair_id:
                    continue

                pair = pairs[pair_id]
                attested_form, stem_alt, attested_note = infer_attested_form(row, pair)
                environment, env_confidence, env_note = infer_environment(verse_tokens, index, pair, row)
                context = local_context(verse_tokens, index)
                row_for_status = {
                    "pair_id": pair.pair_id,
                    "form_i": pair.form_i,
                    "form_ii": pair.form_ii,
                    "attested_form": attested_form,
                    "verse_id": verse_id,
                    "reference": verse_meta["reference"],
                    "token_index": row["token_index"],
                    "surface_form": row["surface_form"],
                    "normalized_form": row["normalized_form"],
                    "segmentation": row["segmentation"],
                    "gloss": row["gloss"],
                    "lemma": row["lemma"],
                    "pos": row["pos"],
                    "local_context": context,
                    "environment": environment,
                    "notes": " ".join(note for note in (pair.notes, pair_note, attested_note, env_note) if note),
                }
                print_status, status_note = row_print_status(
                    pair,
                    row_for_status,
                    environment,
                    accepted_candidate_row_keys,
                )
                notes = merge_notes(row_for_status["notes"], status_note)
                audit_row = {
                    "pair_id": pair.pair_id,
                    "form_i": pair.form_i,
                    "form_ii": pair.form_ii,
                    "attested_form": attested_form,
                    "stem_form": row["stem_form"],
                    "verse_id": verse_id,
                    "reference": verse_meta["reference"],
                    "token_index": row["token_index"],
                    "surface_form": row["surface_form"],
                    "normalized_form": row["normalized_form"],
                    "segmentation": row["segmentation"],
                    "gloss": row["gloss"],
                    "lemma": row["lemma"],
                    "pos": row["pos"],
                    "stem_alternation": stem_alt,
                    "prefix_chain": row["prefix_chain"],
                    "suffix_chain": row["suffix_chain"],
                    "usage_type": row["usage_type"],
                    "function_type": row["function_type"],
                    "local_context": context,
                    "kjv": verse_meta["kjv"],
                    "inferred_environment": environment,
                    "environment_confidence": env_confidence,
                    "print_status": print_status,
                    "notes": notes,
                }

                writer.writerow(audit_row)

                pair_counts[pair.pair_id]["total"] += 1
                if stem_alt == "I":
                    pair_counts[pair.pair_id]["form_i_total"] += 1
                if stem_alt == "II":
                    pair_counts[pair.pair_id]["form_ii_total"] += 1
                pair_form_env_counts[pair.pair_id][stem_alt][environment] += 1

                env_key = (pair.pair_id, environment)
                env_bucket = env_summary[env_key]
                env_bucket["total_count"] += 1
                if stem_alt == "I":
                    env_bucket["form_i_count"] += 1
                if stem_alt == "II":
                    env_bucket["form_ii_count"] += 1
                if verse_meta["reference"] not in env_bucket["references"] and len(env_bucket["references"]) < 5:
                    env_bucket["references"].append(verse_meta["reference"])
                env_bucket["notes"][env_note] += 1

                if stem_alt in {"I", "II"}:
                    key = (pair.pair_id, stem_alt, environment)
                    example_counts[key] += 1
                    example_row = {
                        "pair_id": pair.pair_id,
                        "form_i": pair.form_i,
                        "form_ii": pair.form_ii,
                        "gloss": pair.gloss,
                        "alternation_type": pair.alternation_type,
                        "stem_side": "form_i" if stem_alt == "I" else "form_ii",
                        "attested_form": attested_form,
                        "environment": environment,
                        "verse_id": verse_id,
                        "reference": verse_meta["reference"],
                        "token_index": row["token_index"],
                        "surface_form": row["surface_form"],
                        "normalized_form": row["normalized_form"],
                        "segmentation": row["segmentation"],
                        "gloss_span": row["gloss"],
                        "lemma": row["lemma"],
                        "pos": row["pos"],
                        "local_context": context,
                        "kjv": verse_meta["kjv"],
                        "print_status": print_status,
                        "notes": merge_notes(
                            notes,
                            "Review bucket only; not a clean syntactic construction." if environment == "unknown_or_needs_review" else "",
                            "Candidate for print." if print_status in {"print_ready", "print_usable_with_caveat"} else "",
                            "Needs review before print use." if print_status in {"dossier_only", "needs_analyzer_review"} else "",
                        ),
                    }
                    priority = selection_priority(
                        example_row,
                        accepted_candidate_row_keys,
                        review_references,
                        row_order,
                    )
                    current = best_examples.get(key)
                    if current is None or priority > current["priority"]:
                        best_examples[key] = {"priority": priority, "row": example_row}
                row_order += 1

    with ENV_SUMMARY_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ENV_SUMMARY_COLUMNS, delimiter="\t")
        writer.writeheader()
        for pair_id, pair in sorted(pairs.items()):
            pair_environments = sorted(
                key for key in env_summary
                if key[0] == pair_id
            )
            for _, environment in pair_environments:
                bucket = env_summary[(pair_id, environment)]
                writer.writerow(
                    {
                        "pair_id": pair_id,
                        "form_i": pair.form_i,
                        "form_ii": pair.form_ii,
                        "environment": environment,
                        "form_i_count": bucket["form_i_count"],
                        "form_ii_count": bucket["form_ii_count"],
                        "total_count": bucket["total_count"],
                        "representative_references": "; ".join(bucket["references"]),
                        "notes": join_top(bucket["notes"], limit=1),
                    }
                )

    with PAIR_SUMMARY_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PAIR_SUMMARY_COLUMNS, delimiter="\t")
        writer.writeheader()
        for pair_id, pair in sorted(pairs.items()):
            counts = pair_counts[pair_id]
            dominant_i = pair_form_env_counts[pair_id]["I"]
            dominant_ii = pair_form_env_counts[pair_id]["II"]
            recommendation = recommendation_for_pair(pair, counts["form_i_total"], counts["form_ii_total"], list(dominant_ii))
            note_parts = []
            siblings = sorted(other for other in form_i_index[pair.form_i] if other != pair_id)
            if siblings:
                note_parts.append(f"Shared Form I base with {', '.join(siblings)}.")
            if pair.notes:
                note_parts.append(pair.notes)
            writer.writerow(
                {
                    "pair_id": pair_id,
                    "form_i": pair.form_i,
                    "form_ii": pair.form_ii,
                    "gloss": pair.gloss,
                    "alternation_type": pair.alternation_type,
                    "form_i_total": counts["form_i_total"],
                    "form_ii_total": counts["form_ii_total"],
                    "total": counts["total"],
                    "dominant_form_i_environments": join_top(dominant_i),
                    "dominant_form_ii_environments": join_top(dominant_ii),
                    "analyzer_status": pair.analyzer_status,
                    "used_in_print_packet": "yes" if pair.used_in_print_packet else "no",
                    "in_candidate_tsv": "yes" if pair.in_candidate_tsv else "no",
                    "candidate_statuses": ", ".join(pair.candidate_statuses),
                    "publication_status": pair.publication_status,
                    "recommendation": recommendation,
                    "notes": " ".join(note_parts),
                }
            )

    with EXAMPLE_MATRIX_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=EXAMPLE_MATRIX_COLUMNS, delimiter="\t")
        writer.writeheader()
        for key in sorted(best_examples, key=lambda item: (item[0], item[1] != "I", item[2])):
            pair_id, stem_alt, environment = key
            example = dict(best_examples[key]["row"])
            example["environment_count_for_side"] = str(example_counts[key])
            example["selection_reason"] = build_selection_reason(
                example,
                accepted_candidate_row_keys,
                review_references,
            )
            writer.writerow(example)

    write_lexical_inventory(pairs, form_i_index, verses)

    print(f"Wrote {display_path(CORPUS_AUDIT_PATH)}")
    print(f"Wrote {display_path(ENV_SUMMARY_PATH)}")
    print(f"Wrote {display_path(PAIR_SUMMARY_PATH)}")
    print(f"Wrote {display_path(EXAMPLE_MATRIX_PATH)}")
    print(f"Wrote {display_path(LEXICAL_INVENTORY_PATH)}")
    print(f"Wrote {display_path(PROMOTABLE_EXAMPLES_PATH)}")


def main() -> None:
    write_corpus_audit()


if __name__ == "__main__":
    main()
