
import shutil
import subprocess
import tempfile
from pathlib import Path

from tools.java_tools import detect_common_issues


# Update this path if PMD is installed somewhere else.
PMD_PATH = Path(
    r"C:\Users\Technical Solution\Downloads\pmd-dist-7.28.0-bin"
    r"\pmd-bin-7.28.0\bin\pmd.bat"
)

MAX_FILE_SIZE = 500_000
COMPILER_TIMEOUT = 20
PMD_TIMEOUT = 60


def analyze_java_file(file_path: str) -> dict:
    """Analyze Java code using local checks, javac, and PMD."""

    path = Path(file_path).resolve()

    if not path.is_file():
        raise FileNotFoundError(f"Java file not found: {path}")

    if path.suffix.lower() != ".java":
        raise ValueError("Please provide a .java file.")

    if path.stat().st_size > MAX_FILE_SIZE:
        raise ValueError("Java file is too large. Maximum size is 500 KB.")

    code = path.read_text(encoding="utf-8")

    result = {
        "file_name": path.name,
        "code": code,
        "static_findings": detect_common_issues(code),
        "compiler_output": "",
        "compiler_status": "not_run",
        "pmd_output": "",
        "pmd_status": "not_run",
    }

    # Stage 1: Compile Java without executing the program.
    javac = shutil.which("javac")

    if not javac:
        result["compiler_status"] = "JDK_NOT_FOUND"
        result["compiler_output"] = (
            "javac was not found. Install a JDK and configure PATH."
        )
    else:
        try:
            with tempfile.TemporaryDirectory(
                prefix="javaguard_"
            ) as temp_dir:
                completed = subprocess.run(
                    [
                        javac,
                        "-proc:none",
                        "-Xlint:all",
                        "-d",
                        temp_dir,
                        str(path),
                    ],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=COMPILER_TIMEOUT,
                    check=False,
                )

                result["compiler_status"] = (
                    "passed"
                    if completed.returncode == 0
                    else "failed"
                )

                result["compiler_output"] = (
                    completed.stdout + completed.stderr
                ).strip() or "No compiler diagnostics."

        except subprocess.TimeoutExpired:
            result["compiler_status"] = "timeout"
            result["compiler_output"] = (
                f"Compilation exceeded {COMPILER_TIMEOUT} seconds."
            )
        except OSError as exc:
            result["compiler_status"] = "error"
            result["compiler_output"] = str(exc)

    # Stage 2: Run PMD using a proper file list.
    if not PMD_PATH.is_file():
        result["pmd_status"] = "PMD_NOT_FOUND"
        result["pmd_output"] = (
            f"PMD executable not found: {PMD_PATH}"
        )
        return result

    try:
        with tempfile.TemporaryDirectory(
            prefix="javaguard_pmd_"
        ) as temp_dir:
            file_list = Path(temp_dir) / "files.txt"
            file_list.write_text(
                str(path) + "\n",
                encoding="utf-8",
            )

            # PMD's --file-list expects a text file containing
            # source-file paths, not the Java source file itself.
            command = (
                f'call "{PMD_PATH}" check '
                f'--file-list "{file_list}" '
                '--rulesets "rulesets/java/quickstart.xml" '
                '--format text'
            )

            completed = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=PMD_TIMEOUT,
                check=False,
            )

            output = (
                completed.stdout + completed.stderr
            ).strip()

            result["pmd_output"] = (
                output or "PMD completed without diagnostic output."
            )

            # PMD commonly uses exit code 4 when violations are found.
            if completed.returncode in (0, 4):
                result["pmd_status"] = "completed"
            else:
                result["pmd_status"] = "error"
                result["pmd_output"] += (
                    f"\nPMD exit code: {completed.returncode}"
                )

    except subprocess.TimeoutExpired:
        result["pmd_status"] = "timeout"
        result["pmd_output"] = (
            f"PMD exceeded {PMD_TIMEOUT} seconds."
        )
    except OSError as exc:
        result["pmd_status"] = "error"
        result["pmd_output"] = str(exc)

    return result