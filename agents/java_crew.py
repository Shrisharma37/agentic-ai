
from crewai import Agent, Crew, Process, Task, LLM


def create_java_crew():
    """Create a lightweight Java code-review workflow using Ollama."""

    local_llm = LLM(
        model="ollama/qwen2.5-coder:3b",
        base_url="http://localhost:11434",
        temperature=0.1,
    )

    java_reviewer = Agent(
        role="Java Code Review Specialist",
        goal=(
            "Identify actionable Java code issues, explain their impact, "
            "and recommend practical fixes supported by source evidence."
        ),
        backstory=(
            "You are a careful Java reviewer. You distinguish definite "
            "errors from potential risks, avoid inventing findings, and "
            "prioritize correctness, readability, and maintainability."
        ),
        llm=local_llm,
        verbose=False,
        allow_delegation=False,
        max_iter=1,
    )

    review_task = Task(
        description="""
Review the Java source code provided below.

JAVA SOURCE CODE:
```java
{java_code}
```

REVIEW RULES:
1. Identify actionable issues supported by the supplied code.
2. Assign each finding a severity: High, Medium, or Low.
3. Quote the relevant code expression or name the affected method.
4. Explain why the issue matters and suggest a practical fix.
5. Distinguish definite defects from possible risks.
6. Do not invent line numbers, APIs, execution results, or findings.
7. Do not claim that you compiled or executed the code.
8. If no actionable issues are found, say so explicitly.
9. Keep the review concise and avoid repeating the same issue.

Use this output structure:

## Summary
Briefly describe the overall code quality.

## Findings
For each issue:
- Severity
- Evidence
- Explanation
- Suggested fix

If no issues are found, state that clearly.

## Positive Observations
Mention useful practices in the code, if any.

## Limitations
Explain what cannot be concluded from a source-only review.
""",
        expected_output=(
            "A structured, concise Java code review containing a summary, "
            "evidence-based findings, severity levels, practical fixes, "
            "positive observations, and limitations."
        ),
        agent=java_reviewer,
    )

    return Crew(
        agents=[java_reviewer],
        tasks=[review_task],
        process=Process.sequential,
        verbose=False,
    )
