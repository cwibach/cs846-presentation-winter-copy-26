# A_1 #

==================================== short test summary info ===================================== 
FAILED tests/test_analyzer.py::test_top_crashes_respects_n - AssertionError: Each tuple should be (group_id, count, error_type)
FAILED tests/test_analyzer.py::test_generate_report_has_expected_keys - AssertionError: Missing key: generated_at
FAILED tests/test_analyzer.py::test_crash_rate_zero_window_raises_value_error - ZeroDivisionError: division by zero
FAILED tests/test_deduplicator.py::test_first_crash_creates_group - AssertionError: Crash should be stamped with processing time
FAILED tests/test_deduplicator.py::test_cache_size_is_bounded - AssertionError: assert 500 <= 100  
FAILED tests/test_fingerprint.py::test_parse_frames_count - AssertionError: Each frame should be (file, line, function, module)
FAILED tests/test_fingerprint.py::test_same_crash_different_ip_gets_same_fingerprint - AssertionError: assert 'dc27591e67b3...8ffe2c9da1c7f' == 'a8a2a536441b...dbf1f51b5b950'
FAILED tests/test_fingerprint.py::test_normalize_strips_uuid - AssertionError: assert '550e8400' not in 'Entity 550e...-N not found'
FAILED tests/test_storage.py::test_count_by_group - Failed: DID NOT RAISE <class 'KeyError'>       
FAILED tests/test_storage.py::test_sql_injection_in_search_is_blocked - AssertionError: assert 1 == 0
FAILED tests/test_storage.py::test_sql_injection_in_get_group_is_blocked - AssertionError: assert 1 == 0
================================= 11 failed, 22 passed in 1.09s ==================================

# A_2 #
# Pull Request Review: crash_dedup

## Identified Bugs and Fixes

### 1. Division by zero in analyzer.py (crash rate calculation)
**Location:** analyzer.py, get_crash_rate()
**Issue:** Division by zero if window_seconds == 0
**Why it matters:** Causes runtime error, breaks analysis pipeline
**Proposed fix:** Add guard clause to raise ValueError if window_seconds <= 0

### 2. Cache grows without bound in deduplicator.py
**Location:** deduplicator.py, CrashDeduplicator._cache
**Issue:** No eviction policy; memory leak risk in long-running processes
**Why it matters:** Unbounded memory usage, can crash server
**Proposed fix:** Implement LRU or size limit for cache

### 3. Fingerprint includes dynamic values in fingerprint.py
**Location:** fingerprint.py, CrashFingerprint.generate()
**Issue:** Includes raw error_message; dynamic values (IPs, UUIDs, timestamps) cause identical crashes to be split
**Why it matters:** Reduces deduplication accuracy
**Proposed fix:** Normalize error_message to strip dynamic values before hashing

### 4. SQL injection vulnerability in storage.py
**Location:** storage.py, CrashStorage.search_by_error_type()
**Issue:** Uses f-string for SQL query; user input can inject SQL
**Why it matters:** Security risk; attacker can exfiltrate or modify data
**Proposed fix:** Use parameterized query with ? placeholder

### 5. Hardcoded credentials in storage.py
**Location:** storage.py, API_KEY, DB_PASSWORD, SECRET_KEY
**Issue:** Credentials committed to source control
**Why it matters:** Security risk; exposed secrets
**Proposed fix:** Move credentials to environment variables or secrets manager

# A_3 #
## Code Review Categorization

### Bugs
- Division by zero in analyzer.py (crash rate, error distribution)
- Cache memory leak in deduplicator.py (no eviction policy)
- Fingerprint includes dynamic values in fingerprint.py (deduplication accuracy)
- SQL injection vulnerability in storage.py (search_by_error_type)
- SQLite connection not thread-safe in storage.py
- Similarity check in deduplicator.py uses strict > instead of >= (boundary cases missed)

### Low Quality Code
- compute_similarity in deduplicator.py compares MD5 hex strings, which is not meaningful for crash similarity
- No cache eviction policy in deduplicator.py (previously fixed, but consider LRU details)
- Hardcoded cache size in deduplicator.py (should be configurable)
- Error handling in analyzer.py and storage.py could be more robust

### Documentation Issues
- Some methods lack detailed docstrings (parameters, return values, edge cases)
- Security and thread-safety concerns are noted in comments, but should be more prominent and explicit
- Usage examples and API documentation missing for public interfaces
- No documentation on normalization logic in fingerprint.py

## Suggested Fixes
- Add guard clauses for division by zero in analyzer.py
- Ensure cache eviction policy is LRU and cache size is configurable in deduplicator.py
- Improve fingerprint normalization to handle more dynamic values and document logic
- Use parameterized queries everywhere in storage.py
- Make SQLite connection thread-safe or document single-threaded limitation
- Change similarity check to >= for correct boundary handling in deduplicator.py
- Refactor compute_similarity to compare stack trace structure, not MD5 hex
- Add detailed docstrings and API documentation
- Add usage examples in README and docstrings

