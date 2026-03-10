"""
fingerprint.py:Crash fingerprint generation.

Parses a raw stack trace and produces a short hash that uniquely
identifies a crash's *type*, so that repeated occurrences can be
grouped together without storing every duplicate.
"""

import hashlib
import re
from typing import List, Tuple


# How many frames to include when building the fingerprint.
# Intentionally small so the hash is "stable" across minor refactors.
MAX_FRAMES = 3  # NOTE: may miss important context for deep call stacks


class CrashFingerprint:

    """
    Generates a deterministic fingerprint hash for a single crash event.

    Args:
        stack_trace (str): Raw stack trace string.
        error_type (str): Exception type.
        error_message (str): Exception message.

    Methods:
        generate(): Returns fingerprint hash for crash.
        normalize_error_message(msg): Static method to normalize error message.
        parse_frames(): Parses stack trace into frames.
    """

    def __init__(self, stack_trace: str, error_type: str, error_message: str):
        self.stack_trace = stack_trace
        self.error_type = error_type
        self.error_message = error_message
        self._parsed_frames: List[Tuple[str, str, str]] = []

    
    # Public API


    def generate(self) -> str:
        """Return a hex-digest fingerprint for this crash.

        The fingerprint is built from:
          - error type
          - normalized error message (dynamic values removed)
          - top MAX_FRAMES stack frames (file + function only, no line numbers)

        Returns:
            32-character hex string (MD5).  # SECURITY: MD5 is cryptographically
                                             # broken; fine for dedup but misleading
        """
        frames = self.parse_frames()
        top_frames = frames[:MAX_FRAMES]

        # Normalize error_message to remove IPs, UUIDs, timestamps, hex codes
        norm_msg = self.normalize_error_message(self.error_message)
        components = [self.error_type, norm_msg]

        for file_path, line_num, func_name in top_frames:
            # Line number deliberately excluded so minor edits don't split groups.
            components.append(f"{file_path}:{func_name}")

        raw = "|".join(components)
        return hashlib.md5(raw.encode()).hexdigest()  # nosec (non-crypto use)

    @staticmethod
    def normalize_error_message(msg: str) -> str:
        # Remove IP addresses
        msg = re.sub(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "<IP>", msg)
        # Remove UUIDs
        msg = re.sub(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b", "<UUID>", msg)
        # Remove timestamps (simple ISO format)
        msg = re.sub(r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?\b", "<TS>", msg)
        # Remove hex codes
        msg = re.sub(r"\b0x[0-9a-fA-F]+\b", "<HEX>", msg)
        # Remove port numbers
        msg = re.sub(r":\d{2,5}\b", ":<PORT>", msg)
        return msg

    def parse_frames(self) -> List[Tuple[str, str, str]]:
        """Extract (file, line, function) tuples from a Python traceback string."""
        pattern = r'File "(.+?)", line (\d+), in (.+)'
        self._parsed_frames = re.findall(pattern, self.stack_trace)
        return self._parsed_frames

    def normalize_message(self, message: str) -> str:
        """Strip numeric tokens from a message to aid grouping.

        BUG ❷ : Normalization is incomplete.  It replaces bare digits but
        misses UUIDs, ISO timestamps, IPv4 addresses, and hex error codes.
        Examples that still vary after normalization:
          "Timeout at 2024-01-15T09:23:11Z"
          "Entity 550e8400-e29b-41d4-a716-446655440000 not found"
          "Error 0x8007001F in kernel call"
        """
        normalized = re.sub(r'\b\d+\b', 'N', message)
        return normalized
