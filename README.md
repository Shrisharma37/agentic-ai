# JavaGuard AI — Java Code Analysis Assistant

JavaGuard AI is a Python-based Java code analysis tool designed to identify common coding issues, check Java compilation, and generate structured analysis reports.

The project combines rule-based checks, the Java compiler, and PMD to help developers review their Java source code.

## Features

- **Basic static analysis:** Detects selected suspicious coding patterns, including String comparisons using `==`, empty exception handlers, explicit `null` assignments, and unfinished TODO comments.
- **Compilation checks:** Uses `javac` to identify Java compilation errors and warnings.
- **Code quality analysis:** Integrates PMD for additional Java code-quality checks.
- **Automated reports:** Generates Markdown reports containing analysis results.
- **Modular architecture:** Separates analysis tools, services, agents, and tests.
- **AI integration foundation:** Includes a CrewAI agent module for future AI-assisted code reviews.

## Technology Stack

- Python
- Java and `javac`
- PMD
- CrewAI
- python-dotenv
- Python unittest

## Project Structure

```text
JavaGuardAI/
├── agents/
│   └── java_crew.py
├── input/
│   └── Main.java
├── reports/
├── services/
│   ├── analyzer.py
│   └── reporter.py
├── tests/
│   └── test_java_tools.py
├── tools/
│   └── java_tools.py
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Getting Started

### 1. Install Python dependencies

```bash
python -m pip install -r requirements.txt
```

### 2. Install a Java Development Kit

Ensure that `java` and `javac` are available from your terminal.

### 3. Install PMD

Download the PMD binary distribution from the official releases page:

https://github.com/pmd/pmd/releases

Configure the PMD executable path in `services/analyzer.py` to match your installation.

### 4. Add Java code

Place the Java source file you want to analyze in the `input/` directory.

### 5. Run JavaGuard AI

```bash
python main.py
```

Enter the Java filename when prompted, for example:

```text
Main.java
```

### 6. View the report

Generated Markdown reports are saved in the `reports/` directory.

## Run Tests

```bash
python -m unittest discover -s tests -v
```

## Current Limitations

- Basic pattern checks do not understand every aspect of Java syntax or program behavior.
- Successful compilation does not guarantee logical correctness.
- PMD must be installed and configured correctly.
- AI-assisted review requires a configured model and may not be available when offline.
- Findings should be reviewed and tested before making changes to source code.

## Future Improvements

- Improve PMD integration and error handling.
- Add more automated tests.
- Integrate a suitable local or hosted AI model.
- Provide clearer explanations and suggested fixes.
- Add support for analyzing multiple Java files.

## Project Goal

The goal of JavaGuard AI is to make Java code review more accessible by combining traditional static analysis with AI-assisted explanations in a modular, extensible application.
# agentic-ai
working on creating agentic ai using langchain
