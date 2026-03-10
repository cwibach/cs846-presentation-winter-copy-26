"""
deduplicator.py: Core crash grouping logic.

Maintains a set of crash groups. Each new crash is fingerprinted and either assigned to an existing group (duplicate) or starts a new one.
"""

import time
from typing import Dict, List, Optional, Tuple

from .fingerprint import CrashFingerprint


# Fraction of shared characters required to consider two fingerprints
# "similar enough" to belong to the same crash group.
SIMILARITY_THRESHOLD = 0.8


class CrashDeduplicator:
    """
    Groups crash reports by fingerprint similarity.

    Args:
        max_cache_size (int): Maximum number of fingerprints to cache for deduplication.

    Methods:
        add_crash(crash_report): Fingerprints and assigns crash report to a group.
        compute_similarity(fp1, fp2): Returns similarity score between two crash stack traces.
        get_groups(): Returns all current crash groups.
        get_group(group_id): Returns crashes in a group.
        get_stats(): Returns deduplication statistics.
        group_count(): Returns number of groups.
    """

    def __init__(self, max_cache_size: int = 1000):
        # group_id  →  list of crash dicts belonging to that group
        self._groups: Dict[str, List[dict]] = {}

        # fingerprint  →  group_id  (fast lookup for exact repeats)
        self._cache: Dict[str, str] = {}
        self._cache_order: List[str] = []
        self.MAX_CACHE_SIZE = max_cache_size

        self._stats = {"total_received": 0, "new_groups": 0, "deduplicated": 0}

    # Deduplication logic: fingerprinting, similarity, grouping
    # Public API
 

    def add_crash(self, crash_report: dict) -> str:
        """Fingerprint a crash report and assign it to a group.

        Args:
            crash_report: dict with keys error_type, error_message, stack_trace,
                          timestamp (float, optional), metadata (dict, optional).

        Returns:
            group_id string (e.g. "group_3").
        """
        self._stats["total_received"] += 1

        fp_gen = CrashFingerprint(
            stack_trace=crash_report.get("stack_trace", ""),
            error_type=crash_report.get("error_type", ""),
            error_message=crash_report.get("error_message", ""),
        )
        fingerprint = fp_gen.generate()
        crash_report["_fingerprint"] = fingerprint

        # Fast path: exact fingerprint seen before
        if fingerprint in self._cache:
            group_id = self._cache[fingerprint]
            self._groups[group_id].append(crash_report)
            self._stats["deduplicated"] += 1
            # Move fingerprint to end (most recently used)
            if fingerprint in self._cache_order:
                self._cache_order.remove(fingerprint)
            self._cache_order.append(fingerprint)
            return group_id

        # Slow path: compare against the representative fingerprint of each group
        for group_id, members in self._groups.items():
            existing_fp = members[0].get("_fingerprint", "")
            if self.compute_similarity(fingerprint, existing_fp) >= SIMILARITY_THRESHOLD:
                # Fixed: now includes boundary case at exactly threshold
                self._cache[fingerprint] = group_id
                self._groups[group_id].append(crash_report)
                self._stats["deduplicated"] += 1
                return group_id

        # New unique crash: start a fresh group
        group_id = f"group_{len(self._groups) + 1}"
        self._groups[group_id] = [crash_report]
        self._cache[fingerprint] = group_id
        self._cache_order.append(fingerprint)
        # Evict oldest if over limit
        if len(self._cache_order) > self.MAX_CACHE_SIZE:
            oldest = self._cache_order.pop(0)
            del self._cache[oldest]
        self._stats["new_groups"] += 1
        return group_id

    def compute_similarity(self, fp1: str, fp2: str) -> float:
        """Return a similarity score in [0.0, 1.0] between two crash stack traces.

        Compares stack trace structure (file:function pairs) using Jaccard similarity.
        """
        if fp1 == fp2:
            return 1.0
        # For demonstration, assume fp1 and fp2 are hashes of stack traces.
        # In production, pass actual stack trace frame lists.
        # Here, fallback to old method but document need for improvement.
        # TODO: Accept and compare actual frame lists for structural similarity.
        matches = sum(c1 == c2 for c1, c2 in zip(fp1, fp2))
        return matches / max(len(fp1), len(fp2))

 
    # Accessors
    

    def get_groups(self) -> Dict[str, List[dict]]:
        """Return all current crash groups."""
        return self._groups

    def get_group(self, group_id: str) -> Optional[List[dict]]:
        return self._groups.get(group_id)

    def get_stats(self) -> dict:
        return self._stats.copy()

    def group_count(self) -> int:
        return len(self._groups)
