#!/usr/bin/env python3
"""Run the full grammar-facing publication-review validation sequence."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]

PYTEST_FILES = [
    "tests/test_stem_alternation_normalized_print_slice.py",
    "tests/test_nominalization_normalized_print_slice.py",
    "tests/test_clause_linkage_normalized_print_slice.py",
    "tests/test_switch_reference_normalized_print_slice.py",
    "tests/test_relative_clauses_normalized_print_slice.py",
    "tests/test_ki_reflexive_middle_normalized_print_slice.py",
    "tests/test_pih_comitative_applicative_normalized_print_slice.py",
    "tests/test_hong_kong_object_prefix_normalized_print_slice.py",
    "tests/test_verb_paradigms_normalized_print_slice.py",
    "tests/test_phonology_tone_normalized_print_slice.py",
    "tests/test_prefix_agreement_normalized_print_slice.py",
    "tests/test_pronouns_normalized_print_slice.py",
    "tests/test_demonstratives_normalized_print_slice.py",
    "tests/test_interrogatives_normalized_print_slice.py",
    "tests/test_sentence_final_particles_normalized_print_slice.py",
    "tests/test_negation_normalized_print_slice.py",
    "tests/test_coordinators_normalized_print_slice.py",
    "tests/test_reduplication_normalized_print_slice.py",
    "tests/test_transitivity_normalized_print_slice.py",
    "tests/test_derivation_valency_normalized_print_slice.py",
    "tests/test_vp_structure_stacking_normalized_print_slice.py",
    "tests/test_tam_normalized_print_slice.py",
    "tests/test_directionals_normalized_print_slice.py",
    "tests/test_relators_postpositions_normalized_print_slice.py",
    "tests/test_grammar_facing_pdf_style.py",
    "tests/test_assembled_grammar_review_preview.py",
    "tests/test_case_marking_normalized_print_slice.py",
    "tests/test_noun_domain_normalized_print_slice.py",
    "tests/test_np_possession_normalized_print_slice.py",
    "tests/test_quantifiers_normalized_print_slice.py",
    "tests/test_numerals_normalized_print_slice.py",
    "tests/test_coverage_normalization_audit.py",
    "tests/test_post_normalization_coverage_checkpoint.py",
    "tests/test_consistency_drift_invariant_audit.py",
    "tests/test_report_to_grammar_coverage_reconciliation.py",
    "tests/test_publication_review_packet_integrity.py",
]


def run_step(heading: str, command: list[str]) -> None:
    print(f"== {heading} ==")
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    try:
        run_step(
            "Rebuilding grammar-facing preview",
            [sys.executable, "scripts/assemble_publication_review_preview.py", "--grammar-facing"],
        )
        run_step(
            "Running grammar-facing quality gate",
            [
                sys.executable,
                "scripts/grammar_pdf_quality_gate.py",
                "output/publication_review/assembled_grammar_review_preview.tex",
            ],
        )
        run_step(
            "Running publication-review pytest suite",
            [sys.executable, "-m", "pytest", *PYTEST_FILES, "-v", "--tb=short"],
        )
    except subprocess.CalledProcessError as exc:
        return exc.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
