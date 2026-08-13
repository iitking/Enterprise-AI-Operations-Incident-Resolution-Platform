"""
OpsPilot AI - Prompt Injection & Adversarial Defense Guard
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

import re
from typing import Tuple, List

# Suspicious phrases commonly used in LLM jailbreaks and prompt injections
INJECTION_SIGNATURES: List[str] = [
    r"ignore (all )?previous instructions",
    r"disregard all previous (commands|rules)",
    r"you are now a (dan|jailbroken|unrestricted)",
    r"reveal (your |the )?(system prompt|instructions)",
    r"drop table|truncate table|delete from users",
    r"rm -rf /|chmod 777",
    r"bypass security|override approval",
    r"elevate privileges to admin",
    r"pretend you have no safety rules"
]

COMPILED_SIGNATURES = [re.compile(pattern, re.IGNORECASE) for pattern in INJECTION_SIGNATURES]

def inspect_for_prompt_injection(prompt: str) -> Tuple[bool, str]:
    """
    Scans incoming prompt or log string for prompt injection attempts.
    Returns: (is_suspicious: bool, flag_reason: str)
    """
    if not prompt or not isinstance(prompt, str):
        return False, "Clean"

    for pattern in COMPILED_SIGNATURES:
        if pattern.search(prompt):
            return True, f"Suspicious prompt injection signature matched: {pattern.pattern}"

    return False, "Clean"

def sanitize_agent_input(text: str) -> str:
    """Sanitizes text and warns if injection was detected."""
    is_suspicious, reason = inspect_for_prompt_injection(text)
    if is_suspicious:
        # Wrap safely to disarm instructions
        return f"[SECURITY WARNING: Untrusted content flagged - {reason}]\nSafe Content: {text[:200]}..."
    return text
