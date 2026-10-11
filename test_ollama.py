
from crewai import LLM

def main():
    print("Testing JavaGuard AI local model connection...")

    llm = LLM(
        model="ollama/qwen2.5-coder:3b",
        base_url="http://localhost:11434",
        temperature=0.2,
    )

    response = llm.call(
        messages=[
            {
                "role": "user",
                "content": (
                    "In one sentence, explain why Java String values "
                    "should usually be compared with .equals() instead of ==."
                ),
            }
        ]
    )

    print("\nModel response:")
    print(response)
    print("\nLocal model connection test completed.")


if __name__ == "__main__":
    main()
