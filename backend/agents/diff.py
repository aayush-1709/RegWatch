from typing import Any

from services.gemini import call_gemini


def generate_policy_diff(old_policy: str, new_policy: str) -> dict[str, Any]:
    """
    Generate a structured policy diff.

    Returns JSON-like dict:
      - added_lines: list[str]
      - removed_lines: list[str]
      - modified_lines: list[str]
    """
    prompt = (
        "You are a policy diff engine.\n"
        "Given an old policy and a new policy, compute differences.\n\n"
        "Return ONLY valid JSON with exactly these keys:\n"
        "{\n"
        '  "added_lines": string[],\n'
        '  "removed_lines": string[],\n'
        '  "modified_lines": string[]\n'
        "}\n\n"
        "Rules:\n"
        "- No markdown\n"
        "- No extra keys\n"
        '- modified_lines should be strings like "OLD: ... -> NEW: ..." when line text changes.\n\n'
        f"OLD_POLICY:\n{old_policy}\n\nNEW_POLICY:\n{new_policy}"
    )

    result = call_gemini(prompt)
    if not result or "error" in result:
        return _fallback_diff(old_policy, new_policy)

    try:
        added = result.get("added_lines") or result.get("additions") or []
        removed = result.get("removed_lines") or result.get("removals") or []
        modified = result.get("modified_lines") or []  # keep key consistent with prompt

        if not isinstance(added, list):
            added = [str(added)]
        if not isinstance(removed, list):
            removed = [str(removed)]
        if not isinstance(modified, list):
            modified = [str(modified)]

        return {
            "added_lines": [str(x).strip() for x in added if str(x).strip()],
            "removed_lines": [str(x).strip() for x in removed if str(x).strip()],
            "modified_lines": [str(x).strip() for x in modified if str(x).strip()],
        }
    except Exception:
        return _fallback_diff(old_policy, new_policy)


def _fallback_diff(old_policy: str, new_policy: str) -> dict[str, Any]:
    old_lines = [ln.strip() for ln in (old_policy or "").splitlines() if ln.strip()]
    new_lines = [ln.strip() for ln in (new_policy or "").splitlines() if ln.strip()]

    old_set = set(old_lines)
    new_set = set(new_lines)

    added = [ln for ln in new_lines if ln not in old_set]
    removed = [ln for ln in old_lines if ln not in new_set]

    modified: list[str] = []
    # Heuristic: same index changed (only if line counts overlap)
    for i in range(min(len(old_lines), len(new_lines))):
        if old_lines[i] != new_lines[i] and old_lines[i] in old_set and new_lines[i] in new_set:
            modified.append(f"OLD: {old_lines[i]} -> NEW: {new_lines[i]}")

    return {
        "added_lines": added,
        "removed_lines": removed,
        "modified_lines": modified,
    }


class PolicyDiffAgent:
    def run(self, old_policy: str, new_policy: str) -> dict:
        return generate_policy_diff(old_policy, new_policy)
