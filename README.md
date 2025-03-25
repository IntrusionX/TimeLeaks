TimeLeaks
 is a tool for pentesters and bug bounty hunters that extracts URLs from the Wayback Machine and classifies them based on GF-patterns for common vulnerabilities such as:

SQL Injection (SQLi)

Remote Code Execution (RCE)

Cross-Site Scripting (XSS)

Server-Side Request Forgery (SSRF)

This tool helps you quickly categorize URLs from archived websites, identifying potential vulnerability types based on predefined patterns.

How to Run:

git clone https://github.com/IntrusionX/TimeLeaks.git

cd TimeLeaks

Set up the tool:


chmod +x setup.sh

Install dependencies:


./setup.sh

Run the tool:

bash
Copy
python3 tool.py example.com
The tool will retrieve URLs from the Wayback Machine and classify them based on the GF-patterns for SQLi, RCE, XSS, SSRF
