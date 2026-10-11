
import unittest

from tools.java_tools import detect_common_issues


class TestJavaTools(unittest.TestCase):
    """Tests for JavaGuard AI's basic static checks."""

    def test_detects_string_comparison(self):
        code = '''
        class Main {
            void check() {
                String name = "Java";
                if (name == "Java") {
                    System.out.println(name);
                }
            }
        }
        '''

        findings = detect_common_issues(code)

        self.assertTrue(
            any("String comparison" in item for item in findings)
        )

    def test_detects_empty_catch_block(self):
        code = '''
        class Main {
            void check() {
                try {
                    int number = 10 / 2;
                } catch (Exception e) {
                }
            }
        }
        '''

        findings = detect_common_issues(code)

        self.assertTrue(
            any("empty catch block" in item.lower() for item in findings)
        )

    def test_detects_null_assignment(self):
        code = '''
        class Main {
            void check() {
                String name = null;
                System.out.println(name);
            }
        }
        '''

        findings = detect_common_issues(code)

        self.assertTrue(
            any("assigned null" in item.lower() for item in findings)
        )

    def test_detects_todo(self):
        code = '''
        class Main {
            // TODO: finish this method
            void check() {
                System.out.println("Hello");
            }
        }
        '''

        findings = detect_common_issues(code)

        self.assertTrue(
            any("TODO" in item for item in findings)
        )

    def test_detects_multiple_issues(self):
        code = '''
        class Main {
            void check() {
                String name = null;

                if (name == "Java") {
                    System.out.println(name);
                }

                try {
                    System.out.println("Test");
                } catch (Exception e) {
                }
            }
        }
        '''

        findings = detect_common_issues(code)

        self.assertTrue(
            any("String comparison" in item for item in findings)
        )
        self.assertTrue(
            any("empty catch block" in item.lower() for item in findings)
        )
        self.assertTrue(
            any("assigned null" in item.lower() for item in findings)
        )

    def test_returns_fallback_when_no_checks_match(self):
        code = '''
        class Main {
            int add(int a, int b) {
                return a + b;
            }
        }
        '''

        findings = detect_common_issues(code)

        self.assertTrue(findings)
        self.assertTrue(
            any("No issues were detected" in item for item in findings)
        )

    def test_empty_source_returns_fallback(self):
        findings = detect_common_issues("")

        self.assertTrue(findings)
        self.assertTrue(
            any("No issues were detected" in item for item in findings)
        )


if __name__ == "__main__":
    unittest.main()
