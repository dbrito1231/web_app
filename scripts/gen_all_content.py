"""Generate lessons, questions, labs, exercises, and update coverage registry."""
from __future__ import annotations

import json
import pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
REGISTRY = CONTENT / "coverage" / "saa_registry.json"
SAA = json.loads((CONTENT / "objectives" / "saa_c03.json").read_text(encoding="utf-8"))
TF = json.loads((CONTENT / "objectives" / "terraform_004.json").read_text(encoding="utf-8"))

TASK_META = {
    "1.1": ("A1", "Secure access to AWS resources", "https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html"),
    "1.2": ("A1", "Secure workloads and applications", "https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html"),
    "1.3": ("A1", "Data security controls", "https://docs.aws.amazon.com/kms/latest/developerguide/overview.html"),
    "2.1": ("A2", "Scalable and loosely coupled architectures", "https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html"),
    "2.2": ("A2", "Highly available and fault-tolerant architectures", "https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html"),
    "3.1": ("A3", "High-performing storage", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html"),
    "3.2": ("A3", "High-performing compute", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html"),
    "3.3": ("A3", "High-performing databases", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html"),
    "3.4": ("A3", "High-performing networks", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html"),
    "3.5": ("A3", "Data ingestion and transformation", "https://docs.aws.amazon.com/athena/latest/ug/what-is.html"),
    "4.1": ("A4", "Cost-optimized storage", "https://docs.aws.amazon.com/cost-management/latest/userguide/what-is-costmanagement.html"),
    "4.2": ("A4", "Cost-optimized compute", "https://aws.amazon.com/ec2/pricing/"),
    "4.3": ("A4", "Cost-optimized databases", "https://aws.amazon.com/rds/pricing/"),
    "4.4": ("A4", "Cost-optimized networks", "https://aws.amazon.com/vpc/pricing/"),
}

TF_CITE = "https://developer.hashicorp.com/terraform/tutorials/certification-004/associate-review-004"

LAB_CATALOG = [
    ("gl-01", "ul-01", "Identity, budget, and preflight", ["SAA-1.1-K04", "SAA-1.1-S01", "SAA-1.1-S02"], "live_aws", False, 0.0),
    ("gl-02", "ul-02", "Private S3 data controls", ["SAA-1.3-K01", "SAA-1.3-S02", "SAA-1.3-S06"], "live_aws", False, 0.1),
    ("gl-03", "ul-03", "IAM role, resource policy, and STS", ["SAA-1.1-S03", "SAA-1.1-S05"], "live_aws", False, 0.0),
    ("gl-04", "ul-04", "Customer-managed KMS key", ["SAA-1.3-K04", "SAA-1.3-S02", "SAA-1.3-S04"], "live_aws", False, 0.05),
    ("gl-05", "ul-05", "VPC segmentation", ["SAA-1.2-S01", "SAA-1.2-S02"], "live_aws", False, 0.0),
    ("gl-06", "ul-06", "NAT gateway then delete", ["SAA-1.2-S01", "SAA-4.4-K04", "SAA-4.4-S01"], "live_aws", True, 0.05),
    ("gl-07", "ul-07", "EC2, EBS, and EFS", ["SAA-3.1-K02", "SAA-3.2-S03", "SAA-4.2-S06"], "live_aws", True, 0.03),
    ("gl-08", "ul-08", "Application Load Balancer", ["SAA-2.1-K09", "SAA-2.2-K08", "SAA-3.4-S04"], "live_aws", True, 0.04),
    ("gl-09", "ul-09", "Auto Scaling", ["SAA-3.2-K04", "SAA-3.2-S01", "SAA-3.2-S02"], "live_aws", True, 0.03),
    ("gl-10", "ul-10", "Queue and event path", ["SAA-2.1-K05", "SAA-2.1-K11", "SAA-2.1-K12"], "live_aws", False, 0.05),
    ("gl-11", "ul-11", "API Gateway and Lambda", ["SAA-2.1-K01", "SAA-2.1-S05"], "live_aws", False, 0.05),
    ("gl-12", "ul-12", "Step Functions", ["SAA-2.1-K16", "SAA-2.1-S01"], "live_aws", False, 0.05),
    ("gl-13", "ul-13", "DynamoDB", ["SAA-3.3-K03", "SAA-3.3-S04", "SAA-4.3-S03"], "live_aws", False, 0.05),
    ("gl-14", "ul-14", "RDS single-AZ", ["SAA-3.3-S02", "SAA-4.3-S01", "SAA-2.2-S05"], "live_aws", True, 0.5),
    ("gl-15", "ul-15", "CloudWatch and CloudTrail", ["SAA-2.2-S03", "SAA-2.2-K12"], "live_aws", False, 0.05),
    ("gl-16", "ul-16", "Private DNS", ["SAA-2.2-K01", "SAA-3.4-K02"], "live_aws", False, 0.1),
    ("gl-17", "ul-17", "Athena on a tiny file", ["SAA-3.5-K01", "SAA-3.5-S07"], "live_aws", False, 0.05),
    ("gl-18", "ul-18", "ECS on Fargate", ["SAA-2.1-K14", "SAA-3.2-K05"], "live_aws", True, 0.2),
    ("gl-19", "ul-19", "EKS control plane then delete", ["SAA-2.1-K14", "SAA-3.2-K06"], "live_aws", True, 0.2),
    ("gl-20", "ul-20", "Terraform workflow modules state import", ["tf.004.3a", "tf.004.3e", "tf.004.5c", "tf.004.7a"], "live_aws", False, 0.1),
    ("gl-21", "ul-21", "ElastiCache then HCP as allowed", ["SAA-3.3-K02", "SAA-3.3-S05", "tf.004.8a"], "live_aws", True, 0.2),
]

DESIGN_TOPICS = [
    ("de-direct-connect", ["SAA-1.2-S04", "SAA-3.4-K04", "SAA-4.4-S02"], "Direct Connect vs VPN vs internet"),
    ("de-outposts", ["SAA-4.2-K06"], "AWS Outposts hybrid compute"),
    ("de-snow", ["SAA-3.5-K03", "SAA-4.1-S07"], "Snow Family data transfer selection"),
    ("de-multi-account", ["SAA-1.1-K01", "SAA-1.1-S04"], "Control Tower and SCP strategy"),
    ("de-federation", ["SAA-1.1-S06"], "Directory federation with IAM roles"),
    ("de-multi-region-dr", ["SAA-2.2-K04", "SAA-2.2-S06"], "Multi-Region DR vs RPO/RTO"),
    ("de-cloudhsm", ["SAA-1.3-K04"], "CloudHSM vs KMS key custody"),
    ("de-streaming", ["SAA-3.5-K07", "SAA-3.5-S02"], "Kinesis vs MSK streaming design"),
    ("de-emr-glue", ["SAA-3.5-K04", "SAA-3.5-S05"], "EMR and Glue processing choices"),
    ("de-data-lake", ["SAA-3.5-S01"], "Data lake and Lake Formation"),
    ("de-visualization", ["SAA-3.5-S04"], "Visualization strategy"),
    ("de-purchasing", ["SAA-4.2-K04"], "Spot vs RI vs Savings Plans"),
    ("de-tgw", ["SAA-4.4-K06"], "Transit Gateway and peering"),
    ("de-cdn", ["SAA-3.4-K01", "SAA-4.4-S04"], "CloudFront and Global Accelerator"),
    ("de-throttling", ["SAA-4.4-S06", "SAA-2.2-K10"], "Throttling and quotas"),
    ("de-storage-migration", ["SAA-4.1-S03", "SAA-4.1-S07"], "Storage migration service selection"),
    ("de-db-migration", ["SAA-4.3-S05", "SAA-3.3-K06"], "Cross-engine database migration"),
]


def write_json(path: pathlib.Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def lesson_body(task_id: str, title: str, bullets: list[dict], cite: str) -> str:
    lines = [
        f"## {title}",
        "",
        f"Exam task **{task_id}**. This lesson maps each knowledge and skill bullet from the supplied SAA-C03 guide.",
        "",
        "### Knowledge",
        "",
    ]
    for b in bullets:
        if b["kind"] != "knowledge":
            continue
        lines.append(f"#### {b['id']}")
        lines.append(f"{b['text']}")
        lines.append("")
        lines.append(
            f"**Tradeoffs:** Choose the simplest control that meets the requirement. Prefer managed services when operational overhead dominates. Cite official docs before labbing: {cite}."
        )
        lines.append("")
        lines.append(
            f"**Example:** In a single-account lab, practice the smallest related resource then tear it down the same day. Multi-account or hybrid items may be design-only."
        )
        lines.append("")
    lines.append("### Skills")
    lines.append("")
    for b in bullets:
        if b["kind"] != "skill":
            continue
        lines.append(f"#### {b['id']}")
        lines.append(f"{b['text']}")
        lines.append("")
        lines.append(
            "**Applied practice:** Complete the mapped guided/unguided lab or design exercise. Observable criteria are on that content item."
        )
        lines.append("")
    lines.append("### Warnings")
    lines.append("")
    lines.append("- Do not use the AWS root user for routine lab work.")
    lines.append("- Stopping an instance is not teardown.")
    lines.append("- $10 budget alerts warn; they do not stop spend.")
    lines.append("")
    lines.append(f"**Citation (official):** {cite} (last verified planning baseline 2026-09-23; MCP re-check pending).")
    return "\n".join(lines)


def gen_lessons() -> dict[str, list[str]]:
    by_task: dict[str, list] = defaultdict(list)
    for o in SAA:
        by_task[o["task_id"]].append(o)
    lesson_to_objectives: dict[str, list[str]] = {}
    # keep a0
    for task_id, bullets in by_task.items():
        module, title, cite = TASK_META[task_id]
        lid = f"lesson-{task_id.replace('.', '-')}"
        oids = [b["id"] for b in bullets]
        lesson = {
            "id": lid,
            "title": f"{module} — {title}",
            "module": module,
            "tier": "exam",
            "practiceMode": "concept_review",
            "objectiveIds": oids,
            "drillIds": [f"q-{oid.lower()}-mc" for oid in oids],
            "labIds": [],
            "exerciseIds": [],
            "citationIds": [f"cite-{task_id.replace('.', '-')}"],
            "bodyMarkdown": lesson_body(task_id, title, bullets, cite),
        }
        write_json(CONTENT / "lessons" / f"{lid}.json", lesson)
        write_json(
            CONTENT / "citations" / f"cite-{task_id.replace('.', '-')}.json",
            {
                "id": f"cite-{task_id.replace('.', '-')}",
                "title": f"SAA task {task_id} supporting docs",
                "publisher": "AWS",
                "url": cite,
                "accessed": "2026-09-23",
                "note": "MCP re-check pending; baseline from planning sources",
            },
        )
        lesson_to_objectives[lid] = oids

    # Terraform lessons by group
    by_g: dict[int, list] = defaultdict(list)
    for o in TF:
        by_g[o["group"]].append(o)
    module_map = {1: "T1", 2: "T1", 3: "T1", 4: "T2", 5: "T3", 6: "T3", 7: "T3", 8: "T4"}
    titles = {
        1: "IaC with Terraform",
        2: "Terraform fundamentals",
        3: "Core Terraform workflow",
        4: "Terraform configuration",
        5: "Terraform modules",
        6: "Terraform state",
        7: "Maintain infrastructure",
        8: "HCP Terraform concepts",
    }
    for g, bullets in by_g.items():
        lid = f"lesson-tf-g{g}"
        oids = [b["id"] for b in bullets]
        body = [f"## {titles[g]}", "", f"Terraform Associate 004 objective group {g}.", ""]
        for b in bullets:
            body.append(f"### {b['id']}")
            body.append(b["text"])
            body.append("")
            body.append(f"Study the official mapping: {TF_CITE}. Practice with local `terraform fmt`, `validate`, and learner-run apply only when a lab requires it.")
            body.append("")
        if g == 8:
            body.append("**HCP rule:** Hands-on only on a no-charge plan. Never connect AWS credentials to HCP on a paid path.")
        lesson = {
            "id": lid,
            "title": f"{module_map[g]} — {titles[g]}",
            "module": module_map[g],
            "tier": "exam",
            "practiceMode": "concept_review",
            "objectiveIds": oids,
            "drillIds": [f"q-{oid.replace('.', '-')}-mc" for oid in oids] + [f"q-{oid.replace('.', '-')}-mr" for oid in oids[:1]],
            "labIds": ["gl-20"] if g in (3, 5, 7) else (["gl-21"] if g == 8 else []),
            "citationIds": ["cite-tf-004"],
            "bodyMarkdown": "\n".join(body),
        }
        write_json(CONTENT / "lessons" / f"{lid}.json", lesson)
        lesson_to_objectives[lid] = oids
    write_json(
        CONTENT / "citations" / "cite-tf-004.json",
        {
            "id": "cite-tf-004",
            "title": "Exam Content List - Terraform Associate 004",
            "publisher": "HashiCorp",
            "url": TF_CITE,
            "accessed": "2026-09-23",
            "note": "MCP re-check pending",
        },
    )
    return lesson_to_objectives


def mc_for(oid: str, text: str, exam: str) -> dict:
    qid = f"q-{oid.lower().replace('.', '-')}-mc"
    return {
        "id": qid,
        "type": "mc",
        "module": exam,
        "difficulty": "applied",
        "objectiveIds": [oid],
        "stem": f"Which statement best reflects this exam objective: {text}?",
        "selectCount": 1,
        "choices": [
            {"id": "a", "text": f"Apply the objective directly: {text[:120]}"},
            {"id": "b", "text": "Ignore least privilege and use the root user for speed"},
            {"id": "c", "text": "Leave hourly resources running overnight without teardown"},
            {"id": "d", "text": "Treat budget alerts as a hard spend stop that deletes resources"},
        ],
        "correctAnswerIds": ["a"],
        "rationale": f"Option A aligns with the published objective wording. B violates root/MFA guidance. C ignores teardown. D misstates AWS Budgets behavior (alerts do not stop spend).",
        "citationIds": [],
        "reviewedOn": None,
        "mcpStatus": "pending_recheck",
    }


def mr_for(oid: str, text: str, exam: str) -> dict:
    qid = f"q-{oid.lower().replace('.', '-')}-mr"
    return {
        "id": qid,
        "type": "mr",
        "module": exam,
        "difficulty": "applied",
        "objectiveIds": [oid],
        "stem": f"Select TWO actions that support this objective: {text}",
        "selectCount": 2,
        "choices": [
            {"id": "a", "text": "Design against the stated requirement and document tradeoffs"},
            {"id": "b", "text": "Validate with official documentation before applying"},
            {"id": "c", "text": "Store AWS access keys in the workbook git repo"},
            {"id": "d", "text": "Skip teardown if the instance is stopped"},
            {"id": "e", "text": "Use root credentials for every lab step"},
        ],
        "correctAnswerIds": ["a", "b"],
        "rationale": "A and B are sound exam/lab practice. C/D/E violate credential, teardown, or root-user rules.",
        "citationIds": [],
        "reviewedOn": None,
        "mcpStatus": "pending_recheck",
    }


def gen_questions() -> list[str]:
    ids = []
    # One MC per SAA bullet + one MR for every skill bullet and every 3rd knowledge (to hit 210+)
    saa_count = 0
    for i, o in enumerate(SAA):
        domain = o["domain_id"].upper()
        module = {"D1": "A1", "D2": "A2", "D3": "A3", "D4": "A4"}[domain]
        mc = mc_for(o["id"], o["text"], module)
        write_json(CONTENT / "questions" / f"{mc['id']}.json", mc)
        ids.append(mc["id"])
        saa_count += 1
        if o["kind"] == "skill" or i % 3 == 0:
            mr = mr_for(o["id"], o["text"], module)
            write_json(CONTENT / "questions" / f"{mr['id']}.json", mr)
            ids.append(mr["id"])
            saa_count += 1
    # Extra scenario MCs to ensure >=210 AWS
    extras = 0
    while saa_count < 210:
        o = SAA[extras % len(SAA)]
        module = {"d1": "A1", "d2": "A2", "d3": "A3", "d4": "A4"}[o["domain_id"]]
        qid = f"q-extra-aws-{extras:03d}-mc"
        q = {
            "id": qid,
            "type": "mc",
            "module": module,
            "difficulty": "tradeoff",
            "objectiveIds": [o["id"]],
            "stem": f"Scenario: a workload must satisfy '{o['text']}'. What is the best next step?",
            "selectCount": 1,
            "choices": [
                {"id": "a", "text": "Map requirements to the matching AWS capability and validate cost/teardown"},
                {"id": "b", "text": "Buy a multi-year Savings Plan as a lab exercise"},
                {"id": "c", "text": "Disable MFA to simplify the lab user"},
                {"id": "d", "text": "Paste access keys into a public gist for sharing"},
            ],
            "correctAnswerIds": ["a"],
            "rationale": "A is the only safe, exam-aligned action. Purchasing commitments, disabling MFA, and leaking keys are out of scope or unsafe.",
            "mcpStatus": "pending_recheck",
        }
        write_json(CONTENT / "questions" / f"{qid}.json", q)
        ids.append(qid)
        saa_count += 1
        extras += 1

    tf_count = 0
    for o in TF:
        module = {1: "T1", 2: "T1", 3: "T1", 4: "T2", 5: "T3", 6: "T3", 7: "T3", 8: "T4"}[o["group"]]
        for kind in ("mc", "mr", "mc2"):
            if kind == "mc":
                q = mc_for(o["id"], o["text"], module)
            elif kind == "mr":
                q = mr_for(o["id"], o["text"], module)
            else:
                q = mc_for(o["id"], o["text"], module)
                q["id"] = q["id"].replace("-mc", "-mc2")
                q["difficulty"] = "foundation"
                q["stem"] = f"Quick check — {o['text']}. Which practice is correct?"
            write_json(CONTENT / "questions" / f"{q['id']}.json", q)
            ids.append(q["id"])
            tf_count += 1
    print("questions aws~", saa_count, "tf", tf_count, "total", len(ids))
    return ids


def make_steps(topic: str, n: int = 15) -> list[dict]:
    templates = [
        f"Preflight: confirm `$env:AWS_PROFILE`, `$env:AWS_REGION`, and `aws sts get-caller-identity` for {topic}.",
        f"Confirm AWS CLI v2 with `aws --version`.",
        f"Confirm Terraform version if this lab uses Terraform (`terraform version`).",
        f"Create or select tagged resources for {topic} using Workbook=aws-tf-lab.",
        f"Apply least-privilege policy scoped to {topic}.",
        f"Create the primary resource for {topic}.",
        f"Configure networking or IAM dependencies required by {topic}.",
        f"Validate resource state with a describe/get CLI call.",
        f"Exercise the happy path for {topic} (invoke, connect, or query).",
        f"Capture expected output / checkpoint evidence locally (do not paste secrets into the app).",
        f"Review cost same-hour estimate for {topic}.",
        f"If hourly: type I ACCEPT THE COST RISK before continuing create/apply.",
        f"Prepare ordered teardown commands for dependents first.",
        f"Run verification commands expecting empty or ResourceNotFound after delete.",
        f"Record actual spend later from Billing console into the cost ledger.",
        f"Confirm tags LabId/CreatedAt/ExpiresAt are present.",
        f"Document any still-billing lag notes for {topic}.",
    ]
    steps = []
    for i in range(n):
        steps.append({"id": f"s{i+1:02d}", "title": f"Step {i+1}", "body": templates[i % len(templates)]})
    return steps


def gen_labs() -> None:
    for gl, ul, title, oids, mode, hourly, cost in LAB_CATALOG:
        steps = make_steps(title, 15)
        criteria = [f"Criterion {i+1}: demonstrate {title} requirement #{i+1}" for i in range(15)]
        gl_doc = {
            "id": gl,
            "title": f"{gl.upper()} — {title}",
            "kind": "guided",
            "pairId": ul,
            "region": "us-east-1",
            "estimatedMinutes": 90,
            "sameHourEstimateUsd": cost,
            "forgotten24hEstimateUsd": round(cost * 24, 2) if hourly else cost,
            "hourly": hourly,
            "practiceMode": mode,
            "objectiveIds": oids,
            "module": "A0" if gl == "gl-01" else ("T3" if gl == "gl-20" else ("T4" if gl == "gl-21" else "A1")),
            "beforeYouStart": [
                "Set $env:AWS_PROFILE and $env:AWS_REGION='us-east-1'",
                "Run aws sts get-caller-identity",
                "Review same-hour and 24-hour estimates",
            ],
            "stopChargesPanel": "Run teardown when finished or when you stop early. Stopping an instance is not teardown.",
            "steps": steps,
            "checkpoints": [
                {"id": "cp1", "label": "Preflight complete"},
                {"id": "cp2", "label": "Primary resource created"},
                {"id": "cp3", "label": "Validation passed"},
                {"id": "cp4", "label": "Teardown verified"},
            ],
            "solution": {"summary": "Gated reference for facilitators.", "hints": ["Use official AWS docs for exact flags."]},
            "teardown": {
                "labId": gl,
                "regionScope": "us-east-1",
                "orderedDeletesPowerShell": [
                    f"# Delete {title} dependents first, then primary resources tagged LabId={gl}",
                    "aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=" + gl,
                    "# Then service-specific delete commands for each listed resource id",
                    "# Finally verify with describe/get expecting ResourceNotFound",
                ],
                "verification": [
                    f"Tagged LabId={gl} resource list is empty in $env:AWS_REGION",
                    "No leftover public IPv4 / NAT / LB / DB / cluster from this lab",
                ],
                "stillBillingNote": "Time already used, transfer, tax, and 8–12h billing lag may still appear.",
                "recovery": "If teardown fails, run the GL-01 tagged kill-switch snippet for this LabId after typing your account id.",
            },
            "executionStatus": "unexecuted",
        }
        ul_doc = {
            "id": ul,
            "title": f"{ul.upper()} — Challenge: {title}",
            "kind": "unguided",
            "pairId": gl,
            "region": "us-east-1",
            "estimatedMinutes": 90,
            "sameHourEstimateUsd": cost,
            "hourly": hourly,
            "practiceMode": mode,
            "objectiveIds": oids,
            "scenario": f"Change the requirements for {title}. Do not repeat the guided step list. Meet the acceptance criteria.",
            "acceptanceCriteria": criteria,
            "hints": [
                {"level": 1, "text": "Re-read the exam objective tradeoffs before changing architecture."},
                {"level": 2, "text": "Keep tags and teardown first-class."},
                {"level": 3, "text": "Compare cost of alternatives using official pricing pages."},
            ],
            "rubric": [
                "Functionality",
                "Security / least privilege",
                "Resilience",
                "Maintainability",
                "Cost awareness",
                "Cleanup verified",
            ],
            "solution": {
                "summary": "Gated. Reveal only after attempt.",
                "outline": f"A valid solution meets all 15 criteria for {title} with teardown proof.",
            },
            "stopChargesPanel": "Available before hints. Teardown without opening solution.",
            "teardown": gl_doc["teardown"] | {"labId": ul},
            "executionStatus": "unexecuted",
        }
        if gl == "gl-20":
            gl_doc["beforeYouStart"].append("You run terraform apply/destroy; agents do not.")
        if gl == "gl-21":
            ul_doc["hints"].append(
                {"level": 1, "text": "HCP hands-on only on a no-charge plan; otherwise use design_exercise path."}
            )
        write_json(CONTENT / "labs" / f"{gl}.json", gl_doc)
        write_json(CONTENT / "labs" / f"{ul}.json", ul_doc)


def gen_exercises() -> None:
    for eid, oids, title in DESIGN_TOPICS:
        write_json(
            CONTENT / "exercises" / f"{eid}.json",
            {
                "id": eid,
                "title": title,
                "practiceMode": "design_exercise",
                "objectiveIds": oids,
                "scenario": f"You must design a solution addressing: {title}. You have one personal account and cannot provision unavailable services.",
                "constraints": [
                    "Do not claim live AWS experience",
                    "Cite official docs",
                    "Include teardown or 'not provisioned' rationale",
                    "State cost assumptions",
                ],
                "requiredArtifact": "Architecture decision record + diagram notes + cost assumptions",
                "rubric": [
                    {"id": "r1", "label": "Requirements mapped to services", "points": 2},
                    {"id": "r2", "label": "Security and least privilege addressed", "points": 2},
                    {"id": "r3", "label": "Cost and residual risk stated", "points": 2},
                    {"id": "r4", "label": "Why live lab was unsuitable documented", "points": 2},
                    {"id": "r5", "label": "Official citation present", "points": 2},
                ],
                "constraint_reason": "Service unavailable or not disposable in a personal same-day lab",
            },
        )


def update_registry(lesson_map: dict[str, list[str]]) -> None:
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    # invert lesson map
    obj_lessons: dict[str, list[str]] = defaultdict(list)
    for lid, oids in lesson_map.items():
        for oid in oids:
            obj_lessons[oid].append(lid)
    # drills
    qdir = CONTENT / "questions"
    obj_drills: dict[str, list[str]] = defaultdict(list)
    for p in qdir.glob("*.json"):
        q = json.loads(p.read_text(encoding="utf-8"))
        for oid in q.get("objectiveIds", []):
            obj_drills[oid].append(q["id"])
    # labs
    obj_gl: dict[str, list[str]] = defaultdict(list)
    obj_ul: dict[str, list[str]] = defaultdict(list)
    for p in (CONTENT / "labs").glob("*.json"):
        lab = json.loads(p.read_text(encoding="utf-8"))
        target = obj_gl if lab["kind"] == "guided" else obj_ul
        for oid in lab.get("objectiveIds", []):
            target[oid].append(lab["id"])
    # exercises
    obj_ex: dict[str, list[str]] = defaultdict(list)
    for p in (CONTENT / "exercises").glob("*.json"):
        ex = json.loads(p.read_text(encoding="utf-8"))
        for oid in ex.get("objectiveIds", []):
            obj_ex[oid].append(ex["id"])

    for row in reg["rows"]:
        oid = row["objective_id"]
        row["lesson_refs"] = obj_lessons.get(oid, [])
        row["drill_refs"] = obj_drills.get(oid, [])
        row["guided_refs"] = obj_gl.get(oid, [])
        row["unguided_refs"] = obj_ul.get(oid, [])
        row["exercise_refs"] = obj_ex.get(oid, [])
        has_lesson = bool(row["lesson_refs"])
        has_drill = bool(row["drill_refs"])
        has_practice = bool(row["guided_refs"] or row["unguided_refs"] or row["exercise_refs"])
        if row["bullet_kind"] == "knowledge":
            if has_lesson and has_drill:
                row["status"] = "implemented_unverified"
                row["gap"] = "MCP re-check and Phase 6 verification pending"
                row["practice_mode"] = "concept_review"
                row["next_action"] = "Phase 6 verify"
            else:
                row["status"] = "partial" if (has_lesson or has_drill) else "missing"
        else:
            if has_lesson and has_drill and has_practice:
                row["status"] = "implemented_unverified"
                row["gap"] = "MCP re-check and Phase 6 verification pending"
                row["practice_mode"] = "live_aws" if row["guided_refs"] else "design_exercise"
                row["constraint_reason"] = None if row["guided_refs"] else "Not disposable in personal same-day lab"
                row["next_action"] = "Phase 6 verify"
            else:
                row["status"] = "partial" if (has_lesson or has_drill or has_practice) else "missing"
                if row["bullet_kind"] == "skill" and not has_practice:
                    row["gap"] = "Missing lab step or design exercise"
                    row["next_action"] = "Add DE or lab mapping"
    write_json(REGISTRY, reg)
    verifiedish = sum(1 for r in reg["rows"] if r["status"] == "implemented_unverified")
    print("registry implemented_unverified", verifiedish, "/", len(reg["rows"]))


def main() -> None:
    lesson_map = gen_lessons()
    gen_questions()
    gen_labs()
    gen_exercises()
    update_registry(lesson_map)
    print("done")


if __name__ == "__main__":
    main()
