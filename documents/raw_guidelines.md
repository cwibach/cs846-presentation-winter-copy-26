# Week 10 Raw Guidelines: CodeReview / PR

**Authors:** [Neel Sanjaybhai Faganiya, Ibrahim Mohammed Sayem, Felix Wang]

**Readings:**
- Accountability in Code Review: The Role of Intrinsic Drivers and the Impact of LLMs [1]
- Prompting and Fine-tuning Large Language Models for Automated Code Review Comment Generation [2]
- Rethinking Code Review Workflows with LLM Assistance: An Empirical Study [3]
- The Impact of Large Language Models (LLMs) on Code Review Process [4]
- LLMs as Code Review Agents: A Rapid Review [5]
- Evaluating Large Language Models for Code Review [6]
- Automated Code Review In Practice [7]
- GitHub blog: Code review in the age of AI [8] 
- Unlocking the full power of Copilot code review: Master your instructions files [9]
- Using GitHub Copilot code review [10]
- uReview: Scalable, Trustworthy GenAI for Code Review at Uber [11] 
- Detecting malicious pull requests at scale with LLMs [12]

**Additional Readings:**
- Wolves in the Repository: A Software Engineering Analysis of the XZ Utils Supply Chain Attack [13]
- Arbiter: Bridging the static and dynamic divide in vulnerability discovery on binary programs. [14]
- Your security scans are missing Critical Vulnerabilities—Here’s Why. [15]

## 1. Guidelines from Readings

### Guideline 1: Create a structured instruction file [9].

**Description:**  

Add a Copilot Code Review instructions file that is concise, structured, and scoped to where it should apply:

* Use repo-wide `.github/copilot-instructions.md` for standards that apply everywhere.

* Use path-specific `.github/instructions/*.instructions.md` with applyTo frontmatter for language/module-specific rules. 

Your instruction file should be concise and structured, consider including sections like: "Naming Conventions", "Code Style", "Error Handling", "Testing", and "Example".

**Reasoning:**  
LLMs struggle with complex tasks that require extensive contextual or repository understanding [5], and due to the inherent undeterministic nature of LLMs, their outputs can drift in unexpected directions without clear constraints. Github Copilot recently added support for repo-wide and path-specific instructions [9] so that you can define a universal and customized guidelines for your Copilot agent to fit into your workflow. By providing structured headings and bullet points, it helps Copilot to access organized and focued instruction. However, long instruction files (over 1000 lines) should be avoided, as this leads to inconsistent behaviours and may cause "Lost in the middle" effect [16]. 

**Good Example:**  

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

**Bad Example:**

```
Perform a Pull Request review.
```

---

### Guideline 2: Using Static Analysis Tools as a CI Gate [11] [8]

**Description:**

Integrate static analysis tools (e.g., linters, type checkers, security scanners) into your CI pipeline and configure them as mandatory checks before pull request merge. GitHub CI supports assorted static analysis tool integrations like CodeQL (primarily for security), Semgrep (pattern based bug finding with customized rules), and your ecosystem’s usual linters/type checkers (ESLint/tsc, pylint/mypy, etc.). 

**Reasoning:**

Unlike LLMs, most static analysis tools like Semgrep, CodeQL, etc. are deterministic and rule-based. They enforce predefined constraints across all changes, which can provide a consistent and systematic guarantee to your project. Depending on its proprietary, static analysis tools are generally capable of detecting: Syntax and type errors, Code style violations, Security vulnerabilities, Dead code or unreachable branches, and Complexity thresholds. However, this is not in conflict with LLM-assisted Code Review, as static analysis tools sometimes lack flexibility and may generate false alarms. These tools should be combined together. 

**Good Example:**

Customized static analysis patterns should neither be overly broad nor overly strict.

- If it's too broad, it may trigger too many false positives. 
- If it's too strict, it likely will not catch anything. 

A good static analysis pattern definition should find a balance in between, and match project-specific conventions and expectations. 

A good example can be found at `.github/semgrep.yml`. 

**Bad Example:**

Static analysis patterns being too broad or too strict. 


#### Guideline 2.3 Enforce Test Coverage

**Description:**

Require automated tests to run in CI and enforce a minimum, meaningful test coverage threshold as a mandatory condition before merging.

**Reasoning:**

While static analysis and dependency scanning catch structural and known vulnerability issues, they do not validate runtime behavior. Tests provide behavioral guarantees and protect against regressions.

**Good Example:**

Ensure good testing principles like Blackbox testing, Whitebox testing, MC/DC testing, mutation test etc, in alignment with project-specific conventions and risk expectations. Establish a team-wide test coverage as a threshold. 

**Bad Example:**

Writing meaningless test cases just for a high branch coverage and mutation score. 

---

### Guideline N: [Short, Actionable Title]
(Repeat the same structure for each guideline.)

---

## 2. Guidelines from from any related research/grey literature like practitioner or developer tool blogs

> **Note:** Guidelines should be actionable, specific, and usable during real coding tasks.

### Guideline 1: Be Extra Cautious about Binary Executables [13]
**Description:**  
Avoid committing binary executables (e.g., .exe, .dll, .jar, compiled artifacts, vendor-provided binaries) directly into the repository unless absolutely necessary. If inclusion is required, document their origin for accountability [1]. 

**Reasoning:**  

Previous studies have shown that many known CVE vulnerabilities are embedded within third-party components and precompiled binaries committed into repositories [13–15]. Unlike source code, binary artifacts cannot be meaningfully reviewed, diffed, or statically analyzed using standard development workflows. This creates a blind spot in both human review and automated tooling. However, opaqueness requirements do exist, and it also happens a lot in testing. Thus, binary files they must be treated as high-risk supply chain elements rather than normal source files.

**Good Example:**

Require the PR submitter to explicitly justify its inclusion. Explicitly document it for accountability. 

**Bad Example:**

Ignore it and merge it into the repo. 


**Example:**  
Provide a brief illustrative example (code or pseudo-code if helpful).

---

### Guideline 2: Use Automated Dependency Management Tools

**Description:**

Enable automated dependency monitoring and update mechanisms in your CI/CD workflow to continuously detect and remediate vulnerable or outdated third-party packages before merge.

**Reasoning:**

A large portion of modern security risk does not originate from first-party code, but from third-party dependencies [17]. Even if your internal code is perfectly written, a vulnerable library version can introduce critical vulnerabilities into production. Automated dependency management tools like Dependabot are continuously monitoring vulnerability databases and ensuring the packages used are free of known vulnerabilities, so as to mitigate software supply-chain attacks. 

**Good Example:**

In your repository, go to:

Settings -> Security -> Advanced Security -> Dependabot -> Enable Dependabot Alerts. 

And then go to:

Security -> Vulnerability Alerts -> Dependabot. 

**Bad Example:**

```
You are an experienced coding agent, please verify the dependency versions for me: [path-to-file].
```

### Guideline 3: Enforce Test Quality over Coverage [18]

**Description:**

Require automated tests to run in CI and enforce a minimum, meaningful test coverage threshold as a mandatory condition before merging. In addition, manually review test quality — do not rely solely on coverage metrics.

**Reasoning:**

While static analysis and dependency scanning catch structural and known vulnerability issues, they do not validate runtime behavior. Tests provide behavioral guarantees and protect against regressions.

**Good Example:**

Ensure good testing principles like Blackbox testing, Whitebox testing, MC/DC testing, mutation test etc, in alignment with project-specific conventions and risk expectations. Establish a team-wide test coverage as a threshold. 

**Bad Example:**

Writing meaningless test cases to inflate high test coverage.

---

### Guideline N: [Short, Actionable Title]
(Repeat the same structure for each guideline.)

---

## 3. Guidelines from LLMs

> **Note:** Guidelines should be actionable, specific, and usable during real coding tasks.

### Guideline 1: Keep Pull Requests Small and Focused
**Description:**  
Require pull requests to contain one logical change (e.g., a single feature, fix, or refactor). Avoid bundling unrelated modifications in the same PR.

**Reasoning:**  
Smaller PRs reduce cognitive load, improve defect detection, and make reviews faster and more thorough. Large, mixed-purpose PRs hide risk and often receive superficial approval—especially in AI-accelerated workflows where diffs can grow quickly.

In modern AI-assisted workflows, this becomes even more important:
- LLMs may generate large diffs quickly.
- Reviewers may assume AI-generated changes are safe.
- Subtle logic issues can hide inside extensive formatting or refactoring changes.

**Good Example:**
PR: “Fix null check in authentication flow”
– Small logic change
– Corresponding test updates
– No unrelated refactoring

**Bad Example:**
PR: “Refactor + Cleanup + Add feature + Upgrade deps”

---

### Guideline 2: [Short, Actionable Title]
(Repeat the same structure for each guideline.)

---

### Guideline N: [Short, Actionable Title]
(Repeat the same structure for each guideline.)

---

## 4. References


[1] Alami, Adam, et al. ‘Accountability in Code Review: The Role of Intrinsic Drivers and the Impact of LLMs’. ACM Trans. Softw. Eng. Methodol., vol. 34, no. 8, Association for Computing Machinery, Oct. 2025, https://doi.org/10.1145/3721127.

[2] Haider, Md Asif, et al. "Prompting and fine-tuning large language models for automated code review comment generation." arXiv preprint arXiv:2411.10129 (2024).

[3] Aðalsteinsson, Fannar Steinn, et al. "Rethinking code review workflows with llm assistance: An empirical study." 2025 ACM/IEEE International Symposium on Empirical Software Engineering and Measurement (ESEM). IEEE, 2025.
[4] Collante, Antonio, et al. "The Impact of Large Language Models (LLMs) on Code Review Process." arXiv preprint arXiv:2508.11034 (2025).

[5] Kawalerowicz, Marcin, Marcin Pietranik, and Krzysztof Stępniak. "LLMs as Code Review Agents: A Rapid Review and Experimental Evaluation with Human Expert Judges." International Conference on Computational Collective Intelligence. Cham: Springer Nature Switzerland, 2025.

[6] Cihan, Umut, et al. "Evaluating Large Language Models for Code Review." arXiv preprint arXiv:2505.20206 (2025).

[7] Cihan, Umut, et al. "Automated code review in practice." 2025 IEEE/ACM 47th International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP). IEEE, 2025.

[8] Shwer, Elle, et al. “Code Review in the Age of AI: Why Developers Will Always Own the Merge Button.” The GitHub Blog, 14 July 2025, github.blog/ai-and-ml/generative-ai/code-review-in-the-age-of-ai-why-developers-will-always-own-the-merge-button.

[9] Gopu, Ria, et al. “Unlocking the Full Power of Copilot Code Review: Master Your Instructions Files.” The GitHub Blog, 15 Nov. 2025, github.blog/ai-and-ml/unlocking-the-full-power-of-copilot-code-review-master-your-instructions-files.

[10] “Using GitHub Copilot Code Review - GitHub Docs.” GitHub Docs, docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review.

[11] Mahajan, Sonal. “uReview: Scalable, Trustworthy GenAI for Code Review at Uber | Uber Blog.” Uber Blog, 3 Sept. 2025, www.uber.com/en-CA/blog/ureview.

[12] Qian, Callan Lamb Christoph Hamsen, Julien Doutre, Jason Foral, Kassen. “Detecting Malicious Pull Requests at Scale With LLMs | Datadog.” Datadog, 21 Oct. 2025, www.datadoghq.com/blog/engineering/malicious-pull-requests.

[13] Przymus, Piotr, and Thomas Durieux. "Wolves in the repository: A software engineering analysis of the xz utils supply chain attack." 2025 IEEE/ACM 22nd International Conference on Mining Software Repositories (MSR). IEEE, 2025.

[14] Vadayath, Jayakrishna, et al. "Arbiter: Bridging the static and dynamic divide in vulnerability discovery on binary programs." 31st USENIX Security Symposium (USENIX Security 22). 2022.

[15] Owen, R. (2025, November 14). Your security scans are missing Critical Vulnerabilities—Here’s Why. NetRise. https://www.netrise.io/xiot-security-blog/why-scanners-miss-vulnerabilities.

[16] Liu, Nelson F., et al. "Lost in the middle: How language models use long contexts." Transactions of the association for computational linguistics 12 (2024): 157-173.

[17] Ayala, Jessy, Yu-Jye Tung, and Joshua Garcia. "A {Mixed-Methods} Study of {Open-Source} Software Maintainers On Vulnerability Management and Platform Security Features." 34th USENIX Security Symposium (USENIX Security 25). 2025.

[18] Shimizu, Sasara, and Yoshiki Higo. "Coverage Isn’t Enough: SBFL-Driven Insights into Manually Created vs. Automatically Generated Tests." International Conference on Product-Focused Software Process Improvement. Cham: Springer Nature Switzerland, 2025.

---

