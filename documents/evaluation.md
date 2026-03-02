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

### Problem C: Pull Request Supply Chain Review

**Evaluation Description:**  
This problem will not likely be resolved by simply letting LLMs inspect the dependency files before and after PR. LLMs are not designed to reliably reason over large, highly-structured lockfile. A reasonable process is to apply dependency management tools like Dependabot and/or dependency-review-action@v4 for identifying vulnerable packages. 
In this PR, the package "multer": "2.1.0" is changed to "multer": "2.0.2". 

However, multer package versions < 2.1.0 are known to be severely vulnerable to Denial of Service attacks (CVE-2026-3304). More details can be found on the National Vulnerability Database (NVD)'s official website [https://nvd.nist.gov/vuln/detail/CVE-2026-3304](https://nvd.nist.gov/vuln/detail/CVE-2026-3304), and from the table below:

|             | CVE-2026-3304           |
|-------------|-------------------------------------|
| Severity   | High |
| CVSS Score | 8.7 |
|  Description  | Multer is a node.js middleware for handling `multipart/form-data`. A vulnerability in Multer prior to version 2.1.0 allows an attacker to trigger a Denial of Service (DoS) by sending malformed requests, potentially causing resource exhaustion. Users should upgrade to version 2.1.0 to receive a patch. No known workarounds are available.                                    |
| NVD Published Date | 02/27/2026 |
| Attack Vector | Network |
| Attack Complexity | Low |
| Attack Requirement | None |
| Privileges Required | None | 
| User Interaction | None |
| Related CWE | CWE-459 Incomplete Cleanup | 




## 3. References

[1]  
[2] 

---

