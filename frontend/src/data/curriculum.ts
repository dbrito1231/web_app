import type { CSSProperties } from 'react';

export type ModuleColor = 'd1' | 'd2' | 'd3' | 'd4' | 'd5' | 'd6';

export interface CurriculumLabRef {
  id: string;
  title: string;
  chip: string;
}

export interface CurriculumGroup {
  id: string;
  title: string;
  labs: CurriculumLabRef[];
}

export interface CurriculumModule {
  id: string;
  pill: string;
  title: string;
  color: ModuleColor;
  weight: number;
  groups: CurriculumGroup[];
}

export const DOMAIN_STYLE: Record<ModuleColor, CSSProperties> = {
  d1: { ['--dc' as string]: 'var(--d1)', ['--dsoft' as string]: 'var(--d1-soft)', ['--mc' as string]: 'var(--d1)' },
  d2: { ['--dc' as string]: 'var(--d2)', ['--dsoft' as string]: 'var(--d2-soft)', ['--mc' as string]: 'var(--d2)' },
  d3: { ['--dc' as string]: 'var(--d3)', ['--dsoft' as string]: 'var(--d3-soft)', ['--mc' as string]: 'var(--d3)' },
  d4: { ['--dc' as string]: 'var(--d4)', ['--dsoft' as string]: 'var(--d4-soft)', ['--mc' as string]: 'var(--d4)' },
  d5: { ['--dc' as string]: 'var(--d5)', ['--dsoft' as string]: 'var(--d5-soft)', ['--mc' as string]: 'var(--d5)' },
  d6: { ['--dc' as string]: 'var(--d6)', ['--dsoft' as string]: 'var(--d6-soft)', ['--mc' as string]: 'var(--d6)' },
};

/** Static curriculum map; labs appear in the UI only when present in /api/content/summary. */
export const CURRICULUM: CurriculumModule[] = [
  {
    id: 'A0',
    pill: '0.0',
    title: 'Lab safety',
    color: 'd1',
    weight: 0,
    groups: [
      {
        id: 'A0.1',
        title: 'Safety and preflight',
        labs: [
          { id: 'gl-01', title: 'Identity, budget, and preflight', chip: 'GL-01' },
          { id: 'ul-01', title: 'Challenge: Identity, budget, and preflight', chip: 'UL-01' },
        ],
      },
    ],
  },
  {
    id: 'A1',
    pill: '1.0',
    title: 'Secure architectures',
    color: 'd2',
    weight: 30,
    groups: [
      { id: 'A1.1', title: 'Secure access', labs: [{ id: 'gl-02', title: 'Private S3 data controls', chip: 'GL-02' }, { id: 'ul-02', title: 'Challenge: Private S3 data controls', chip: 'UL-02' }, { id: 'gl-03', title: 'IAM role & STS', chip: 'GL-03' }, { id: 'ul-03', title: 'Challenge: IAM role, resource policy, and STS', chip: 'UL-03' }, { id: 'gl-04', title: 'Customer-managed KMS', chip: 'GL-04' }, { id: 'ul-04', title: 'Challenge: Customer-managed KMS key', chip: 'UL-04' }] },
      { id: 'A1.2', title: 'Network segmentation', labs: [{ id: 'gl-05', title: 'VPC segmentation', chip: 'GL-05' }, { id: 'ul-05', title: 'Challenge: VPC segmentation', chip: 'UL-05' }] },
    ],
  },
  {
    id: 'A2',
    pill: '2.0',
    title: 'Resilient architectures',
    color: 'd3',
    weight: 26,
    groups: [
      { id: 'A2.1', title: 'Connectivity & compute', labs: [{ id: 'gl-06', title: 'NAT gateway', chip: 'GL-06' }, { id: 'ul-06', title: 'Challenge: NAT gateway then delete', chip: 'UL-06' }, { id: 'gl-07', title: 'EC2, EBS, EFS', chip: 'GL-07' }, { id: 'ul-07', title: 'Challenge: EC2, EBS, and EFS', chip: 'UL-07' }, { id: 'gl-08', title: 'Application Load Balancer', chip: 'GL-08' }, { id: 'ul-08', title: 'Challenge: Application Load Balancer', chip: 'UL-08' }, { id: 'gl-09', title: 'Auto Scaling', chip: 'GL-09' }, { id: 'ul-09', title: 'Challenge: Auto Scaling', chip: 'UL-09' }] },
      { id: 'A2.2', title: 'Integration', labs: [{ id: 'gl-10', title: 'Queue and event path', chip: 'GL-10' }, { id: 'ul-10', title: 'Challenge: Queue and event path', chip: 'UL-10' }, { id: 'gl-11', title: 'API Gateway & Lambda', chip: 'GL-11' }, { id: 'ul-11', title: 'Challenge: API Gateway and Lambda', chip: 'UL-11' }, { id: 'gl-12', title: 'Step Functions', chip: 'GL-12' }, { id: 'ul-12', title: 'Challenge: Step Functions', chip: 'UL-12' }] },
    ],
  },
  {
    id: 'A3',
    pill: '3.0',
    title: 'High-performing architectures',
    color: 'd4',
    weight: 24,
    groups: [
      { id: 'A3.1', title: 'Data & ops', labs: [{ id: 'gl-13', title: 'DynamoDB', chip: 'GL-13' }, { id: 'ul-13', title: 'Challenge: DynamoDB', chip: 'UL-13' }, { id: 'gl-14', title: 'RDS single AZ', chip: 'GL-14' }, { id: 'ul-14', title: 'Challenge: RDS, single AZ', chip: 'UL-14' }, { id: 'gl-15', title: 'CloudWatch & CloudTrail', chip: 'GL-15' }, { id: 'ul-15', title: 'Challenge: CloudWatch and CloudTrail', chip: 'UL-15' }, { id: 'gl-16', title: 'Private DNS', chip: 'GL-16' }, { id: 'ul-16', title: 'Challenge: Private DNS', chip: 'UL-16' }, { id: 'gl-17', title: 'Athena', chip: 'GL-17' }, { id: 'ul-17', title: 'Challenge: Athena on a tiny file', chip: 'UL-17' }] },
      { id: 'A3.2', title: 'Containers', labs: [{ id: 'gl-18', title: 'ECS on Fargate', chip: 'GL-18' }, { id: 'ul-18', title: 'Challenge: ECS on Fargate', chip: 'UL-18' }, { id: 'gl-19', title: 'EKS control plane', chip: 'GL-19' }, { id: 'ul-19', title: 'Challenge: EKS control plane, then delete', chip: 'UL-19' }] },
    ],
  },
  {
    id: 'A4',
    pill: '4.0',
    title: 'Cost-optimized architectures',
    color: 'd5',
    weight: 20,
    groups: [
      { id: 'A4.1', title: 'Cost labs', labs: [{ id: 'gl-20', title: 'Terraform workflow & state', chip: 'GL-20' }, { id: 'ul-20', title: 'Challenge: Terraform workflow', chip: 'UL-20' }, { id: 'gl-21', title: 'ElastiCache & HCP path', chip: 'GL-21' }, { id: 'ul-21', title: 'Challenge: ElastiCache, then HCP as allowed', chip: 'UL-21' }] },
    ],
  },
  {
    id: 'T1',
    pill: 'T1',
    title: 'Terraform 1–3',
    color: 'd6',
    weight: 0,
    groups: [{ id: 'T1.1', title: 'IaC fundamentals', labs: [] }],
  },
  {
    id: 'T2',
    pill: 'T2',
    title: 'Terraform 4',
    color: 'd6',
    weight: 0,
    groups: [{ id: 'T2.1', title: 'Modules & providers', labs: [] }],
  },
  {
    id: 'T3',
    pill: 'T3',
    title: 'Terraform 5–7',
    color: 'd6',
    weight: 0,
    groups: [{ id: 'T3.1', title: 'State & operations', labs: [] }],
  },
  {
    id: 'T4',
    pill: 'T4',
    title: 'Terraform 8',
    color: 'd6',
    weight: 0,
    groups: [{ id: 'T4.1', title: 'HCP & automation', labs: [] }],
  },
];

export const HOURLY_COST_RISK_LABS = new Set([
  'gl-06',
  'gl-07',
  'gl-08',
  'gl-09',
  'gl-14',
  'gl-18',
  'gl-19',
  'gl-21',
  'ul-06',
  'ul-07',
  'ul-08',
  'ul-09',
  'ul-14',
  'ul-18',
  'ul-19',
  'ul-21',
]);

export const EXAM_MODULE_ORDER = ['A0', 'A1', 'A2', 'A3', 'A4', 'T1', 'T2', 'T3', 'T4'] as const;

export const EXAM_MODULE_LABELS: Record<string, string> = {
  A0: 'A0 — Lab safety',
  A1: 'A1 — Secure architectures',
  A2: 'A2 — Resilient architectures',
  A3: 'A3 — High-performing architectures',
  A4: 'A4 — Cost-optimized architectures',
  T1: 'T1 — Terraform 1–3',
  T2: 'T2 — Terraform 4',
  T3: 'T3 — Terraform 5–7',
  T4: 'T4 — Terraform 8',
};

export const EXAM_MODULE_COLOR: Record<string, ModuleColor> = {
  A0: 'd1',
  A1: 'd2',
  A2: 'd3',
  A3: 'd4',
  A4: 'd5',
  T1: 'd6',
  T2: 'd6',
  T3: 'd6',
  T4: 'd6',
};
