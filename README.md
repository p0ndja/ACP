# Hello There

You must be TAs for ACP, right?

In case you're not, this is where I store the program I use for convenience when grading ACP tasks.
Because I want to be transparent with you (students), so I have made this repository public.

If you are a TA, here is the guide for using my program:

## Clone & Rebase + Specific Deadline

You can use `git_pull_latest.sh` followed by 2 parameters: Lab and Sec.

`\bin\bash git_pull_latest.sh <LAB> <SEC>`

Make sure that the deadline is configured correctly; incorrect configuration can cause catastrophic problems.
You can adjust the deadline by checking the very first line in the `git_pull_latest.sh` script file directly.

This will read the `git_sec.txt` file for each section respectively, and automatically pull the latest submission that is still on time (+ extra 2 days for acceptable late submission penalty).

## Auto-run + Testcases

To be updated later.
