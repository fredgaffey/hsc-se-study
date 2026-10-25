#!/usr/bin/env python3
"""
HSC Pseudocode Linter
Checks pseudocode against NSW HSC Software Engineering Course Spec (Nov 2024) conventions.

Usage:
    python3 hsc_pseudocode_linter.py myfile.txt
    python3 hsc_pseudocode_linter.py --text "BEGIN\n..."
    
Or import and use in code:
    from hsc_pseudocode_linter import lint_pseudocode
    results = lint_pseudocode(text)
"""

import re
import sys
import argparse


# --- Rule definitions ---

# Structural pairs: (opener pattern, closer pattern, friendly name)
STRUCTURAL_PAIRS = [
    (r'^\s*BEGIN\b',    r'^\s*END\b',       'BEGIN',     'END'),
    (r'^\s*IF\b',       r'^\s*ENDIF\b',     'IF',        'ENDIF'),
    (r'^\s*WHILE\b',    r'^\s*ENDWHILE\b',  'WHILE',     'ENDWHILE'),
    (r'^\s*FOR\b',      r'^\s*NEXT\b',      'FOR',       'NEXT'),
    (r'^\s*REPEAT\b',   r'^\s*UNTIL\b',     'REPEAT',    'UNTIL'),
    (r'^\s*CASEWHERE\b', r'^\s*END\s+CASE\b', 'CASEWHERE', 'END CASE'),
]

# Keywords that must be capitalised when used as control keywords
# We check for lowercase versions of these appearing at the start of a line
# (to avoid false positives on natural language descriptions)
CONTROL_KEYWORDS_LOWER = {
    'begin': 'BEGIN',
    'endif': 'ENDIF',
    'endwhile': 'ENDWHILE',
    'casewhere': 'CASEWHERE',
    'elseif': 'ELSEIF',
    'repeat': 'REPEAT',
    'until': 'UNTIL',
}

# Keywords that could appear at the start of a line
START_OF_LINE_KEYWORDS = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'next': 'NEXT',
    'set': 'SET',
    'get': 'GET',
    'display': 'DISPLAY',
    'return': 'RETURN',
    'end': 'END',
}


class LintIssue:
    """A single linting issue."""
    
    SEVERITY_BUG = "BUG"
    SEVERITY_CONVENTION = "CONVENTION"
    SEVERITY_READABILITY = "READABILITY"
    
    def __init__(self, line_num, severity, message, suggestion=None):
        self.line_num = line_num
        self.severity = severity
        self.message = message
        self.suggestion = suggestion
    
    def __str__(self):
        prefix = f"Line {self.line_num}" if self.line_num else "General"
        result = f"[{self.severity}] {prefix}: {self.message}"
        if self.suggestion:
            result += f"\n         Fix: {self.suggestion}"
        return result


def strip_comments(line):
    """Remove comments from a line (# and everything after)."""
    # Don't strip if # is inside quotes
    in_string = False
    quote_char = None
    for i, ch in enumerate(line):
        if ch in ('"', "'") and not in_string:
            in_string = True
            quote_char = ch
        elif ch == quote_char and in_string:
            in_string = False
        elif ch == '#' and not in_string:
            return line[:i].rstrip()
    return line


def check_structural_pairs(lines):
    """Check that every opening keyword has a matching closing keyword."""
    issues = []
    
    for open_pat, close_pat, open_name, close_name in STRUCTURAL_PAIRS:
        # Track openers as a stack with line numbers
        stack = []
        
        for i, raw_line in enumerate(lines, 1):
            line = strip_comments(raw_line)
            if not line.strip():
                continue
            
            # Check for opener
            if re.match(open_pat, line):
                stack.append(i)
            
            # Check for closer
            if re.match(close_pat, line):
                # Special case: END also matches END CASE and ENDWHILE etc
                # So for the BEGIN/END pair, skip lines that are ENDIF, ENDWHILE, END CASE
                if open_name == 'BEGIN':
                    stripped = line.strip()
                    if stripped.startswith('ENDIF') or stripped.startswith('ENDWHILE') or stripped.startswith('END CASE'):
                        continue
                
                if stack:
                    stack.pop()
                else:
                    issues.append(LintIssue(
                        i, LintIssue.SEVERITY_CONVENTION,
                        f"'{close_name}' on line {i} has no matching '{open_name}'.",
                        f"Add a '{open_name}' before this '{close_name}', or remove the extra '{close_name}'."
                    ))
        
        # Any remaining openers are unmatched
        for opener_line in stack:
            issues.append(LintIssue(
                opener_line, LintIssue.SEVERITY_CONVENTION,
                f"'{open_name}' on line {opener_line} has no matching '{close_name}'.",
                f"Add '{close_name}' to close the '{open_name}' that starts on line {opener_line}."
            ))
    
    return issues


def check_keyword_capitalisation(lines):
    """Check that control keywords are capitalised."""
    issues = []
    
    for i, raw_line in enumerate(lines, 1):
        line = strip_comments(raw_line)
        stripped = line.strip()
        if not stripped:
            continue
        
        first_word = stripped.split()[0] if stripped.split() else ""
        first_word_lower = first_word.lower()
        
        # Check keywords that are unambiguous (always control keywords)
        if first_word_lower in CONTROL_KEYWORDS_LOWER and first_word != CONTROL_KEYWORDS_LOWER[first_word_lower]:
            expected = CONTROL_KEYWORDS_LOWER[first_word_lower]
            issues.append(LintIssue(
                i, LintIssue.SEVERITY_CONVENTION,
                f"Keyword '{first_word}' should be capitalised as '{expected}'.",
                f"Change '{first_word}' to '{expected}'."
            ))
        
        # Check start-of-line keywords (these could be natural language, so only flag
        # if they look like they're being used as keywords)
        if first_word_lower in START_OF_LINE_KEYWORDS and first_word != START_OF_LINE_KEYWORDS[first_word_lower]:
            expected = START_OF_LINE_KEYWORDS[first_word_lower]
            # Heuristic: if the word is followed by patterns that suggest keyword usage
            is_keyword = False
            rest = stripped[len(first_word):].strip()
            
            if first_word_lower == 'if' and 'then' in rest.lower():
                is_keyword = True
            elif first_word_lower == 'else' and (rest == '' or rest.lower().startswith('if')):
                is_keyword = True
            elif first_word_lower == 'while' and ('=' in rest or 'true' in rest.lower() or 'false' in rest.lower() or 'not' in rest.lower() or 'and' in rest.lower() or 'or' in rest.lower()):
                is_keyword = True
            elif first_word_lower == 'for' and ('=' in rest and 'to' in rest.lower()):
                is_keyword = True
            elif first_word_lower == 'next':
                is_keyword = True
            elif first_word_lower == 'set' and '=' in rest:
                is_keyword = True
            elif first_word_lower == 'get' and len(rest.split()) <= 2:
                is_keyword = True
            elif first_word_lower in ('display', 'return', 'end'):
                is_keyword = True
            
            if is_keyword:
                issues.append(LintIssue(
                    i, LintIssue.SEVERITY_CONVENTION,
                    f"Keyword '{first_word}' should be capitalised as '{expected}'.",
                    f"Change '{first_word}' to '{expected}'."
                ))
    
    return issues


def check_let_usage(lines):
    """Check for LET which is not in the HSC spec — should be SET."""
    issues = []
    
    for i, raw_line in enumerate(lines, 1):
        line = strip_comments(raw_line)
        stripped = line.strip()
        if not stripped:
            continue
        
        # Check for LET (any case) at the start of a line followed by assignment
        match = re.match(r'^\s*(let|LET|Let)\s+\w+\s*=', raw_line, re.IGNORECASE)
        if match:
            issues.append(LintIssue(
                i, LintIssue.SEVERITY_CONVENTION,
                f"'LET' is not a valid HSC pseudocode keyword. Use 'SET' instead.",
                f"Replace '{match.group(1)}' with 'SET'."
            ))
    
    return issues


def check_named_parameters(lines):
    """Check for Python-style named parameters in function calls."""
    issues = []
    
    for i, raw_line in enumerate(lines, 1):
        line = strip_comments(raw_line)
        if not line.strip():
            continue
        
        # Look for func(name=value) patterns
        # Match word( ... word=  patterns but not inside conditions (IF x = y)
        matches = re.findall(r'\w+\s*\([^)]*\w+\s*=\s*[^=]', line)
        if matches:
            # Filter out false positives from SET x = func() patterns
            # Only flag if there's a named param inside parentheses
            paren_content = re.findall(r'\(([^)]+)\)', line)
            for content in paren_content:
                if re.search(r'\w+\s*=\s*[^=]', content):
                    issues.append(LintIssue(
                        i, LintIssue.SEVERITY_CONVENTION,
                        f"Named parameters (e.g. 'param=value') are Python syntax, not valid HSC pseudocode.",
                        f"Use positional parameters only: func(value1, value2)."
                    ))
                    break
    
    return issues


def check_dot_notation(lines):
    """Check for object.property dot notation."""
    issues = []
    
    for i, raw_line in enumerate(lines, 1):
        line = strip_comments(raw_line)
        if not line.strip():
            continue
        
        # Look for word.word patterns (but not numbers like 3.14)
        matches = re.findall(r'[a-zA-Z_]\w*\.[a-zA-Z_]\w*', line)
        if matches:
            for match in matches:
                issues.append(LintIssue(
                    i, LintIssue.SEVERITY_CONVENTION,
                    f"Dot notation '{match}' is OOP/programming syntax, not valid HSC pseudocode.",
                    f"Use array indexing (e.g. data[i]) or pass values as subroutine parameters."
                ))
    
    return issues


def check_variable_consistency(lines):
    """Check for potential variable name typos (SET x vs later reference to y)."""
    issues = []
    
    set_vars = {}  # name -> line number where first SET
    
    for i, raw_line in enumerate(lines, 1):
        line = strip_comments(raw_line)
        stripped = line.strip()
        if not stripped:
            continue
        
        # Track SET assignments
        match = re.match(r'^\s*SET\s+(\w+)\s*=', stripped)
        if match:
            var_name = match.group(1)
            if var_name not in set_vars:
                set_vars[var_name] = i
    
    # Check for near-miss variable names (Levenshtein distance 1)
    var_names = list(set_vars.keys())
    for j in range(len(var_names)):
        for k in range(j + 1, len(var_names)):
            name_a = var_names[j]
            name_b = var_names[k]
            if levenshtein_distance(name_a.lower(), name_b.lower()) == 1:
                issues.append(LintIssue(
                    set_vars[name_b], LintIssue.SEVERITY_BUG,
                    f"Variable '{name_b}' (line {set_vars[name_b]}) looks like a typo of '{name_a}' (line {set_vars[name_a]}).",
                    f"Check if these should be the same variable."
                ))
    
    return issues


def levenshtein_distance(s1, s2):
    """Calculate the Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    prev_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = prev_row[j + 1] + 1
            deletions = curr_row[j] + 1
            substitutions = prev_row[j] + (c1 != c2)
            curr_row.append(min(insertions, deletions, substitutions))
        prev_row = curr_row
    
    return prev_row[-1]


def check_if_then(lines):
    """Check that IF statements include THEN."""
    issues = []
    
    for i, raw_line in enumerate(lines, 1):
        line = strip_comments(raw_line)
        stripped = line.strip()
        if not stripped:
            continue
        
        # Check for IF without THEN (case-insensitive check for 'then')
        if re.match(r'^\s*IF\b', stripped):
            if 'THEN' not in stripped:
                # Check if lowercase 'then' is present
                if re.search(r'\bthen\b', stripped, re.IGNORECASE):
                    issues.append(LintIssue(
                        i, LintIssue.SEVERITY_CONVENTION,
                        f"'then' should be capitalised as 'THEN'.",
                        f"Change 'then' to 'THEN' — keywords must be in capitals."
                    ))
                else:
                    issues.append(LintIssue(
                        i, LintIssue.SEVERITY_CONVENTION,
                        f"IF statement is missing 'THEN'.",
                        f"HSC pseudocode requires: IF condition THEN"
                    ))
        
        # Also check for ELSEIF without THEN
        if re.match(r'^\s*ELSEIF\b', stripped):
            if 'THEN' not in stripped:
                if re.search(r'\bthen\b', stripped, re.IGNORECASE):
                    issues.append(LintIssue(
                        i, LintIssue.SEVERITY_CONVENTION,
                        f"'then' should be capitalised as 'THEN'.",
                        f"Change 'then' to 'THEN' — keywords must be in capitals."
                    ))
                else:
                    issues.append(LintIssue(
                        i, LintIssue.SEVERITY_CONVENTION,
                        f"ELSEIF statement is missing 'THEN'.",
                        f"HSC pseudocode requires: ELSEIF condition THEN"
                    ))
    
    return issues


def check_inline_keyword_caps(lines):
    """Check that inline keywords like TO, STEP, AND, OR, NOT are capitalised."""
    issues = []
    
    for i, raw_line in enumerate(lines, 1):
        line = strip_comments(raw_line)
        stripped = line.strip()
        if not stripped:
            continue
        
        # Check FOR lines for lowercase 'to' and 'step'
        if re.match(r'^\s*FOR\b', stripped):
            # Look for ' to ' (word boundary) that should be ' TO '
            if re.search(r'\bto\b', stripped) and not re.search(r'\bTO\b', stripped):
                issues.append(LintIssue(
                    i, LintIssue.SEVERITY_CONVENTION,
                    f"'to' should be capitalised as 'TO' in FOR loop.",
                    f"HSC pseudocode requires: FOR variable = start TO finish"
                ))
            if re.search(r'\bstep\b', stripped, re.IGNORECASE) and not re.search(r'\bSTEP\b', stripped):
                issues.append(LintIssue(
                    i, LintIssue.SEVERITY_CONVENTION,
                    f"'step' should be capitalised as 'STEP' in FOR loop.",
                    f"HSC pseudocode requires: FOR variable = start TO finish STEP increment"
                ))
    
    return issues


def check_indentation(lines):
    """Check that code inside control structures is indented."""
    issues = []
    
    # Track nesting depth
    depth = 0
    openers = {'BEGIN', 'IF', 'WHILE', 'FOR', 'REPEAT', 'CASEWHERE'}
    # ELSE/ELSEIF are at the same level as IF, not deeper
    same_level = {'ELSE', 'ELSEIF', 'OTHERWISE'}
    closers = {'END', 'ENDIF', 'ENDWHILE', 'NEXT', 'UNTIL'}
    
    for i, raw_line in enumerate(lines, 1):
        line = strip_comments(raw_line)
        stripped = line.strip()
        if not stripped:
            continue
        
        first_word = stripped.split()[0] if stripped.split() else ""
        
        # Check for END CASE specifically
        if stripped.startswith('END CASE'):
            first_word = 'END CASE'
        
        # Determine expected indent level
        if first_word in closers or first_word == 'END CASE':
            depth = max(0, depth - 1)
        elif first_word in same_level:
            pass  # stays at current depth
        
        # Check actual indentation
        if depth > 0:
            actual_indent = len(raw_line) - len(raw_line.lstrip())
            if actual_indent == 0 and first_word not in closers and first_word != 'END CASE' and first_word not in same_level:
                # Only warn if it's clearly inside a block but not indented
                issues.append(LintIssue(
                    i, LintIssue.SEVERITY_READABILITY,
                    f"This line appears to be inside a control structure but is not indented.",
                    f"Indent this line to show it's inside the enclosing block."
                ))
        
        # Update depth for openers
        if first_word in openers:
            depth += 1
        elif first_word in same_level:
            pass  # depth doesn't change
    
    return issues


def check_subroutine_end_matching(lines):
    """Check that END lines match their BEGIN names and include parameters.
    
    Per the HSC course spec (pp.19-21), END lines must mirror the BEGIN line:
      BEGIN Add (x, y) -> END Add (x, y)
      BEGIN AddNumbers  -> END AddNumbers
    
    This check flags:
      - END name that doesn't match the corresponding BEGIN name
      - END line missing parameters that were present in the BEGIN line
      - END line with parameters when BEGIN had none
    """
    issues = []
    
    # Stack of (line_num, name, params_str) for BEGIN statements
    # params_str is the raw text inside parentheses, or None if no params
    begin_stack = []
    
    begin_pattern = re.compile(r'^\s*BEGIN\s+(\w+)\s*(\(([^)]*)\))?\s*$')
    end_pattern = re.compile(r'^\s*END\s+(.+)$')
    # Keywords that follow END but aren't subroutine names
    end_keywords = {'CASE'}
    
    for i, raw_line in enumerate(lines, 1):
        line = strip_comments(raw_line)
        stripped = line.strip()
        if not stripped:
            continue
        
        # Skip ENDIF, ENDWHILE etc — those are control structure closers, not subroutine ENDs
        if re.match(r'^\s*(ENDIF|ENDWHILE)\b', stripped):
            continue
        
        # Check for BEGIN with a name
        begin_match = begin_pattern.match(stripped)
        if begin_match:
            name = begin_match.group(1)
            params_str = begin_match.group(3)  # None if no parens, "" if empty parens
            begin_stack.append((i, name, params_str))
            continue
        
        # Check for bare BEGIN (no name — mainline)
        if re.match(r'^\s*BEGIN\s*$', stripped):
            begin_stack.append((i, None, None))
            continue
        
        # Check for END
        if re.match(r'^\s*END\b', stripped):
            # Skip END CASE
            if stripped.startswith('END CASE'):
                continue
            
            end_match = end_pattern.match(stripped)
            
            if not begin_stack:
                continue  # structural pair checker handles unmatched ENDs
            
            begin_line, begin_name, begin_params = begin_stack.pop()
            
            # Bare END — matches bare BEGIN (mainline) or named BEGIN without issue
            if stripped.strip() == 'END':
                if begin_name is not None and begin_params is not None:
                    # Named BEGIN with params, but bare END
                    issues.append(LintIssue(
                        i, LintIssue.SEVERITY_CONVENTION,
                        f"END on line {i} should include the subroutine name and parameters to match 'BEGIN {begin_name} ({begin_params})' on line {begin_line}.",
                        f"Change to: END {begin_name} ({begin_params})"
                    ))
                elif begin_name is not None:
                    # Named BEGIN without params, but bare END
                    issues.append(LintIssue(
                        i, LintIssue.SEVERITY_CONVENTION,
                        f"END on line {i} should include the subroutine name to match 'BEGIN {begin_name}' on line {begin_line}.",
                        f"Change to: END {begin_name}"
                    ))
                continue
            
            if not end_match:
                continue
            
            end_rest = end_match.group(1).strip()
            
            # Parse the END line for name and optional params
            end_name_match = re.match(r'(\w+)\s*(\(([^)]*)\))?\s*$', end_rest)
            if not end_name_match:
                continue
            
            end_name = end_name_match.group(1)
            end_params = end_name_match.group(3)
            
            # Check name matches
            if begin_name is not None and end_name != begin_name:
                expected = f"END {begin_name}"
                if begin_params is not None:
                    expected += f" ({begin_params})"
                issues.append(LintIssue(
                    i, LintIssue.SEVERITY_CONVENTION,
                    f"END name '{end_name}' on line {i} doesn't match BEGIN name '{begin_name}' on line {begin_line}.",
                    f"Change to: {expected}"
                ))
            
            # Check params match (only if name was correct or close enough to be worth checking)
            if begin_name is not None and end_name == begin_name:
                if begin_params is not None and end_params is None:
                    issues.append(LintIssue(
                        i, LintIssue.SEVERITY_CONVENTION,
                        f"END line is missing parameters. The spec requires END to mirror BEGIN.",
                        f"Change to: END {begin_name} ({begin_params})"
                    ))
                elif begin_params is None and end_params is not None:
                    issues.append(LintIssue(
                        i, LintIssue.SEVERITY_CONVENTION,
                        f"END line has parameters but BEGIN on line {begin_line} has none.",
                        f"Change to: END {begin_name}"
                    ))
    
    return issues


def lint_pseudocode(text):
    """
    Run all linting checks on the given pseudocode text.
    Returns a list of LintIssue objects.
    """
    lines = text.split('\n')
    
    all_issues = []
    all_issues.extend(check_structural_pairs(lines))
    all_issues.extend(check_keyword_capitalisation(lines))
    all_issues.extend(check_let_usage(lines))
    all_issues.extend(check_named_parameters(lines))
    all_issues.extend(check_dot_notation(lines))
    all_issues.extend(check_if_then(lines))
    all_issues.extend(check_inline_keyword_caps(lines))
    all_issues.extend(check_variable_consistency(lines))
    all_issues.extend(check_indentation(lines))
    all_issues.extend(check_subroutine_end_matching(lines))
    
    # Sort by line number
    all_issues.sort(key=lambda x: (x.line_num or 0, x.severity))
    
    return all_issues


def format_results(issues, source_name="input"):
    """Format linting results as a readable report."""
    if not issues:
        return f"✅ {source_name}: No issues found! Pseudocode follows HSC conventions."
    
    # Count by severity
    bugs = sum(1 for i in issues if i.severity == LintIssue.SEVERITY_BUG)
    conventions = sum(1 for i in issues if i.severity == LintIssue.SEVERITY_CONVENTION)
    readability = sum(1 for i in issues if i.severity == LintIssue.SEVERITY_READABILITY)
    
    header = f"{'=' * 60}\n"
    header += f"HSC Pseudocode Lint: {source_name}\n"
    header += f"{'=' * 60}\n"
    header += f"Found {len(issues)} issue(s): "
    parts = []
    if bugs:
        parts.append(f"{bugs} bug(s)")
    if conventions:
        parts.append(f"{conventions} convention violation(s)")
    if readability:
        parts.append(f"{readability} readability issue(s)")
    header += ", ".join(parts) + "\n"
    header += f"{'-' * 60}\n"
    
    body = "\n".join(str(issue) for issue in issues)
    
    return header + body


def main():
    parser = argparse.ArgumentParser(description="HSC Pseudocode Linter")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("file", nargs="?", help="Path to pseudocode file")
    group.add_argument("--text", help="Pseudocode text to lint (use \\n for newlines)")
    
    args = parser.parse_args()
    
    if args.text:
        text = args.text.replace("\\n", "\n")
        source = "inline"
    else:
        try:
            with open(args.file, 'r') as f:
                text = f.read()
            source = args.file
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.")
            sys.exit(1)
    
    issues = lint_pseudocode(text)
    print(format_results(issues, source))
    
    # Exit with error code if there are bugs or convention issues
    if any(i.severity in (LintIssue.SEVERITY_BUG, LintIssue.SEVERITY_CONVENTION) for i in issues):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
