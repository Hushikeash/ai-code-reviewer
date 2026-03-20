def parse_diff(diff_text: str) -> list[dict]:
    """
    Parses a git diff and returns a list of changed files with their changes.
    """
    files = []
    current_file = None

    for line in diff_text.splitlines():
        # Detect new file in diff
        if line.startswith("diff --git"):
            if current_file:
                files.append(current_file)
            current_file = {"filename": "", "changes": []}

        # Get the filename
        elif line.startswith("+++ b/") and current_file is not None:
            current_file["filename"] = line[6:]

        # Capture added/removed lines only
        elif current_file is not None:
            if line.startswith("+") and not line.startswith("+++"):
                current_file["changes"].append(("added", line[1:]))
            elif line.startswith("-") and not line.startswith("---"):
                current_file["changes"].append(("removed", line[1:]))

    # Don't forget the last file
    if current_file:
        files.append(current_file)

    return files