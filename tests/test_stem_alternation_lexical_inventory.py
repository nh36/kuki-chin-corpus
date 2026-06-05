import csv
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEXICAL_INVENTORY_PATH = ROOT / "output/publication_review/stem_alternation_lexical_inventory.tsv"
PROMOTABLE_EXAMPLES_PATH = ROOT / "output/publication_review/stem_alternation_promotable_examples.tsv"
MANUAL_PROMOTION_REVIEW_PATH = ROOT / "output/publication_review/stem_alternation_manual_promotion_review.tsv"
CITATION_SHORTLIST_PATH = ROOT / "output/publication_review/stem_alternation_citation_shortlist.tsv"
SYNTACTIC_CONTEXT_MATRIX_PATH = ROOT / "output/publication_review/stem_alternation_syntactic_context_matrix.tsv"
PAIR_DISCUSSION_PLAN_PATH = ROOT / "output/publication_review/stem_alternation_pair_discussion_plan.tsv"
GRAMMAR_SLICE_PATH = ROOT / "output/publication_review/grammar_stem_alternation_print_slice.md"
GRAMMAR_SECTION_DRAFT_PATH = ROOT / "output/publication_review/grammar_stem_alternation_section_draft.md"

sys.path.insert(0, str(ROOT / "scripts"))
from analyze_morphemes import VERB_STEM_PAIRS  # noqa: E402
from generate_vsa_report import PSC_TO_TEDIM  # noqa: E402


REQUIRED_INVENTORY_COLUMNS = {
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
}

REQUIRED_PROMOTABLE_COLUMNS = {
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
}

REQUIRED_MANUAL_REVIEW_COLUMNS = {
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
}

REQUIRED_CITATION_SHORTLIST_COLUMNS = {
    "lexeme_id",
    "promotion_group",
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
    "tedim_clause_or_sentence",
    "local_context",
    "kjv",
    "environment",
    "construction_label",
    "example_role",
    "citation_quality",
    "why_this_example",
    "remaining_caveat",
    "use_in_grammar",
    "notes",
}

REQUIRED_CONTEXT_MATRIX_COLUMNS = {
    "context_id",
    "context_label",
    "description",
    "expected_stem_tendency",
    "form_i_evidence_pairs",
    "form_ii_evidence_pairs",
    "quotation_safe_form_i_examples",
    "quotation_safe_form_ii_examples",
    "review_only_examples",
    "strongest_showcase_pair",
    "caveated_pairs",
    "difficult_pairs",
    "what_this_context_shows",
    "what_not_to_claim",
    "recommended_grammar_subsection",
    "notes",
}

REQUIRED_PAIR_DISCUSSION_PLAN_COLUMNS = {
    "lexeme_id",
    "form_i",
    "form_ii",
    "gloss",
    "grammar_status",
    "discussion_order",
    "form_i_attestation_summary",
    "form_ii_attestation_summary",
    "main_contexts_for_form_i",
    "main_contexts_for_form_ii",
    "best_citation_rows",
    "contexts_to_discuss",
    "main_generalization_for_this_pair",
    "caveats",
    "blocked_or_noisy_material",
    "recommended_prose_treatment",
    "include_in_core_showcase_table",
    "include_in_promoted_pair_inventory",
    "include_in_pair_by_pair_discussion",
    "include_in_coverage_or_control_table",
    "include_in_blocked_or_noise_table",
    "notes",
}


def load_tsv(path: Path):
    with path.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return set(reader.fieldnames or []), list(reader)


def section_between(text: str, start_heading: str, end_heading: str) -> str:
    start = text.index(start_heading)
    end = text.index(end_heading, start)
    return text[start:end]


def test_stem_alternation_lexical_inventory_and_review_outputs_exist_with_required_columns():
    inventory_header, inventory_rows = load_tsv(LEXICAL_INVENTORY_PATH)
    promotable_header, promotable_rows = load_tsv(PROMOTABLE_EXAMPLES_PATH)
    manual_header, manual_rows = load_tsv(MANUAL_PROMOTION_REVIEW_PATH)
    citation_header, citation_rows = load_tsv(CITATION_SHORTLIST_PATH)
    context_header, context_rows = load_tsv(SYNTACTIC_CONTEXT_MATRIX_PATH)
    pair_plan_header, pair_plan_rows = load_tsv(PAIR_DISCUSSION_PLAN_PATH)

    assert REQUIRED_INVENTORY_COLUMNS <= inventory_header
    assert REQUIRED_PROMOTABLE_COLUMNS <= promotable_header
    assert REQUIRED_MANUAL_REVIEW_COLUMNS <= manual_header
    assert REQUIRED_CITATION_SHORTLIST_COLUMNS <= citation_header
    assert REQUIRED_CONTEXT_MATRIX_COLUMNS <= context_header
    assert REQUIRED_PAIR_DISCUSSION_PLAN_COLUMNS <= pair_plan_header
    assert inventory_rows
    assert promotable_rows
    assert manual_rows
    assert citation_rows
    assert context_rows
    assert pair_plan_rows
    assert GRAMMAR_SECTION_DRAFT_PATH.exists()
    assert GRAMMAR_SECTION_DRAFT_PATH.read_text(encoding="utf-8").strip()


def test_stem_alternation_lexical_inventory_includes_psc_and_analyzer_pairs():
    _, rows = load_tsv(LEXICAL_INVENTORY_PATH)
    lexeme_ids = {row["lexeme_id"] for row in rows}

    expected_psc = {f"{form_i}-{form_ii}" for form_i, form_ii, _ in PSC_TO_TEDIM.values()}
    expected_analyzer = {f"{form_i}-{form_ii}" for form_ii, (form_i, _) in VERB_STEM_PAIRS.items()}

    assert expected_psc <= lexeme_ids
    assert expected_analyzer <= lexeme_ids


def test_core_pairs_are_promoted_and_manual_review_promotes_new_caveated_verbs():
    _, rows = load_tsv(LEXICAL_INVENTORY_PATH)
    row_map = {row["lexeme_id"]: row for row in rows}

    for lexeme_id in {"mu-muh", "ne-nek", "nei-neih"}:
        assert row_map[lexeme_id]["promotion_status"] == "promote_to_main_grammar"
        assert row_map[lexeme_id]["lexical_category"] == "lexical_verb"

    for lexeme_id in {"za-zak", "pia-piak", "nusia-nusiat"}:
        assert row_map[lexeme_id]["promotion_status"] == "promote_with_caveat"
        assert row_map[lexeme_id]["lexical_category"] == "lexical_verb"

    assert row_map["bia-biak"]["promotion_status"] == "promote_with_caveat"
    assert row_map["bia-biak"]["lexical_category"] == "lexical_verb"

    for lexeme_id in {"thei-theih", "piang-pian", "zui-zuih", "khial-khialh", "kia-kiak", "sawlkhia-sawlkhiat"}:
        assert row_map[lexeme_id]["promotion_status"] == "promote_with_caveat"

    assert row_map["ngai-ngaih"]["promotion_status"] == "discuss_as_difficult_case"


def test_same_form_questionnaire_controls_are_classified_as_controls():
    _, rows = load_tsv(LEXICAL_INVENTORY_PATH)
    row_map = {row["lexeme_id"]: row for row in rows}

    for lexeme_id in {"dawn-dawn", "pai-pai", "hong-hong", "om-om", "ci-ci", "hi-hi", "bawl-bawl", "zui-zui"}:
        row = row_map[lexeme_id]
        assert row["source_vsa_questionnaire"] == "yes"
        assert row["form_i"] == row["form_ii"]
        assert row["lexical_category"] == "same_form_questionnaire_control"
        assert row["promotion_status"] == "mention_as_questionnaire_control"
        assert row["promotion_blocker"] == "same_written_form_no_overt_alternation"


def test_nominal_rows_are_not_promoted_to_main_verb_inventory():
    _, rows = load_tsv(LEXICAL_INVENTORY_PATH)
    row_map = {row["lexeme_id"]: row for row in rows}

    for lexeme_id in {"mual-mualh", "sum-sumh", "thu-thuh", "lampi-lampih", "khua-khuat", "gamla-gamlat"}:
        row = row_map[lexeme_id]
        assert row["lexical_category"] == "noun_or_nominal_compound"
        assert row["clean_verb_form_i_count"] == "0"
        assert row["clean_verb_form_ii_count"] == "0"
        assert row["promotion_status"] == "block_from_verb_inventory_pending_review"
        assert row["promotion_blocker"] == "nominal_or_compound_examples_only"


def test_high_priority_suspicious_rows_get_expected_category_controls():
    _, rows = load_tsv(LEXICAL_INVENTORY_PATH)
    row_map = {row["lexeme_id"]: row for row in rows}

    assert row_map["no-noh"]["lexical_category"] == "stative_or_adjectival_predicate"
    assert row_map["ci-cih"]["lexical_category"] == "auxiliary_or_functional_verb"
    assert row_map["hi-hih"]["lexical_category"] == "auxiliary_or_functional_verb"
    assert row_map["om-omh"]["lexical_category"] == "auxiliary_or_functional_verb"
    assert row_map["pai-paih"]["lexical_category"] == "analyzer_only_uncertain"
    assert row_map["pua-puak"]["lexical_category"] == "lexicalized_or_category_mixed"
    assert row_map["pua-puah"]["lexical_category"] == "analyzer_only_uncertain"
    assert row_map["tua-tuak"]["lexical_category"] == "analyzer_only_uncertain"
    assert row_map["tua-tuah"]["lexical_category"] == "analyzer_only_uncertain"


def test_promotable_examples_mark_controls_nominals_and_difficult_pairs_distinctly():
    _, rows = load_tsv(PROMOTABLE_EXAMPLES_PATH)

    def find(lexeme_id, form_side):
        return next(row for row in rows if row["lexeme_id"] == lexeme_id and row["form_side"] == form_side)

    assert find("mu-muh", "form_i")["example_quality"] == "print_ready"
    assert find("bia-biak", "form_ii")["example_quality"] in {"descriptive_with_caveat", "print_usable_with_caveat"}
    assert find("dawn-dawn", "form_i")["example_quality"] == "questionnaire_control"
    assert find("mual-mualh", "form_i")["example_quality"] == "blocked_nonverbal"
    assert find("pua-puak", "form_i")["example_quality"] == "needs_manual_review"
    assert find("ngai-ngaih", "form_i")["example_quality"] == "needs_manual_review"


def test_lexical_inventory_keeps_noisy_forms_out_of_best_clean_examples():
    _, rows = load_tsv(LEXICAL_INVENTORY_PATH)
    noisy_forms = {"piangsak", "ngaihsutna", "luimu", "mualtung"}
    row_map = {row["lexeme_id"]: row for row in rows}

    for row in rows:
        best_examples = f"{row['best_clean_verb_form_i_examples']} {row['best_clean_verb_form_ii_examples']}".lower()
        assert all(noisy_form not in best_examples for noisy_form in noisy_forms)

    assert "piangsak" in row_map["piang-pian"]["homophone_or_noise_notes"]
    assert "ngaihsun/ngaihsut/ngaihsutna" in row_map["ngai-ngaih"]["homophone_or_noise_notes"]
    assert "Clean exact verbal rows still survive" in row_map["ngai-ngaih"]["category_evidence"]


def test_manual_review_covers_all_bilateral_lexical_verbs_and_key_difficult_cases():
    _, inventory_rows = load_tsv(LEXICAL_INVENTORY_PATH)
    _, manual_rows = load_tsv(MANUAL_PROMOTION_REVIEW_PATH)
    manual_map = {row["lexeme_id"]: row for row in manual_rows}

    bilateral_lexical_verbs = {
        row["lexeme_id"]
        for row in inventory_rows
        if row["lexical_category"] == "lexical_verb"
        and int(row["clean_verb_form_i_count"]) > 0
        and int(row["clean_verb_form_ii_count"]) > 0
    }
    assert bilateral_lexical_verbs <= manual_map.keys()

    assert manual_map["thei-theih"]["manual_review_decision"] == "promote_with_caveat_now"
    assert manual_map["thei-theih"]["recommended_new_promotion_status"] == "promote_with_caveat"
    assert manual_map["piang-pian"]["manual_review_decision"] == "promote_with_caveat_now"
    assert manual_map["ngai-ngaih"]["manual_review_decision"] == "retain_as_difficult_case"
    assert "clean exact verbal `ngai`/`ngaih` rows exist" in manual_map["ngai-ngaih"]["decision_rationale"]
    assert manual_map["keu-keuh"]["manual_review_decision"] == "block_nonverbal"


def test_citation_shortlist_covers_core_and_caveated_pairs():
    _, rows = load_tsv(CITATION_SHORTLIST_PATH)
    by_pair = defaultdict(list)
    for row in rows:
        by_pair[row["lexeme_id"]].append(row)

    core_pairs = {"mu-muh", "ne-nek", "nei-neih"}
    caveated_pairs = {
        "za-zak",
        "pia-piak",
        "nusia-nusiat",
        "bia-biak",
        "thei-theih",
        "piang-pian",
        "zui-zuih",
        "khial-khialh",
        "kia-kiak",
        "sawlkhia-sawlkhiat",
    }

    for lexeme_id in core_pairs | caveated_pairs:
        sides = {row["form_side"] for row in by_pair[lexeme_id]}
        assert {"form_i", "form_ii"} <= sides

    for lexeme_id in core_pairs:
        assert any(row["use_in_grammar"] == "use_as_main_example" for row in by_pair[lexeme_id])

    assert all(
        row["citation_quality"] != "print_ready"
        for row in rows
        if row["lexeme_id"] in caveated_pairs
    )


def test_citation_shortlist_keeps_special_cases_and_blocked_rows_honest():
    _, inventory_rows = load_tsv(LEXICAL_INVENTORY_PATH)
    _, citation_rows = load_tsv(CITATION_SHORTLIST_PATH)
    inventory_map = {row["lexeme_id"]: row for row in inventory_rows}

    nusia_form_ii = [
        row
        for row in citation_rows
        if row["lexeme_id"] == "nusia-nusiat" and row["form_side"] == "form_ii"
    ]
    assert nusia_form_ii
    assert all(row["citation_quality"] != "print_ready" for row in nusia_form_ii)
    assert any(row["pos"] == "N" for row in nusia_form_ii)
    assert any("clause-linking" in row["construction_label"] or "source" in row["construction_label"] for row in nusia_form_ii)

    thei_rows = [row for row in citation_rows if row["lexeme_id"] == "thei-theih"]
    assert any(
        any(keyword in row["construction_label"].lower() for keyword in {"modal", "ability", "purpose", "purposive", "nominal"})
        for row in thei_rows
    )

    piang_rows = [row for row in citation_rows if row["lexeme_id"] == "piang-pian"]
    assert piang_rows
    assert {row["normalized_form"] for row in piang_rows} <= {"piang", "pian"}

    for lexeme_id in {"zui-zuih", "khial-khialh", "kia-kiak", "sawlkhia-sawlkhiat"}:
        form_ii = inventory_map[lexeme_id]["form_ii"]
        relevant = [
            row
            for row in citation_rows
            if row["lexeme_id"] == lexeme_id and row["form_side"] == "form_ii"
        ]
        assert relevant
        assert all(
            row["normalized_form"] == form_ii or row["citation_quality"] == "needs_manual_check"
            for row in relevant
        )

    promoted_groups = {"core_showcase", "caveated_promoted"}
    for lexeme_id in {"ngai-ngaih", "pua-puak", "pai-paih", "tua-tuak", "tua-tuah", "keu-keuh", "khai-khaih", "sia-siah", "tan-tanh"}:
        relevant = [row for row in citation_rows if row["lexeme_id"] == lexeme_id]
        assert relevant
        assert all(row["promotion_group"] not in promoted_groups for row in relevant)


def test_syntactic_context_matrix_covers_major_contexts_and_claim_boundaries():
    _, rows = load_tsv(SYNTACTIC_CONTEXT_MATRIX_PATH)
    row_map = {row["context_id"]: row for row in rows}
    required_contexts = {
        "finite_main_or_matrix",
        "imperative_or_directive",
        "negative_clause",
        "dependent_temporal_ciangin",
        "dependent_temporal_ni_in",
        "clause_linking_kipan",
        "purpose_nadingin",
        "nominalized_na",
        "relative_or_attributive_mi",
        "possessed_or_genitive_attributive",
        "modal_or_ability",
        "quotative_or_say_complement",
        "compound_or_lexicalized",
        "causative_or_derivational_sak",
        "unknown_or_needs_review",
    }

    assert required_contexts <= row_map.keys()

    for context_id in required_contexts:
        row = row_map[context_id]
        assert row["context_label"]
        assert row["what_this_context_shows"]
        assert row["what_not_to_claim"]
        assert row["recommended_grammar_subsection"]
        assert (
            row["quotation_safe_form_i_examples"]
            or row["quotation_safe_form_ii_examples"]
            or row["review_only_examples"]
            or row["notes"]
        )

    assert "not a single decisive diagnostic" in row_map["negative_clause"]["expected_stem_tendency"]
    assert "Do not claim that Form II simply equals negation" in row_map["negative_clause"]["what_not_to_claim"]
    assert "Do not claim that Form I is the only possible matrix form" in row_map["finite_main_or_matrix"]["what_not_to_claim"]
    assert "Do not claim that Form II is nominalized only" in row_map["nominalized_na"]["what_not_to_claim"]
    assert row_map["imperative_or_directive"]["quotation_safe_form_ii_examples"] == ""
    assert "biakinn" not in row_map["imperative_or_directive"]["quotation_safe_form_ii_examples"]
    assert "hihpak" not in row_map["imperative_or_directive"]["quotation_safe_form_ii_examples"]

    for context_id in {"compound_or_lexicalized", "causative_or_derivational_sak", "unknown_or_needs_review"}:
        row = row_map[context_id]
        assert row["quotation_safe_form_i_examples"] == ""
        assert row["quotation_safe_form_ii_examples"] == ""
        assert row["review_only_examples"]
        assert any(word in row["expected_stem_tendency"].lower() for word in {"filter", "caution", "dangerous"})


def test_pair_discussion_plan_covers_required_pairs_and_statuses():
    _, inventory_rows = load_tsv(LEXICAL_INVENTORY_PATH)
    _, rows = load_tsv(PAIR_DISCUSSION_PLAN_PATH)
    row_map = {row["lexeme_id"]: row for row in rows}

    core_pairs = {"mu-muh", "ne-nek", "nei-neih"}
    caveated_pairs = {
        "za-zak",
        "pia-piak",
        "nusia-nusiat",
        "bia-biak",
        "thei-theih",
        "piang-pian",
        "zui-zuih",
        "khial-khialh",
        "kia-kiak",
        "sawlkhia-sawlkhiat",
    }
    difficult_pairs = {"ngai-ngaih", "pua-puak", "pai-paih", "tua-tuah", "tua-tuak"}
    one_sided_pairs = {
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
    }
    blocked_pairs = {
        "keu-keuh",
        "khai-khaih",
        "sia-siah",
        "tan-tanh",
        "mual-mualh",
        "sum-sumh",
        "thu-thuh",
        "lampi-lampih",
        "khua-khuat",
        "gamla-gamlat",
    }

    assert core_pairs <= row_map.keys()
    assert caveated_pairs <= row_map.keys()
    assert difficult_pairs <= row_map.keys()
    assert one_sided_pairs <= row_map.keys()
    assert blocked_pairs <= row_map.keys()

    same_form_controls = {
        row["lexeme_id"]
        for row in inventory_rows
        if row["lexical_category"] == "same_form_questionnaire_control"
    }
    assert same_form_controls <= row_map.keys()

    assert {row["lexeme_id"] for row in rows if row["include_in_core_showcase_table"] == "yes"} == core_pairs
    assert {row["lexeme_id"] for row in rows if row["include_in_promoted_pair_inventory"] == "yes"} == core_pairs | caveated_pairs

    for lexeme_id in core_pairs:
        row = row_map[lexeme_id]
        assert row["grammar_status"] == "core_showcase_pair"
        assert row["include_in_core_showcase_table"] == "yes"
        assert row["include_in_promoted_pair_inventory"] == "yes"
        assert row["include_in_pair_by_pair_discussion"] == "yes"
        assert row["include_in_coverage_or_control_table"] == "no"
        assert row["include_in_blocked_or_noise_table"] == "no"

    for lexeme_id in caveated_pairs:
        row = row_map[lexeme_id]
        assert row["grammar_status"] == "promoted_caveated_pair"
        assert row["include_in_core_showcase_table"] == "no"
        assert row["include_in_promoted_pair_inventory"] == "yes"
        assert row["include_in_pair_by_pair_discussion"] == "yes"
        assert row["include_in_coverage_or_control_table"] == "no"
        assert row["include_in_blocked_or_noise_table"] == "no"

    for lexeme_id in difficult_pairs:
        row = row_map[lexeme_id]
        assert row["grammar_status"] == "difficult_but_real_pair"
        assert row["include_in_core_showcase_table"] == "no"
        assert row["include_in_promoted_pair_inventory"] == "no"
        assert row["include_in_pair_by_pair_discussion"] == "yes"
        assert row["include_in_coverage_or_control_table"] == "no"
        assert row["include_in_blocked_or_noise_table"] == "no"

    for lexeme_id in one_sided_pairs:
        row = row_map[lexeme_id]
        assert row["grammar_status"] == "one_sided_bible_attestation"
        assert row["include_in_core_showcase_table"] == "no"
        assert row["include_in_promoted_pair_inventory"] == "no"
        assert row["include_in_pair_by_pair_discussion"] == "no"
        assert row["include_in_coverage_or_control_table"] == "yes"
        assert row["include_in_blocked_or_noise_table"] == "no"

    for lexeme_id in same_form_controls:
        row = row_map[lexeme_id]
        assert row["grammar_status"] == "same_form_questionnaire_control"
        assert row["include_in_core_showcase_table"] == "no"
        assert row["include_in_promoted_pair_inventory"] == "no"
        assert row["include_in_pair_by_pair_discussion"] == "no"
        assert row["include_in_coverage_or_control_table"] == "yes"
        assert row["include_in_blocked_or_noise_table"] == "no"

    assert row_map["om-omh"]["grammar_status"] == "functional_or_stative_predicate"
    assert any(row["grammar_status"] == "functional_or_stative_predicate" for row in rows)
    assert row_map["om-omh"]["include_in_core_showcase_table"] == "no"
    assert row_map["om-omh"]["include_in_promoted_pair_inventory"] == "no"
    assert row_map["om-omh"]["include_in_coverage_or_control_table"] == "yes"
    assert row_map["om-omh"]["include_in_blocked_or_noise_table"] == "no"

    for lexeme_id in blocked_pairs:
        row = row_map[lexeme_id]
        assert row["grammar_status"] == "rejected_nonverbal_or_noise"
        assert row["include_in_core_showcase_table"] == "no"
        assert row["include_in_promoted_pair_inventory"] == "no"
        assert row["include_in_pair_by_pair_discussion"] == "no"
        assert row["include_in_coverage_or_control_table"] == "no"
        assert row["include_in_blocked_or_noise_table"] == "yes"
        assert row["recommended_prose_treatment"] != "Use in the small core showcase table and return to it briefly at the start of the pair-by-pair discussion."


def test_grammar_slice_is_now_a_grammar_facing_section():
    text = GRAMMAR_SLICE_PATH.read_text(encoding="utf-8")
    lower_text = text.lower()
    assert "# Overview of Form I / Form II stem alternation" in text
    assert "Current stem alternation overview" in text
    assert "Distribution by syntactic context" in text
    assert "Core showcase pairs" in text
    assert "Promoted caveated pairs" in text
    assert "Difficult but grammatically important pairs" in text
    assert "One-sided and same-form controls" in text
    assert "Blocked or noisy material" in text
    assert "Several issues remain outside the present account." in text

    assert "draft argument plan" not in lower_text
    assert "eventual prose" not in lower_text
    assert "next commit" not in lower_text
    assert "writing order" not in lower_text
    assert "quotation-safe layer" not in lower_text
    assert not re.search(r"(?:output|tests|scripts|docs)/[A-Za-z0-9_./\\-]+", text)


def test_grammar_section_draft_follows_the_planned_architecture_and_quote_rules():
    _, citation_rows = load_tsv(CITATION_SHORTLIST_PATH)
    _, pair_plan_rows = load_tsv(PAIR_DISCUSSION_PLAN_PATH)

    text = GRAMMAR_SECTION_DRAFT_PATH.read_text(encoding="utf-8")
    lower_text = text.lower()

    assert "# Verb-stem alternation" in text
    assert "## Overview of the Form I / Form II contrast" in text
    assert "## Distribution by syntactic context" in text
    assert "## Core showcase examples" in text
    assert "## Promoted-pair inventory" in text
    assert "## Pair-by-pair notes for promoted and difficult pairs" in text
    assert "## One-sided / same-form / functional coverage table" in text
    assert "## Blocked/noise appendix" in text
    assert "stem_alternation_citation_shortlist.tsv` is the quotation-safe layer" in lower_text
    assert "does **not** simply reduce form ii to subordination, negation, or nominalization" in lower_text

    core_section = section_between(text, "## Core showcase examples", "## Promoted-pair inventory")
    promoted_section = section_between(text, "## Promoted-pair inventory", "## Pair-by-pair notes for promoted and difficult pairs")
    difficult_section = section_between(text, "## Pair-by-pair notes for promoted and difficult pairs", "## One-sided / same-form / functional coverage table")
    coverage_section = section_between(text, "## One-sided / same-form / functional coverage table", "## Blocked/noise appendix")
    blocked_section = text[text.index("## Blocked/noise appendix") :]
    one_sided_section = section_between(coverage_section, "### One-sided Bible attestations", "### Same-form questionnaire controls")
    same_form_section = section_between(coverage_section, "### Same-form questionnaire controls", "### Functional or stative predicates")
    functional_section = coverage_section[coverage_section.index("### Functional or stative predicates") :]

    core_pairs = {"ne ~ nek", "mu ~ muh", "nei ~ neih"}
    promoted_pairs = {
        "za ~ zak",
        "pia ~ piak",
        "nusia ~ nusiat",
        "bia ~ biak",
        "thei ~ theih",
        "piang ~ pian",
        "zui ~ zuih",
        "khial ~ khialh",
        "kia ~ kiak",
        "sawlkhia ~ sawlkhiat",
    }
    difficult_pairs = {"ngai ~ ngaih", "pua ~ puak", "pai ~ paih", "tua ~ tuah", "tua ~ tuak"}
    functional_pairs = {"ci ~ cih", "hi ~ hih", "om ~ omh"}

    def row_marker(pair: str) -> str:
        return f"| `{pair}` |"

    for pair in core_pairs:
        assert pair in core_section

    for pair in promoted_pairs:
        assert pair in promoted_section

    for pair in difficult_pairs:
        assert pair in difficult_section
        assert pair not in promoted_section

    coverage_pairs = {
        f"{row['form_i']} ~ {row['form_ii']}"
        for row in pair_plan_rows
        if row["include_in_coverage_or_control_table"] == "yes"
    }
    same_form_controls = {
        f"{row['form_i']} ~ {row['form_ii']}"
        for row in pair_plan_rows
        if row["grammar_status"] == "same_form_questionnaire_control"
    }
    blocked_pairs = {
        f"{row['form_i']} ~ {row['form_ii']}"
        for row in pair_plan_rows
        if row["include_in_blocked_or_noise_table"] == "yes"
    }
    one_sided_coverage = coverage_pairs - same_form_controls - functional_pairs

    for pair in coverage_pairs:
        assert row_marker(pair) in coverage_section

    for pair in one_sided_coverage:
        assert row_marker(pair) in one_sided_section
        assert row_marker(pair) not in same_form_section
        assert row_marker(pair) not in functional_section

    for pair in same_form_controls:
        assert row_marker(pair) in same_form_section
        assert row_marker(pair) not in one_sided_section
        assert row_marker(pair) not in functional_section

    for pair in functional_pairs:
        assert row_marker(pair) in functional_section
        assert row_marker(pair) not in one_sided_section

    for pair in blocked_pairs:
        assert row_marker(pair) in blocked_section
        assert row_marker(pair) not in core_section
        assert row_marker(pair) not in promoted_section
        assert row_marker(pair) not in difficult_section
        assert row_marker(pair) not in coverage_section

    assert "`nusia ~ nusiat`" in promoted_section
    assert "not yet quotation-ready for print" in promoted_section
    assert "### One-sided Bible attestations" in coverage_section
    assert "### Same-form questionnaire controls" in coverage_section
    assert "### Functional or stative predicates" in coverage_section
    assert "controls, not overt written stem-alternation pairs in the bible layer" in lower_text
    assert "form ii = subordinate" not in lower_text
    assert "form ii = negative" not in lower_text
    assert "form ii = nominalized" not in lower_text

    banned_uses = {"reject", "keep_in_notes_only", "mention_without_quotation"}
    for row in citation_rows:
        if row["use_in_grammar"] not in banned_uses:
            continue
        tedim_clause = row["tedim_clause_or_sentence"].strip()
        if len(tedim_clause) >= 20:
            assert tedim_clause not in text
