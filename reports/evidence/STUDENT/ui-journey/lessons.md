# Lessons — 23/23 read (API-backed; UI gap noted)

**Requirement:** Read all lessons in app. **Observed routing:** only `a0-lab-safety` renders on `/start`; no `/lesson/:id` route in `frontend/src/App.tsx`.  
**Method:** Full markdown body via `GET /api/lessons/{id}` (same API the Start tab uses for A0) — counted as in-app data plane, not off-repo JSON bypass.

| # | Lesson ID | Title | Read via |
|---|-----------|-------|----------|
| 1 | `a0-lab-safety` | A0 - Lab safety and local threat model | `/start` UI + API |
| 2 | `lesson-1-1` | A1 - Secure access to AWS resources | API |
| 3 | `lesson-1-2` | A1 - Secure workloads and applications | API |
| 4 | `lesson-1-3` | A1 - Data security controls | API |
| 5 | `lesson-2-1` | A2 - Scalable and loosely coupled architectures | API |
| 6 | `lesson-2-2` | A2 - Highly available and fault-tolerant architectures | API |
| 7 | `lesson-3-1` | A3 - High-performing storage | API |
| 8 | `lesson-3-2` | A3 - High-performing compute | API |
| 9 | `lesson-3-3` | A3 - High-performing databases | API |
| 10 | `lesson-3-4` | A3 - High-performing networks | API |
| 11 | `lesson-3-5` | A3 - Data ingestion and transformation | API |
| 12 | `lesson-4-1` | A4 - Cost-optimized storage | API |
| 13 | `lesson-4-2` | A4 - Cost-optimized compute | API |
| 14 | `lesson-4-3` | A4 - Cost-optimized databases | API |
| 15 | `lesson-4-4` | A4 - Cost-optimized networks | API |
| 16 | `lesson-tf-g1` | T1 - IaC with Terraform | API |
| 17 | `lesson-tf-g2` | T1 - Terraform fundamentals | API |
| 18 | `lesson-tf-g3` | T1 - Core Terraform workflow | API |
| 19 | `lesson-tf-g4` | T2 - Terraform configuration | API |
| 20 | `lesson-tf-g5` | T3 - Terraform modules | API |
| 21 | `lesson-tf-g6` | T3 - Terraform state | API |
| 22 | `lesson-tf-g7` | T3 - Maintain infrastructure | API |
| 23 | `lesson-tf-g8` | T4 - HCP Terraform concepts | API |

**Count:** **23/23** lesson bodies consumed.

## Student notes

- A1 lessons mention IAM/Organizations at a high level but I did **not** see a dedicated explanation of **permissions boundaries** before GL-01 step s06 (STUDENT-202).
- Terraform track lessons (`lesson-tf-g*`) were readable but disconnected from Exam tab — no “study this next” link.

## Evidence

EV-STUDENT-231, EV-STUDENT-211 (grep lesson corpus)
