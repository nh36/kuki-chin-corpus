import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEXICAL_INVENTORY_PATH = ROOT / "output/publication_review/stem_alternation_lexical_inventory.tsv"
GRAMMAR_SLICE_PATH = ROOT / "output/publication_review/grammar_stem_alternation_print_slice.md"

sys.path.insert(0, str(ROOT / "scripts"))
from analyze_morphemes import VERB_STEM_PAIRS  # noqa: E402
from generate_vsa_report import PSC_TO_TEDIM  # noqa: E402


REQUIRED_COLUMNS = {
    "lexeme_id",
    "form_i",
    "form_ii",
    "gloss",
    "alternation_type",
    "source_secondary_literature",
    "source_vsa_questionnaire",
    "source_analyzer_inventory",
    "source_corpus_audit",
    "source_notes",
    "form_i_bible_attested",
    "form_ii_bible_attested",
    "form_i_clean_token_count",
    "form_ii_clean_token_count",
    "form_i_family_count",
    "form_ii_family_count",
    "best_form_i_examples",
    "best_form_ii_examples",
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
    "notes",
}


def load_tsv(path: Path):
    with path.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return set(reader.fieldnames or []), list(reader)


def test_stem_alternation_lexical_inventory_exists_and_has_required_columns():
    header, rows = load_tsv(LEXICAL_INVENTORY_PATH)
    assert REQUIRED_COLUMNS <= header
    assert rows


def test_stem_alternation_lexical_inventory_includes_psc_and_analyzer_pairs():
    _, rows = load_tsv(LEXICAL_INVENTORY_PATH)
    lexeme_ids = {row["lexeme_id"] for row in rows}

    expected_psc = {f"{form_i}-{form_ii}" for form_i, form_ii, _ in PSC_TO_TEDIM.values()}
    expected_analyzer = {f"{form_i}-{form_ii}" for form_ii, (form_i, _) in VERB_STEM_PAIRS.items()}

    assert expected_psc <= lexeme_ids
    assert expected_analyzer <= lexeme_ids


def test_stem_alternation_lexical_inventory_includes_core_difficult_and_same_form_rows():
    _, rows = load_tsv(LEXICAL_INVENTORY_PATH)
    lexeme_ids = {row["lexeme_id"] for row in rows}

    for required in {
        "mu-muh",
        "ne-nek",
        "nei-neih",
        "za-zak",
        "pia-piak",
        "nusia-nusiat",
        "thei-theih",
        "piang-pian",
        "ngai-ngaih",
        "honkhia-honkhiat",
        "hu-huh",
        "dawn-dawn",
        "pai-pai",
        "hong-hong",
        "om-om",
        "ci-ci",
        "hi-hi",
        "bawl-bawl",
        "zui-zui",
    }:
        assert required in lexeme_ids


def test_same_form_questionnaire_rows_stay_one_sided_and_non_print_ready():
    _, rows = load_tsv(LEXICAL_INVENTORY_PATH)
    row_map = {row["lexeme_id"]: row for row in rows}

    for lexeme_id in {"dawn-dawn", "pai-pai", "hong-hong", "om-om", "ci-ci", "hi-hi", "bawl-bawl", "zui-zui"}:
        row = row_map[lexeme_id]
        assert row["source_vsa_questionnaire"] == "yes"
        assert row["form_i"] == row["form_ii"]
        assert row["lexical_pair_status"] == "questionnaire_pair_bible_one_sided"
        assert row["recommended_grammar_treatment"] == "mention_as_literature_or_questionnaire_only"
        assert row["print_example_status"] == "needs_analyzer_review"


def test_lexical_inventory_keeps_noisy_forms_out_of_best_clean_examples():
    _, rows = load_tsv(LEXICAL_INVENTORY_PATH)
    noisy_forms = {"piangsak", "ngaihsutna", "luimu", "mualtung"}
    row_map = {row["lexeme_id"]: row for row in rows}

    for row in rows:
        best_examples = f"{row['best_form_i_examples']} {row['best_form_ii_examples']}".lower()
        assert all(noisy_form not in best_examples for noisy_form in noisy_forms)

    assert row_map["honkhia-honkhiat"]["form_i_clean_token_count"] == "0"
    assert row_map["honkhia-honkhiat"]["form_ii_clean_token_count"] == "0"
    assert row_map["hu-huh"]["form_i_clean_token_count"] == "0"
    assert row_map["hu-huh"]["form_ii_clean_token_count"] == "0"
    assert "piangsak" in row_map["piang-pian"]["homophone_or_noise_notes"]
    assert "ngaihsun/ngaihsut/ngaihsutna" in row_map["ngai-ngaih"]["homophone_or_noise_notes"]


def test_grammar_slice_discusses_inventory_beyond_print_safety():
    text = GRAMMAR_SLICE_PATH.read_text(encoding="utf-8")

    assert "larger lexical inventory" in text
    assert "one-sided Bible attestations" in text
    assert "same-form questionnaire items" in text
    assert "not itself a set of print-safe quotations" in text
    assert "not every non-print-ready verb is omitted from discussion" in text
