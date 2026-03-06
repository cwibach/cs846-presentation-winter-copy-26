# Week 10 Evaluation: CodeReview / PR

**Authors:** [Neel Sanjaybhai Faganiya, Ibrahim Mohammed Sayem, Felix Wang]


## 1. Evaluation Criteria

This section defines how students can determine whether they solved the example problems correctly.

Criteria should be applicable to any problem in this topic.

* Criteria 1
* Criteria 2
* Criteria n

---

## 2. Evalation specifically for Example Problems

### Problem A_1: [Title]

**Evaluation Description:**  
Describe the evaluation criteria clearly and precisely.

**Code:**  
// Include all necessary code here that is the correct answer.

---

### Problem A_2: [Title]

**Evaluation Description:**  
Describe the evaluation criteria clearly and precisely.

**Code:**  
// Include all necessary code here that is the correct answer.

---

### Problem A_n: [Title]

**Evaluation Description:**  
Describe the evaluation criteria clearly and precisely.

**Code:**  
// Include all necessary code here that is the correct answer.

---

## Problem B: Backend PR Review and Comment Validation

## Problem B.1: Security and Data Exposure

**Model to Use:** GPT-4.1

## Evaluation Description

The review should:
- Identify security and trust-boundary risks scoped only to the code introduced in the diff.
- For each risk, include: the attack/failure path, the impacted endpoint or helper function with a line reference, and a concrete mitigation.
- Avoid flagging issues that are explicitly out of scope per the PR description (e.g., authentication handled upstream, architectural redesign).
- Not repeat general security advice unrelated to the specific code changes.

---

## Bad Example

### Prompt Used
```
Please solve this question for me: Review only security/trust-boundary risks: auth boundaries, sensitive data exposure, internal ID leakage, input handling, and URL/external-call safety. 
For each risk, include: attack/failure path, impacted endpoint/helper, and mitigation.
```

### Characteristics of Output
- Findings are listed without reference to specific line numbers or function names in the diff.
- Flags authentication gaps (e.g., missing token validation, role-based access control) even though the PR explicitly states authentication is handled upstream.
- Suggests adding tests for token expiry and privilege escalation — out of scope for a security review pass.
- Mitigations are generic (e.g., "ensure all endpoints consistently require and validate JWTs") rather than tied to the actual code.
- Summary repeats points already made in the findings without adding new insight.

### Why This Is Weak
The LLM was given no boundaries, so it hallucinated concerns about the surrounding system (auth, RBAC, token validation) that the PR explicitly says are out of scope. Without line references, none of the findings are immediately actionable, a reviewer would need to re-read the entire diff to locate the issue themselves.

## Good Example

### Prompt Used
```
I am reviewing a pull request. Below is the diff and PR description. [diff] [PR_description] Assumptions: - Authentication and input validation are handled upstream. - Only evaluate code introduced in this diff. Non-goals: - Do not flag out-of-scope items from the PR description. - Do not suggest architectural redesigns. Review only for security and trust-boundary risks: auth boundaries, sensitive data exposure, internal ID leakage, and URL/external-call safety. For each risk: state the attack/failure path, the impacted function (with line reference), and a mitigation.
```

### Characteristics of Output
- Each finding includes specific line numbers and function names (e.g., `get_user_list` lines 61–75, `lookup_by_email` lines 89–101).
- Authentication is acknowledged as enforced by FastAPI's dependency injection rather than flagged as a gap which is consistent with the PR's stated assumptions.
- External call safety finding is precise: correctly notes the base URL is fixed and trusted, and scopes the SSRF risk only to future changes.
- Mitigations are concrete and tied to the specific lines identified.
- Does not suggest architectural redesigns or out-of-scope changes.

### Why This Is Better
By stating assumptions and non-goals upfront, the LLM stayed within the actual scope of the PR. The findings are immediately actionable because each one is anchored to a specific location in the code. The output is shorter and more precise, a reviewer can act on it directly without filtering out noise.

---

## Problem B.2: Test Adequacy

**Model to Use:** GPT-4.1

## Evaluation Description

The review should:
- Identify brittle or misleading tests by pointing to specific test names and the exact lines that make them brittle.
- Identify missing edge cases by referencing the specific test or function that lacks coverage.
- Identify gaps between intended behavior and actual coverage by citing both the code and the test (or lack of one).
- Propose only the minimum additional tests needed before merge — not a comprehensive wishlist.
- Ground every finding in a specific line or test name from the diff.

---

## Bad Example

### Prompt Used
```
Review only test quality. Identify brittle/misleading tests, missing edge cases, and gaps between intended behavior and coverage. Propose the minimum additional tests needed before merge.
```

### Characteristics of Output
- Findings reference test names but rarely quote the specific lines that make them brittle (e.g., "hardcoded user counts" without citing the actual assertion).
- Flags missing tests for JWT expiry, RBAC, and SQL injection — none of which are in scope for this PR or its stated constraints.
- "Minimum additional tests" list contains 7 items, several of which are out of scope (role-based access control, SQL injection, seed logic rollback).
- No distinction between what the tests *document intentionally* (e.g., the skipped test) and what is genuinely missing.
- Summary repeats the findings without adding new information.

### Why This Is Weak
Without being instructed to ground findings in specific lines, the LLM drifted into generic test advice — suggesting tests for concerns the PR explicitly does not address. The "minimum tests before merge" list is not minimum at all; it includes items that would be appropriate for a broader test audit but not for this specific PR.

## Good Example

### Prompt Used
```
I am reviewing a pull request. Below is the diff, PR description, and test file. [diff] [PR_description] [location to test_user_helpers.py]. Review only for test quality: brittle or misleading tests, missing edge cases, and gaps between intended behavior and coverage. For each finding: 1. Quote the specific test or line of code that supports your claim. 2. Explain the gap using only those lines. 3. If you cannot point to a specific line, do not include the finding. End with the minimum list of additional tests needed before merge.
```

### Characteristics of Output
- Every finding quotes the exact assertion or decorator that is the problem (e.g., `assert len(calls["urls"]) == 2` in `test_format_user_for_header_avoids_extra_calls`).
- Correctly distinguishes between intentionally skipped tests (documented behavior not yet implemented) and genuinely missing coverage.
- Identifies that `test_get_user_list_filters_role_and_hides_internal_id` is misleading because it asserts `"id" in u` while the comment implies the opposite intent — a subtle but important finding that requires reading the specific line.
- Minimum tests list contains 5 targeted items, all tied directly to gaps identified in the diff.
- Does not suggest out-of-scope tests (JWT, RBAC, SQL injection).

### Why This Is Better
By requiring line-level evidence, the LLM caught a subtle misleading test that the naive prompt missed entirely — the test that *documents* ID exposure while *implying* it should be hidden. The minimum tests list is genuinely minimal because the LLM could only include items it could justify with a specific line, which filtered out the generic suggestions that appeared in the naive output.

---

## Problem B.3: Peer Review Comment Validation

**Model to Use:** GPT-4.1

## Evaluation Description

The review should:
- Quote the specific lines from the code that are directly relevant to the claim being validated.
- Explain whether those lines support or contradict the claim based on how FastAPI's `Depends()` mechanism actually works, not based on general intuition.
- Reach a clear classification: `Accurate`, `Partially Accurate`, or `Inaccurate`.
- Provide a brief, grounded reasoning and a concrete recommended follow-up action.

---

## Bad Example

### Prompt Used
```
Use an LLM to validate the comment against the PR description, diff, and code in user_helpers.py. Classify it as Accurate, Partially Accurate, or Inaccurate, then provide brief reasoning and a recommended follow-up action.
```

### Characteristics of Output
- Reaches the correct classification (`Inaccurate`) but does not quote the specific lines from the code that support this verdict.
- Explanation relies on general knowledge of FastAPI rather than the actual lines in the diff.
- The reasoning contradicts itself, first saying the reviewer's claim is "inaccurate" in the reasoning, then classifying it as "Accurate" in the header, suggesting the LLM was not anchored to the code.
- Recommended follow-up is vague: "add tests for unauthenticated access" is generic advice not tied to the specific claim.

### Why This Is Weak
Without being instructed to ground the verdict in specific lines, the LLM reasoned from general FastAPI knowledge rather than the actual code. This produced a self-contradicting output, the classification and reasoning disagreed which is exactly the failure mode the guideline is designed to prevent. A student relying on this output would be unsure whether to trust the verdict.

## Good Example

### Prompt Used
```
I am validating a peer review comment against a pull request. Here is the diff, PR description, and the relevant code. [diff] [PR_description] [location to user_helpers.py] The peer reviewer made the following claim: "Although each route declares Depends(auth.get_current_user), the returned value is assigned to _ and discarded, which means authentication is effectively not enforced." Before accepting or rejecting this claim: 1. Quote the exact line(s) from the code that are relevant to this claim. 2. Explain whether those lines support or contradict the claim, based only on how FastAPI's Depends() mechanism actually works. 3. If you cannot ground your verdict in specific lines, do not include the finding. Classify the comment as Accurate, Partially Accurate, or Inaccurate, then provide brief reasoning and a recommended follow-up action.
```

### Characteristics of Output
- Quotes all four relevant lines across the endpoints where `_: dict = Depends(auth.get_current_user)` appears before reaching a verdict.
- Explains the mechanism precisely: FastAPI executes the dependency regardless of whether the return value is used, so assigning to `_` does not bypass enforcement.
- Classification (`Inaccurate`) is consistent with the reasoning, no contradiction.
- Recommended follow-up is concrete and scoped: reject the claim, no code change needed, optionally clarify in comments.

### Why This Is Better
By requiring the LLM to quote the relevant lines before reaching a verdict, the output is self-consistent and immediately verifiable, a reviewer can check the quoted lines themselves and confirm the reasoning. The naive output reached the same general conclusion but contradicted itself, making it untrustworthy. The guided output is actionable: a reviewer can reject the comment confidently and explain why with specific evidence.

---

## Problem B.4: Correctness and Constraint Fit

**Model to Use:** GPT-4.1

## Evaluation Description

The review should:
- Begin with a structured context summary: PR intent, affected components, and high-risk areas.
- List findings with severity (`Blocker`, `Major`, `Minor`, `Question`), impacted file(s), violated requirement or constraint, and a minimal fix.
- Not repeat security or test findings already covered in B1 and B2.
- End with a justified merge decision (`Approve`, `Request Changes`, or `Reject`) based on the findings.

---

## Bad Example

### Prompt Used
```
Review functional correctness and PR-constraint alignment. List findings with severity 
(Blocker, Major, Minor, Question) and include: impacted file(s), violated requirement constraint, and minimal fix. End with a merge decision based on all prior considerations.
```

### Characteristics of Output
- Jumps directly into findings without first establishing what the PR is trying to do or which components are affected.
- Repeats findings from B1 (internal ID exposure) and B2 (missing edge case tests, brittle assertions) instead of focusing on new correctness and constraint-fit issues.
- Finding 5 ("Functional Correctness") is not a finding, it states no bugs were found and suggests a vague audit, which adds no actionable value.
- The merge decision ("Request Changes") is based largely on B1 and B2 findings rather than anything specific to correctness or constraint fit.
- No findings tied to specific files like `database.py` or `seed.py`, which are the most complex parts of this PR.

### Why This Is Weak
Without a context summary step, the LLM had no structured understanding of the PR before reviewing it. It defaulted to rehashing prior findings rather than identifying new correctness issues. The most technically complex parts of the diff, the database migration logic and seed normalization, were not examined at all.

## Good Example

### Prompt Used
```
I am reviewing a pull request. Below is the diff and PR description. [diff] [PR_description] Step 1 — Context summary: - Summarize the intent of this PR. - Identify the affected components. - Highlight any high-risk or complex areas. Step 2 — Focused review: Review only for functional correctness and PR-constraint alignment. For each finding include: - Severity (Blocker, Major, Minor, or Question) - Impacted file(s) - Violated requirement or constraint from the PR description - Minimal fix Do not repeat security or test findings from prior review passes. End with a merge decision: Approve, Request Changes, or Reject.
```

### Characteristics of Output
- Opens with a structured context summary that identifies affected components (including `database.py`, `seed.py`, `main.py`) and flags the migration logic and seed normalization as high-risk areas before any findings are listed.
- Findings are scoped to new correctness issues not covered in B1/B2: the `created_at` migration default being set to an empty string instead of `CURRENT_TIMESTAMP`, and the missing fallback in `_normalize_user` when both `name` and `full_name` are absent.
- Does not re-raise security or test concerns from earlier passes.
- Merge decision ("Request Changes") is justified specifically by the two correctness findings, making it easy to trace back to the evidence.

### Why This Is Better
The context summary forced the LLM to read and understand the full scope of the PR before issuing findings. This is what surfaced the `database.py` migration bug and the seed normalization gap, both of which require understanding what the PR intends before you can identify where it falls short. The naive prompt skipped this step entirely and missed the most technically substantive issues in the diff.

---

### Problem C: Pull Request Supply Chain Review

**Good Example:**
Fork the current repository, then go to:

Settings -> Security -> Advanced Security -> Dependabot -> Enable Dependabot Alerts -> Enable.

Trigger a push on main branch, then go to:

Security -> Vulnerability Alerts -> Dependabot.

**Bad Prompt Example:**

`You are an experienced coding agent, please verify the dependency versions for me: [path-to-file].`

**Good Example Output:**

In Security -> Vulnerability Alerts -> Dependabot, this vulnerabile version of package will show up:

|             | CVE-2026-3304           |
|-------------|-------------------------------------|
| Severity   | High |
| CVSS Score | 8.7/10 |
|  Description  | Multer is a node.js middleware for handling `multipart/form-data`. A vulnerability in Multer prior to version 2.1.0 allows an attacker to trigger a Denial of Service (DoS) by sending malformed requests, potentially causing resource exhaustion. Users should upgrade to version 2.1.0 to receive a patch. No known workarounds are available.                                    |
| NVD Published Date | 02/27/2026 |
| Attack Vector | Network |
| Attack Complexity | Low |
| Attack Requirement | None |
| Privileges Required | None | 
| User Interaction | None |
| Related CWE | CWE-459: Incomplete Cleanup |

**Bad Example Output:**

GPT 4.1: 
```
......

Conclusion & recommendations
* The “after” lock file is consistent with the updated package.json and accurately captures all newly introduced dev dependencies.
* npm ci runs without errors, so the lock file is valid and usable.
* There’s nothing broken in the dependency update itself; the only “issue” is that running npm test returns an error because there are no tests. If you plan to use Jest, add test files or tweak the test script.
```

**Why it's bad:**

This problem will not likely be resolved by simply letting LLMs inspect the dependency files before and after PR. LLMs are not designed to reliably reason over large, highly-structured lockfile. In this example, multer package versions < 2.1.0 are known to be severely vulnerable to Denial of Service attacks (CVE-2026-3304). But the Copilot failed to capture it.

More details can be found on the National Vulnerability Database (NVD)'s official website [https://nvd.nist.gov/vuln/detail/CVE-2026-3304](https://nvd.nist.gov/vuln/detail/CVE-2026-3304).

---

### Problem D: Northwind Signal Project PR Review

#### Problem D.1: Usage Audit Feature PR Review

**Good Prompt Example:**

In `.github/instructions/typescript.instructions.md`, clearly identify testing and security expectations.

```
---
applyTo: "**/*.ts"
---
# TypeScript Coding Standards
This file defines our TypeScript coding conventions for Copilot code review.

## Error Handling

- Always handle promise rejections with `try/catch` or `.catch()`.
- Use custom error classes for application-specific errors.

## Security

- Be extremely cautious with binary executables. Any binary executable should be avoided by default. 

## Testing

- Write unit tests for all exported functions.
- Use [Jest](https://jestjs.io/) for all testing.
- Name test files as `<filename>.test.ts`.

## Example

```typescript
// Good
interface User {
  id: number;
  name: string;
}

const fetchUser = async (id: number): Promise<User> => {
  try {
    // ...fetch logic
  } catch (error) {
    // handle error
  }
};

// Bad
interface user {
  Id: number;
  Name: string;
}

async function FetchUser(Id) {
  // ...fetch logic, no error handling
}
```

**Bad Prompt Example:**

1. No instruction file provided. 
2. Expectations for binary executables are not listed in a security-related section in the instruction. 

**Good Output Example:**

```
...

* The backend (usage.service.ts) uses a vendor-provided binary executable (audit_writer) to write audit events.
TypeScript instructions explicitly warn to avoid binary executables by default for security reasons.
* No unit tests were added for the new backend logic, especially for the audit endpoints.
Instructions require unit tests for all exported functions, using Jest.
* The code does not use custom error classes for application-specific errors; it relies on NestJS exceptions.
Instructions recommend custom error classes for better error handling.
* The frontend and backend changes are otherwise modular and follow naming conventions, code style, and error handling for promises.
```

**Bad Output Example:**

```
...

Conclusion
This PR is well-structured and achieves the goal of integrating a vendor-supplied audit workflow. The encapsulation of vendor logic is appropriate for compliance. The API and UI changes are clear and functional. With minor improvements to error handling and security, this is ready to merge.
```

**Why it's bad:**

The most severe issue contained in this PR is that, the binary executable file under the folder `problem_d/problem_d_backend/src/vendor` called `audit_writer` is simulating some malicious behaviours. Don't worry though, it's not really malicious, you can find the file in the `audit_writer-file` branch. All it does is to create a data record with a message: `This is a malicious event in the binary file, your database is now compromised`. However, the real security concern is not the message itself. The core issue is that: A precompiled binary executable has been committed directly into the repository and invoked by backend logic!

Any PR review comments questioning the necessity of doing so, asking for cryptographic evidence, and ways to reproduce it is a good solution. 

There are other severe issues in this PR, your solution is good if you find more or all of them: 
```
1. Missing Type Safety on Event Handler
File: main.ts
Lines: ~382-395
Issue: The auditButton might be null, but the code proceeds without proper guards in some places.

2. Implicit any Type on Error
File: main.ts, usage.service.ts
Lines: ~364-365 and ~393-394, ~46-50
Issue: Bare catch blocks without typing violate the TypeScript standard of avoiding any types.

3. Insufficient Input Validation
File: main.ts
Lines: ~384-388
Issue: No validation of the API response before rendering. The entries array could be malformed.

4. Arbitrary Command Execution Vulnerability
File: usage.service.ts
Lines: ~32-40
Issue: Using execFile with unsanitized user input (message) as a command argument.
Risk: Although execFile is safer than exec, the message parameter should be further validated/sanitized.

5. Missing Input Validation: Message Length Enforcement
File: usage.controller.ts
Lines: ~12-17
Issue: Message length limit (1000 chars) is enforced but could be externalized as a constant.
Recommendation: Create a constants file with validation rules.

6. There are no tests
No unit tests for usage.service.ts (following TypeScript standard that requires unit tests for all exported functions)
No integration tests for the new endpoints (GET /usage/audit-log, POST /usage/audit)
No frontend tests for the new audit panel UI and event handlers
```

#### Problem D.2: Annual Report Generation PR Review

**Good Prompt Example:**

1. In `.github/instructions/typescript.instructions.md`, clearly identify naming convention expectations and code style expectations.

```
---
applyTo: "**/*.ts"
---
# TypeScript Coding Standards
This file defines our TypeScript coding conventions for Copilot code review.

## Naming Conventions

- Use `camelCase` for variables and functions.
- Use `PascalCase` for class and interface names.
- Prefix private variables with `_`.

## Code Style

- Prefer `const` over `let` when variables are not reassigned.
- Use arrow functions for anonymous callbacks.
- Avoid using `any` type; specify more precise types whenever possible.
- Limit line length to 100 characters.

## Error Handling

- Always handle promise rejections with `try/catch` or `.catch()`.
- Use custom error classes for application-specific errors.

## Security

- Be extremely cautious with binary executables. Any binary executable should be avoided by default. 

## Testing

- Write unit tests for all exported functions.
- Use [Jest](https://jestjs.io/) for all testing.
- Name test files as `<filename>.test.ts`.
- All test cases should pass. 
- Test coverage should reach at least 70%.

## Example

```typescript
// Good
interface User {
  id: number;
  name: string;
}

const fetchUser = async (id: number): Promise<User> => {
  try {
    // ...fetch logic
  } catch (error) {
    // handle error
  }
};

// Bad
interface user {
  Id: number;
  Name: string;
}

async function FetchUser(Id) {
  // ...fetch logic, no error handling
}
```

2. In `.github/semgrep.yml`, clearly formulated static anlysis scan patterns for detecting camelCases, PascalCases, and `any` abuse.

For example:

```
  - id: typescript-camelcase-functions
    message: "Use camelCase for function names."
    languages: [typescript]
    severity: WARNING
    patterns:
      - pattern: "function $F(...) { ... }"
      - metavariable-regex:
          metavariable: "$F"
          regex: "(^[A-Z]|.*_.*)"
```

or

```
  - id: typescript-no-any
    message: "Avoid 'any' in TypeScript. Use a specific type or 'unknown'."
    languages: [typescript]
    severity: WARNING
    pattern-either:
      - pattern: "const $X: any = $Y"
      - pattern: "let $X: any = $Y"
      - pattern: "var $X: any = $Y"
      - pattern: "($P: any) => $BODY"
      - pattern: "function $F($P: any, ...$REST) { ... }"
      - pattern: "function $F(...$ARGS: any[]) { ... }"
      - pattern: "class $C { $K: any; }"
      - pattern: "function $F(...$ARGS): any { ... }"
      - pattern: "$M(...$ARGS): any { ... }"
```

etc. 

**Bad Prompt Example:**

1. No instruction file provided. 
2. Expectations for testing are not listed in the instruction file.
3. Static Analysis Tool is not used. 

**Good Output Example:**

```
...
Fix the unit test expectation:
  In problem_d/problem_d_backend/src/modules/reports/reports.service.spec.ts change
    expect(result.year).toBe(2026);
  to expect(result.year).toBe(2025);
Rationale: align test with input and service behavior.
...
Minor code style: RenderReport and LoadReport use any heavily. Consider adding stronger types.
...
Variable naming:
Rename EndDate → endDate in reports.service.ts for consistency.
...
Decision

Recommendation: Request Changes (do not accept yet).
Rationale: The feature is coherent and valuable, but there are at least one concrete test bug (inconsistent expected year), questionable dependency/tsconfig changes for React (likely accidental), usability/security improvements (XSS risk from innerHTML, missing auth), and some small code-quality items (naming, HTTP error semantics). These should be addressed before merging.
```

**Bad Output Example:**

```
...
Decision
Accept — The PR is well-structured, implements the requested feature, and includes tests. Minor issues are not blockers and can be addressed in future PRs.

Recommendation: Merge this PR. Consider reviewing the year logic and dependency choices in a follow-up.
```

**Why it's bad:**
TypeScript is a superset of JavaScript, and it adds static typing and compile-time checks on top of JavaScript, which offers compile-time guarantees, early error detection, and safer refactoring. Therefore, when TypeScript developers bypass the type system by abusing the `any` type, it could cause the guarantee provided by TS collapse to JS-level safety. That undermines the primary reason for choosing TypeScript in the first place. 

And there are other naming conventions in TypeScript like using `camelCase` for variables and functions, and use `PascalCase` for class and interface names. This is for better consistency, readibility and maintainability across the codebase. 

**Criteria 1:** Your solution is good if you catch more or all `any` type abuses:

| # | File Name |   Line Number       | Code Snippet         |
|---|--|--------|-------------------------------------|
| 1 |problem_d/problem_d_backend/src/modules/reports/reports.controller.ts | 10 | `const resolvedYear: any = year ? Number(year) : new Date().getFullYear() - 1;`| 
| 2 |problem_d/problem_d_backend/src/modules/reports/reports.controller.ts | 11 | `const orgId: any = organizationId ?? 'org_001';`|
| 3 |problem_d/problem_d_backend/src/modules/reports/reports.service.ts | 8 | `CompanyReport(organizationId: any, year: any): any {)`|
| 4 |problem_d/problem_d_backend/src/modules/reports/reports.service.ts | 9 | `const org: any = this.db.get()`|
| 5 |problem_d/problem_d_backend/src/modules/reports/reports.service.ts | 22 | ``const startDate: any = `${year}-01-01`;``|
| 6 |problem_d/problem_d_backend/src/modules/reports/reports.service.ts | 23 | ``const EndDate: any = `${year}-12-31`;``|
| 7 |problem_d/problem_d_backend/src/modules/reports/reports.service.ts | 25 | ``const invoiceSummary: any = this.db.get()``|
| 8 |problem_d/problem_d_backend/src/modules/reports/reports.service.ts | 35 | ``const projectSummary: any = this.db.get()``|
| 9 |problem_d/problem_d_backend/src/modules/reports/reports.service.ts | 43 | ``const lastProject: any = this.db.get()``|
| 10 |problem_d/problem_d_backend/src/modules/reports/reports.service.ts | 52 | ``const usage: any = this.db.get()``|
| 11 |problem_d/problem_d_backend/src/modules/reports/reports.service.ts | 61 | ``const summaryPoints: any[] = []``|
| 12 |problem_d/problem_d_backend/src/modules/reports/reports.service.ts | 69 | ``const keyMetrics: any[] = []``|
| 13 |problem_d/problem_d_backend/src/modules/reports/reports.service.ts | 76 | ``const narrative: any =``|
| 14 |problem_d/problem_d_backend/src/modules/reports/reports.service.ts | 80 | ``const ReportData: any = {``|
| 15 |problem_d/problem_d_frontend/src/main.ts | 288 | ``const RenderReport = (payload: any) => {``|
| 16 |problem_d/problem_d_frontend/src/main.ts | 306 | ``(metric: any) => ``|
| 17 |problem_d/problem_d_frontend/src/main.ts | 315 | ``map((item: any) => `<li>${item}</li>`).join('')}``|
| 18 |problem_d/problem_d_frontend/src/main.ts | 321 | ``const lastYear: any = new Date().getFullYear() - 1;``|
| 19 |problem_d/problem_d_frontend/src/main.ts | 322 | ``const reportButton: any = document.getElementById``|
| 20 |problem_d/problem_d_frontend/src/main.ts | 323 | ``const ReportYear: any = document.getElementById()``|
| 21 |problem_d/problem_d_frontend/src/main.ts | 324 | ``const reportStatus: any = document.getElementById()``|
| 22 |problem_d/problem_d_frontend/src/main.ts | 326 | ``let ReportData: any = null;``|
| 23 |problem_d/problem_d_frontend/src/main.ts | 327 | ``const setreportData: any = (value: any) => {``|
| 24 |problem_d/problem_d_frontend/src/main.ts | 344 | ``const res: any = await fetch``|
| 25 |problem_d/problem_d_frontend/src/main.ts | 345 | ``const data: any = await res.json();``|
| 26 |problem_d/problem_d_frontend/src/main.ts | 350 | ``} catch (error: any) {``|

Try to think about:
- Did the LLM-assisted PR review tool catch all these? Why or why not?
- The static analysis tool using our heuristic only caught 21, why do you think this happened (See [PR #11 -> Files changed](https://github.com/U70-TK/cs846-presentation-winter-26/pull/11/changes))?

**Criteria 2:** And your solution is good if you catch more or all naming convention violations:

| # | File Name |   Line Number       | Code Snippet         |
|---|--|--------|-------------------------------------|
| 1 |problem_d/problem_d_backend/src/modules/reports/reports.service.ts | 23 | ``const EndDate: any = `${year}-12-31`;``|
| 2 |problem_d/problem_d_backend/src/modules/reports/reports.service.ts | 8 | ``CompanyReport(organizationId: any, year: any): any {``|
| 3 |problem_d/problem_d_backend/src/modules/reports/reports.service.ts | 80 | ``const ReportData: any = {``|
| 4 |problem_d/problem_d_frontend/src/main.ts | 288 | ``const RenderReport = (payload: any) => {``|
| 5 |problem_d/problem_d_frontend/src/main.ts | 320 | ``const LoadReport = (): any => {``|
| 6 |problem_d/problem_d_frontend/src/main.ts | 323 | ``const ReportYear: any = document.getElementById(``|
| 7 |problem_d/problem_d_frontend/src/main.ts | 326 | ``let ReportData: any = null;``|

Try to think about:
- Did the LLM-assisted PR review tool catch all these? Why or why not?

**Criteria 3:** Your solution is good if you catch that the test cases for this PR will not pass. 

The test case at line 54 of the file `problem_d/problem_d_backend/src/modules/reports/reports.service.spec.ts` will not pass: `expect(result.year).toBe(2026);`. 


## 3. References

---

