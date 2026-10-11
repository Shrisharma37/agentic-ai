
import re


def detect_common_issues(code: str) -> list[str]:
    """Detect common Java code concerns using lightweight text checks."""

    issues = []

    # 1. Check for console output.
    # This is informational, not necessarily a defect.
    if (
        "System.out.println(" not in code
        and "System.out.print(" not in code
        and re.search(r"\bclass\s+\w+", code)
    ):
        issues.append(
            "No console output statement found. "
            "This may be intentional."
        )

    # 2. Check for possible String comparison using ==.
    # This is a heuristic and may need human verification.
    if re.search(r'==\s*(?:"[^"]*"|\'[^\']*\'|[A-Za-z_$][\w$]*)', code):
        issues.append(
            "Possible String comparison using ==. "
            "Use .equals() when comparing String contents."
        )
    

    # 3. Check for empty catch blocks.
    if re.search(
        r"catch\s*\([^)]*\)\s*\{\s*\}",
        code,
    ):
        issues.append(
            "An empty catch block was found. "
            "Check whether the exception is being silently ignored."
        )

    # 4. Check for explicit null assignments.
    if re.search(r'=\s*null\s*;', code):
        issues.append(
            "A variable is explicitly assigned null. "
            "Check whether this could lead to a NullPointerException."
        )

    # 5. Check for unfinished TODO markers.
    if re.search(r"\bTODO\b", code):
        issues.append(
            "A TODO marker remains in the source code."
        )

    # 6. Return a useful fallback if no checks matched.
    if not issues:
        issues.append(
            "No issues were detected by the basic text checks. "
            "This does not prove the code is correct."
        )

    return issues
