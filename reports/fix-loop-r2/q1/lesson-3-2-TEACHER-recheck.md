# Teacher re-check: lesson 3.2

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files).

**Teacher re-check of lesson 3.2 (`content/lessons/lesson-3-2.json`, commit `db714a6`)**

1. **TEACHER-L32-001:** Gone. K04 now reads: "Because Spot capacity can be reclaimed, Amazon EC2 sends a **two-minute Spot Instance interruption notice** as an EventBridge event and an instance metadata item before interrupting a Spot Instance, and it can send an earlier **rebalance recommendation**..." Clear, student-facing, and placed right after the mixed-instances-policy sentence where a drill would test it. Confirmed both phrases are present in the body via direct file read and grep.

2. **Second-role check, AWS-L32-001 to 003:**
   - AWS-L32-001 (Graviton citation): independently fetched `prescriptive-guidance/latest/optimize-costs-microsoft-workloads/right-size-selection.html` via the AWS Documentation MCP. It states verbatim: "current Graviton processors [are] 20 percent cheaper than their Intel counterparts, but they also deliver a 20 percent or greater performance boost" — matches the lesson's S03 sentence and the citation's `note` exactly. Confirmed accurate.
   - AWS-L32-003 (Compute Optimizer scope): independently fetched `compute-optimizer/latest/ug/what-is-compute-optimizer.html`. Its supported-resources list includes EC2, ASG, EBS, Lambda, ECS-on-Fargate (the compute-adjacent subset the lesson names) plus Aurora/RDS, DynamoDB, ElastiCache, MemoryDB, DocumentDB, NAT Gateway, WorkSpaces, SageMaker, and commercial software licenses. The added S02 clause "(it also covers several database, cache, and other resource types beyond compute)" is accurate and not an overreach.

3. **Format and lint:**
   - Single-asterisk spans: 0
   - `drillIds`: 16, all resolve to existing question files
   - `citationIds`: all 19 resolve to existing citation files
   - `backend\.venv\Scripts\python.exe scripts\content_lint.py` → **PASS** (questions 429, aws 310, tf 119, labs 21+21, lessons 23)

No new issues found — nothing to log as TEACHER-L32-R-###.

**Lesson 3.2: approve for question writing**

Overall: approve
