# Problem B: Code Review Tasks

**PR description:** `test/PR.md`  
**Code to review:** `problem_b/user_helpers.py`

Use the PR description when prompting. It provides the goal, constraints, scope, and what is out of scope.

---

## Task 1: Code review

Get a code review for the changes in this PR. You want feedback on correctness, error handling, security (what is exposed to the UI), and performance (e.g., unnecessary API calls or latency risks). Tie comments to the constraints in the PR.

---

## Task 2: Security and data-exposure concerns

Identify security concerns and data-exposure risks in the PR. Be specific: which data might be exposed where, which inputs are not validated, and any injection or URL risks. Consider what the PR says is in scope vs out of scope.

---

## Task 3: Test and edge-case suggestions

Suggest edge cases and error conditions that should be tested for this PR. Name concrete scenarios (e.g., network failure, empty response, missing keys in JSON, user not found) rather than generic categories. Focus on the areas the PR highlights as critical.

---

## Task 4: High-risk areas and review focus

Using the PR description and code, identify the high-risk or complex areas that deserve the most attention. Then suggest what the review should focus on (and what it should avoid or deprioritize, per the PR’s “Out of scope” section).
