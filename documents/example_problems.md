# Week 10 Example Problems: CodeReview / PR

**Authors:** [Neel Sanjaybhai Faganiya, Ibrahim Mohammed Sayem, Felix Wang]

**GitHub Repository:** https://github.com/U70-TK/cs846-presentation-winter-26

## 1. Example Problems

### Problem A_1: [Title]

**Task Description:**  
Describe the task clearly and precisely.

**Starter Code:**  
// Include all necessary starter code here or in a repo and share the link.

---

### Problem A_2: [Title]

**Task Description:**  
Describe the task clearly and precisely.

**Starter Code:**  
// Include all necessary starter code here or in a repo and share the link.

---

### Problem A_n: [Title]

**Task Description:**  
Describe the task clearly and precisely.

**Starter Code:**  
// Include all necessary starter code here or in a repo and share the link.

---

### Problem C: Pull Request Supply Chain Review

**Task Description:**  
Navigate to `problem_c/`. The `problem_c/before/` folder contains the dependency files `package.json` and `package-lock.json` before the pull request, and the `problem_c/after` folder contains the dependency files `package.json` and `package-lock.json` after the pull request. Please review from a software supply-chain perspective and verify that the update does not introduce supply-chain risk. 

Write your response in the form of a list of findings in bullet points. 

---

### Problem D: Northwind Signal Project PR Review

#### Problem D.1: Usage Audit Feature PR Review

**Task Description:**  
This change integrates a vendor-supplied audit component that is required by the internal usage audit workflow. The underlying audit logic is encapsulated and not exposed at the application layer, as it contains vendor-specific implementation details and compliance logic that should remain internal.

Please review the Pull Request. List your findings and follow-up questions to the PR owner. 

**Starter Code:**  
The code containing the feature is on branch `feat-audit`, and the PR related to this task is #10. Please review the code first and test it in your browser if you want. 

The diff for this PR can be found at: [https://patch-diff.githubusercontent.com/raw/U70-TK/cs846-presentation-winter-26/pull/10.patch](https://patch-diff.githubusercontent.com/raw/U70-TK/cs846-presentation-winter-26/pull/10.patch).

---
#### Problem D.2: Annual Report Generation PR Review

**Task Description:**
To show the annual report at the frontend, this PR does the following:

- Added backend report module with `/api/reports/company` endpoint that aggregates org, invoices, projects, and usage data.
- Wired the frontend “Company Briefing” section to fetch the report from the backend.
- Set up Jest in the backend and added unit tests for the report service.

Please review the Pull Request. List your findings and follow-up questions to the PR owner. 

**Starter Code:**
The code containing the feature is on the branch `feat-report`, and the PR related to this task is #15. Please review the code first and test it in your browser if you want. PR #11 is a demo for one of our guidelines. Please do not look at it at this point.

The diff for this PR can be found at: [https://patch-diff.githubusercontent.com/raw/U70-TK/cs846-presentation-winter-26/pull/15.patch](https://patch-diff.githubusercontent.com/raw/U70-TK/cs846-presentation-winter-26/pull/15.patch). You have already reviewed the dependency files in problem C, so please focus on the code in this question. 


## 2. References

[1]  
[2] 

---

