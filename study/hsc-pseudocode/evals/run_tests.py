#!/usr/bin/env python3
"""
HSC Pseudocode Linter — Test Suite

Runs the linter against:
  1. Verbatim spec examples (pp.15–21) — checks for expected issues only
  2. A correct custom example — should pass clean
  3. A deliberately broken example — should catch all planted errors

Usage:
    python3 evals/run_tests.py
"""

import sys
import os

# Add parent dir so we can import the linter
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.hsc_pseudocode_linter import lint_pseudocode, LintIssue

PASS = "\033[92mPASS\033[0m"
FAIL = "\033[91mFAIL\033[0m"

results = []


def run_test(name, text, expected_clean=None, expected_min_issues=None,
             must_contain=None, must_not_contain=None):
    """
    Run a single test case.
    
    Args:
        name: Test name for reporting
        text: Pseudocode to lint
        expected_clean: If True, expect zero issues. If False, expect some issues.
        expected_min_issues: Minimum number of issues expected
        must_contain: List of substrings that must appear in at least one issue message
        must_not_contain: List of substrings that must NOT appear in any issue message
    """
    issues = lint_pseudocode(text)
    all_messages = " ".join(str(i) for i in issues)
    passed = True
    failures = []
    
    if expected_clean is True and len(issues) > 0:
        passed = False
        failures.append(f"Expected clean but got {len(issues)} issue(s):")
        for iss in issues:
            failures.append(f"  - {iss}")
    
    if expected_clean is False and len(issues) == 0:
        passed = False
        failures.append("Expected issues but got none")
    
    if expected_min_issues is not None and len(issues) < expected_min_issues:
        passed = False
        failures.append(f"Expected at least {expected_min_issues} issues, got {len(issues)}")
    
    if must_contain:
        for substring in must_contain:
            if substring.lower() not in all_messages.lower():
                passed = False
                failures.append(f"Expected to find '{substring}' in issues but didn't")
    
    if must_not_contain:
        for substring in must_not_contain:
            if substring.lower() in all_messages.lower():
                passed = False
                failures.append(f"Did NOT expect to find '{substring}' in issues but did")
    
    status = PASS if passed else FAIL
    print(f"  {status}  {name} ({len(issues)} issue(s))")
    if not passed:
        for f in failures:
            print(f"         {f}")
    
    results.append(passed)
    return passed


def load_file(filename):
    """Load a test file from the evals directory."""
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, 'r') as f:
        return f.read()


def main():
    print("=" * 60)
    print("HSC Pseudocode Linter — Test Suite")
    print("=" * 60)
    
    # ── Spec examples (verbatim from NESA PDF) ──
    print("\n--- Spec Examples (verbatim from course spec) ---")
    
    run_test(
        "p.15 Binary Selection",
        load_file("spec_p15_binary_selection.txt"),
        expected_clean=True
    )
    
    run_test(
        "p.16 Nested IF & CASEWHERE",
        load_file("spec_p16_nested_if_case.txt"),
        expected_clean=True
    )
    
    run_test(
        "p.17 WHILE & REPEAT loops",
        load_file("spec_p17_loops.txt"),
        expected_clean=True
    )
    
    run_test(
        "p.18 FOR/NEXT",
        load_file("spec_p18_for_next.txt"),
        expected_clean=True
    )
    
    # pp.19-21 have known capitalisation inconsistencies in the spec itself
    run_test(
        "p.19 One Parameter (spec has 'Get' not 'GET')",
        load_file("spec_p19_one_param.txt"),
        expected_clean=False,
        must_contain=["GET"]  # should flag the lowercase Get
    )
    
    run_test(
        "p.20 Pass-by-Ref (spec has 'Display' not 'DISPLAY', 'to' not 'TO')",
        load_file("spec_p20_pass_by_ref.txt"),
        expected_clean=False,
        must_contain=["DISPLAY", "TO"]  # should flag both
    )
    
    run_test(
        "p.21 Function RETURN (spec has 'Display' not 'DISPLAY', 'to' not 'TO')",
        load_file("spec_p21_function_return.txt"),
        expected_clean=False,
        must_contain=["DISPLAY", "TO"]  # should flag both
    )
    
    # ── Correct example ──
    print("\n--- Correct Pseudocode (should pass clean) ---")
    
    run_test(
        "L-plate tracker example",
        load_file("test_correct_lplate.txt"),
        expected_clean=True
    )
    
    # ── Deliberate errors ──
    print("\n--- Deliberate Errors (should catch all) ---")
    
    run_test(
        "All error types",
        load_file("test_deliberate_errors.txt"),
        expected_clean=False,
        expected_min_issues=10,
        must_contain=[
            "BEGIN",       # lowercase begin
            "LET",         # LET usage
            "SET",         # lowercase set
            "ENDIF",       # missing ENDIF
            "THEN",        # missing THEN
            "DISPLAY",     # lowercase display
            "ENDWHILE",    # lowercase endwhile
            "Named param", # named parameters
            "Dot notation", # dot notation
            "END",         # lowercase end
        ]
    )
    
    # ── Targeted edge-case tests ──
    print("\n--- Edge Cases ---")
    
    run_test(
        "Lowercase 'then' detected as capitalisation error",
        "IF x > 5 then\n    DISPLAY x\nENDIF",
        expected_clean=False,
        must_contain=["THEN"],
        must_not_contain=["missing"]  # should say "capitalise", not "missing"
    )
    
    run_test(
        "Lowercase 'to' in FOR loop",
        "FOR i = 1 to 10\n    DISPLAY i\nNEXT i",
        expected_clean=False,
        must_contain=["TO"]
    )
    
    run_test(
        "Lowercase 'step' in FOR loop",
        "FOR i = 1 TO 10 step 2\n    DISPLAY i\nNEXT i",
        expected_clean=False,
        must_contain=["STEP"]
    )
    
    run_test(
        "END name mismatch",
        "BEGIN Foo (x)\n    SET y = x + 1\nEND Bar (x)",
        expected_clean=False,
        must_contain=["doesn't match"]
    )
    
    run_test(
        "END missing params",
        "BEGIN Foo (x, y)\n    SET z = x + y\nEND Foo",
        expected_clean=False,
        must_contain=["missing parameters"]
    )
    
    run_test(
        "Variable near-miss typo",
        "BEGIN Test\n    SET logging_enabled = True\n    SET loging_enabled = False\nEND Test",
        expected_clean=False,
        must_contain=["typo"]
    )
    
    run_test(
        "Clean single function",
        "BEGIN CalculateArea (length, width)\n    SET area = length * width\n    RETURN area\nEND CalculateArea (length, width)",
        expected_clean=True
    )
    
    run_test(
        "Comments should not trigger false positives",
        "# This is a comment about the begin of the process\nBEGIN Main\n    # set up the display for the user\n    SET x = 5\n    DISPLAY x\nEND Main",
        expected_clean=True
    )
    
    # ── Summary ──
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    if passed == total:
        print(f"\033[92mAll {total} tests passed!\033[0m")
    else:
        print(f"\033[91m{passed}/{total} tests passed, {total - passed} failed\033[0m")
    print("=" * 60)
    
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
