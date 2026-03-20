import anthropic
import os
from dotenv import load_dotenv
from reviewer.diff_parser import parse_diff

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def review_code(diff_text: str) -> str:
    """
    Sends the parsed diff to Claude and returns a code review.
    """
    parsed = parse_diff(diff_text)

    if not parsed:
        return "No changes found to review."

    # Build a readable summary of changes
    changes_summary = ""
    for file in parsed:
        changes_summary += f"\n### File: {file['filename']}\n"
        for change_type, line in file["changes"]:
            symbol = "+" if change_type == "added" else "-"
            changes_summary += f"{symbol} {line}\n"

    prompt = f"""You are an expert code reviewer. Review the following code changes and provide feedback on:
1. Bugs or errors
2. Security issues
3. Performance problems
4. Code quality and best practices
5. Suggestions for improvement

Be concise, specific, and constructive.

Code changes:
{changes_summary}

Provide your review in a clear, structured format."""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text