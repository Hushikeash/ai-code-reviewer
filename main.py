import sys
from reviewer.llm_reviewer import review_code

def main():
    # Read diff from a file or stdin
    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], "r") as f:
            diff_text = f.read()
    else:
        # Read from stdin
        print("Paste your git diff below (Ctrl+Z then Enter to finish):")
        diff_text = sys.stdin.read()

    print("\n🔍 Reviewing your code...\n")
    review = review_code(diff_text)
    print("=" * 60)
    print("📋 CODE REVIEW RESULTS")
    print("=" * 60)
    print(review)
    print("=" * 60)

if __name__ == "__main__":
    main()