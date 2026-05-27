import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEXICAL_INVENTORY_PATH = ROOT / "output/publication_review/stem_alternation_lexical_inventory.tsv"
PROMOTABLE_EXAMPLES_PATH = ROOT / "output/publication_review/stem_alternation_promotable_examples.tsv"
GRAMMAR_SLICE_PATH = ROOT / "output/publication_review/grammar_stem_alternation_print_slice.md"

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


def load_tsv(path: Path):
    with path.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return set(reader.fieldnames or []), list(reader)


def section_between(text: str, start_heading: str, end_heading: str) -> str:
    start = text.index(start_heading)
    end = text.index(end_heading, start)
    return text[start:end]


def test_stem_alternation_lexical_inventory_and_promotable_examples_exist_with_required_columns():
    inventory_header, inventory_rows = load_tsv(LEXICAL_INVENTORY_PATH)
    promotable_header, promotable_rows = load_tsv(PROMOTABLE_EXAMPLES_PATH)

    assert REQUIRED_INVENTORY_COLUMNS <= inventory_header
    assert REQUIRED_PROMOTABLE_COLUMNS <= promotable_header
    assert inventory_rows
    assert promotable_rows


def test_stem_alternation_lexical_inventory_includes_psc_and_analyzer_pairs():
    _, rows = load_tsv(LEXICAL_INVENTORY_PATH)
    lexeme_ids = {row["lexeme_id"] for row in rows}

    expected_psc = {f"{form_i}-{form_ii}" for form_i, form_ii, _ in PSC_TO_TEDIM.values()}
    expected_analyzer = {f"{form_i}-{form_ii}" for form_ii, (form_i, _) in VERB_STEM_PAIRS.items()}

    assert expected_psc <= lexeme_ids
    assert expected_analyzer <= lexeme_ids


def test_core_pairs_are_promoted_and_difficult_pairs_are_retained():
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

    for lexeme_id in {"thei-theih", "piang-pian", "ngai-ngaih"}:
        assert row_map[lexeme_id]["promotion_status"] == "discuss_as_difficult_case"


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
    assert find("pua-puak", "form_i")["example_quality"] == "blocked_noise"


def test_lexical_inventory_keeps_noisy_forms_out_of_best_clean_examples():
    _, rows = load_tsv(LEXICAL_INVENTORY_PATH)
    noisy_forms = {"piangsak", "ngaihsutna", "luimu", "mualtung"}
    row_map = {row["lexeme_id"]: row for row in rows}

    for row in rows:
        best_examples = f"{row['best_clean_verb_form_i_examples']} {row['best_clean_verb_form_ii_examples']}".lower()
        assert all(noisy_form not in best_examples for noisy_form in noisy_forms)

    assert "piangsak" in row_map["piang-pian"]["homophone_or_noise_notes"]
    assert "ngaihsun/ngaihsut/ngaihsutna" in row_map["ngai-ngaih"]["homophone_or_noise_notes"]


def test_grammar_slice_keeps_main_inventory_nominal_free_and_retains_controls_and_difficult_cases():
    text = GRAMMAR_SLICE_PATH.read_text(encoding="utf-8")
    main_inventory = section_between(text, "# Promoted verbal inventory", "# One-sided Bible attestations and questionnaire controls")

    assert "bia ~ biak" in main_inventory
    for blocked in {"mual ~ mualh", "sum ~ sumh", "thu ~ thuh", "lampi ~ lampih", "khua ~ khuat"}:
        assert blocked not in main_inventory

    assert "# One-sided Bible attestations and questionnaire controls" in text
    assert "# Stative/adjectival and functional predicates" in text
    assert "# Analyzer-only uncertain rows" in text
    assert "# Difficult cases" in text
    assert "same-form questionnaire controls" in text
    assert "thei ~ theih" in text
    assert "piang ~ pian" in text
    assert "ngai ~ ngaih" in text
    assert "honkhia ~ honkhiat" in text
    assert "hu ~ huh" in text
