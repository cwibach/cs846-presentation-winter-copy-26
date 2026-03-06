# Week 10 Example Problems: CodeReview / PR

**Authors:** [Neel Sanjaybhai Faganiya, Ibrahim Mohammed Sayem, Felix Wang]

**GitHub Repository:** https://github.com/U70-TK/cs846-presentation-winter-26

## 1. Example Problems

### Problem A: Understanding the Code Review Process
**Model to Use:** GPT-4.1
### Problem Description

You are given crash-dedup, which deduplicates crash reports from distributed systems by grouping repeated crashes into a single entry so developers can focus on unique issues. The project consists of four modules: fingerprint.py, which generates MD5 fingerprints from stack traces; deduplicator.py, which groups crashes based on similarity; storage.py, which stores and retrieves reports using SQLite; and analyzer.py, which computes crash frequency statistics and generates reports.

Setup: run once before starting: ```pip install -r requirements.txt```
Use the **GPT-4.1** model for this problem

### Problem A_1: Verify the Program

**Task Description:**  
Execute the existing test suite for the project. Record the number of tests that pass and fail and document any error messages or failures observed during execution. For testing, use python -m pytest tests/ -v.

**Starter Code:**  
See all files inside the ``crash_dedup/`` folder and the ``tests/`` folder in the ``problem_a`` project directory.

---

### Problem A_2: Code Review: Identify Bugs and Issues with GitHub Copilot

**Task Description:**  
Use GitHub Copilot Chat to review all files in the crash_dedup/ directory. Ask Copilot to review the code as an experienced software engineer would in a pull request. Your report should document the AI’s findings, including an overall verdict (Approve, Request Changes, or Reject), a list of identified bugs with their locations and proposed fixes, any security vulnerabilities, and missing or insufficient documentation. 


**Starter Code:**  
See all files inside the ``crash_dedup/`` folder and the ``tests/`` folder in the ``problem_a`` project directory.

---

### Problem A_3: Code Review: Quality & Improvement Analysis

**Task Description:**  
Use GitHub Copilot Chat to review the code in the crash_dedup/ directory. Ask Copilot to evaluate the correctness, code quality, comment quality, code style, and security aspects of the code. For each issue identified, categorize it as Bug Fix, Documentation, and indicate any cases that cannot be detected by the Copilot prompt.

**Starter Code:**  
See all files inside the ``crash_dedup/`` folder and the ``tests/`` folder in the ``problem_a`` project directory.

---

### Problem B: Backend PR Review and Comment Validation

**Model to Use:** GPT-4.1

**Shared Context (for B1-B4):**  
Use the PR description and diff as the source of intent, constraints, boundaries, and out-of-scope items. Keep each answer scoped to its task and avoid repeating points across tasks.

**PR To Review:** [Add user helper module and seed data with tests #16](https://github.com/U70-TK/cs846-presentation-winter-26/pull/16) on branch [feat-user-helper](https://github.com/U70-TK/cs846-presentation-winter-26/tree/feat-user-helper)

**Diff and Commit Details:** [https://patch-diff.githubusercontent.com/raw/U70-TK/cs846-presentation-winter-26/pull/16.patch](https://patch-diff.githubusercontent.com/raw/U70-TK/cs846-presentation-winter-26/pull/16.patch)

#### Problem B1: Security and Data Exposure

**Task Description:**  
Review only security/trust-boundary risks: auth boundaries, sensitive data exposure, internal ID leakage, input handling, and URL/external-call safety. For each risk, include: attack/failure path, impacted endpoint/helper, and mitigation.

#### Problem B2: Test Adequacy

**Task Description:**  
Review only test quality. Identify brittle/misleading tests, missing edge cases, and gaps between intended behavior and coverage. Propose the minimum additional tests needed before merge.

#### Problem B3: Peer Review Comment Validation

**Task Description:**  
Your peer reviewer `wangtkuan-crypto` raised the following comment:

`Security review summary: all endpoints appear to be in critical danger. Although each route declares Depends(auth.get_current_user), the returned value is assigned to _ and discarded, which means authentication is effectively not enforced. As implemented, every endpoint should be treated as unauthenticated and vulnerable to unauthorized access until this is fixed.`

and in `problem_b/user_helpers.py` line 139 - 142:

`Depends(auth.get_current_user) is assigned to _, so the dependency result is discarded and auth isn’t actually enforced.` (see the review left by reviewer `wangtkuan-crypto` in the PR for more details).

You are unsure whether this comment is accurate. Use an LLM to validate the comment against the PR description, diff, and code in `problem_b/`. Classify it as `Accurate`, `Partially Accurate`, or `Inaccurate`, then provide brief reasoning and a recommended follow-up action.

#### Problem B4: Correctness and Constraint Fit

**Task Description:**  
After completing B1 and B2, review functional correctness and PR-constraint alignment. List findings with severity (`Blocker`, `Major`, `Minor`, `Question`) and include: impacted file(s), violated requirement/constraint, and minimal fix. End with a merge decision (`Approve`, `Request Changes`, or `Reject`) based on all prior considerations.

---

### Problem C: Pull Request Supply Chain Review (5 mins)

**Model to use:** GPT-4.1 

**Task Description:**  
Navigate to `problem_c/`. The `problem_c/before/` folder contains the dependency files `package.json` and `package-lock.json` before the pull request, and the `problem_c/after` folder contains the dependency files `package.json` and `package-lock.json` after the pull request. Please review from a software supply-chain perspective and verify that the update does not introduce supply-chain risk. 

Write your response in the form of a list of findings in bullet points. End with a merge decision (`Approve`, `Request Changes`, or `Reject`) based on all prior considerations.

---

### Problem D: Northwind Signal Project PR Review (20 mins)

**Model to use:** GPT-4.1 

#### TypeScript Environment Setup

Install Node.js (if you don't have it): 

Copy and paste commands from [https://nodejs.org/en/download](https://nodejs.org/en/download).

Install TypeScript (if you don't have it):
```
npm install typescript --save-dev
```

Verify your Installation (if you don't have it):
```
npx tsc
```

#### How to run this project

**1.** Go to problem_d folder:
```
cd problem_d
```
**2.** Seed the database: 
```
cd problem_d_database
bash seed.sh
cd ..
```
**3.** Start backend:
```
cd problem_d_backend
npm install
npm run start:dev
```
**4.** Create another terminal and start frontend:
```
cd problem_d_frontend
npm install 
npm run dev
```


#### Problem D.1: Usage Audit Feature PR Review (10 mins)

**Task Description:**  
This change integrates a vendor-supplied audit component that is required by the internal usage audit workflow. The underlying audit logic is encapsulated and not exposed at the application layer, as it contains vendor-specific implementation details and compliance logic that should remain internal.

Please review the Pull Request. List your findings and follow-up questions to the PR owner. End with a merge decision (`Approve`, `Request Changes`, or `Reject`) based on all prior considerations.

**Starter Code:**  
The code containing the feature is on branch `feat-audit`, and the PR related to this task is #10. Please review the code first and test it in your browser if you want. 

The diff for this PR can be found at: [https://patch-diff.githubusercontent.com/raw/U70-TK/cs846-presentation-winter-26/pull/10.patch](https://patch-diff.githubusercontent.com/raw/U70-TK/cs846-presentation-winter-26/pull/10.patch).

---
#### Problem D.2: Annual Report Generation PR Review (10 mins)

**Task Description:**
To show the annual report at the frontend, this PR does the following:

- Added backend report module with `/api/reports/company` endpoint that aggregates org, invoices, projects, and usage data.
- Wired the frontend “Company Briefing” section to fetch the report from the backend.
- Set up Jest in the backend and added unit tests for the report service.

Please review the Pull Request. List your findings and follow-up questions to the PR owner. End with a merge decision (`Approve`, `Request Changes`, or `Reject`) based on all prior considerations.

**Starter Code:**
The code containing the feature is on the branch `feat-report`, and the PR related to this task is #15. Please review the code first and test it in your browser if you want. PR #11 is a demo for one of our guidelines. Please do not look at it at this point.

The diff for this PR can be found at: [https://patch-diff.githubusercontent.com/raw/U70-TK/cs846-presentation-winter-26/pull/15.patch](https://patch-diff.githubusercontent.com/raw/U70-TK/cs846-presentation-winter-26/pull/15.patch). You have already reviewed the dependency files in problem C, so please focus on the code in this question. 


## 2. References

[1]  
[2] 

---
