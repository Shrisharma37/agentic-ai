
from pathlib import Path

from services.analyzer import analyze_java_file
from services.reporter import save_report


BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"


def main():
    INPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 50)
    print("                 JavaGuard AI")
    print("       AI-Powered Java Code Review Assistant")
    print("=" * 50)

    file_name = input(
        "\nEnter Java filename (e.g. Main.java): "
    ).strip()

    # Validate the filename
    if (
        not file_name
        or Path(file_name).name != file_name
        or not file_name.lower().endswith(".java")
    ):
        print("Input error: Enter a valid Java filename, such as Main.java.")
        return

    java_file = INPUT_DIR / file_name

    if not java_file.is_file():
        print(f"Input error: File not found: {java_file}")
        print("Place your Java source file inside the input folder.")
        return

    # Stage 1: Local analysis
    print("\n[1/3] Running local analysis...")

    try:
        analysis = analyze_java_file(str(java_file))

        print("Compiler status:", analysis.get("compiler_status", "unknown"))

        print("\nBasic static checks:")
        for finding in analysis.get("static_findings", []):
            print("-", finding)

        print("\nPMD status:", analysis.get("pmd_status", "not_run"))

        pmd_output = analysis.get("pmd_output", "")
        if pmd_output:
            print(pmd_output)

    except (FileNotFoundError, ValueError, UnicodeError) as exc:
        print(f"\nInput error: {exc}")
        return

    except Exception as exc:
        print(
            f"\nLocal analysis failed: "
            f"{type(exc).__name__}: {exc}"
        )
        return

    # Stage 2: AI review using local Ollama
    print("\n[2/3] Running AI code review...")
    ai_review = "AI review was not completed."

    try:
        # Import only when the AI review is needed.
        from agents.java_crew import create_java_crew

        crew = create_java_crew()
        result = crew.kickoff(
            inputs={"java_code": analysis["code"]}
        )

        ai_review = getattr(result, "raw", None) or str(result)

        print("\nAI review completed.")
        print(ai_review)

    except Exception as exc:
        ai_review = (
            "AI review could not be completed.\n"
            f"Error type: {type(exc).__name__}\n"
            f"Details: {exc}"
        )

        print(
            f"\nAI review failed: {type(exc).__name__}: {exc}"
        )
        print("Continuing with local analysis results.")

    # Stage 3: Generate the report
    print("\n[3/3] Generating report...")

    try:
        report_path = save_report(
            file_name=analysis.get("file_name", file_name),
            compiler_status=analysis.get("compiler_status", "unknown"),
            compiler_output=analysis.get("compiler_output", ""),
            static_findings=analysis.get("static_findings", []),
            pmd_status=analysis.get("pmd_status", "not_run"),
            pmd_output=analysis.get("pmd_output", ""),
            ai_review=ai_review,
        )

        print("\nAnalysis finished.")
        print(f"Report saved to: {report_path}")

    except OSError as exc:
        print(f"\nCould not save the report: {exc}")


if __name__ == "__main__":
    main()