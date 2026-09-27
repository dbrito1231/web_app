# Cursor Prompt: Plan a Detailed Repository README

You are working inside an existing software repository.

Your task is to **create a detailed implementation plan for producing a high-quality `README.md` for this repository**.

## Objective

Analyze the repository thoroughly and produce a plan for creating a README that accurately explains:

- What the project is
- What problem it solves
- How the application/system is structured
- How to install and configure it
- How to run it
- How to develop against it
- How to test it
- How to deploy it
- How to troubleshoot common issues
- How contributors should work with the repository

The README must be based on the **actual repository contents**, not assumptions.

## Important Constraints

- **Do not modify any files.**
- **Do not create the README yet.**
- Only inspect the repository and create a detailed README implementation plan.
- Do not invent commands, environment variables, dependencies, ports, services, workflows, architecture details, or deployment instructions.
- If something cannot be confirmed from the repository, explicitly mark it as **Needs Verification**.
- Prefer information found directly in source code, configuration files, scripts, CI/CD files, infrastructure code, tests, and existing documentation.
- Identify contradictions or outdated documentation when found.

## Repository Analysis Requirements

Before creating the plan, inspect relevant files and directories such as:

- Existing `README.md` or documentation
- `AGENTS.md`
- `package.json`
- `pyproject.toml`
- `requirements.txt`
- `Pipfile`
- `poetry.lock`
- `uv.lock`
- `package-lock.json`
- `yarn.lock`
- `pnpm-lock.yaml`
- `Dockerfile`
- `docker-compose.yml`
- `.env.example`
- Application configuration files
- Backend source code
- Frontend source code
- Database models and migrations
- API routes/endpoints
- Authentication/authorization code
- Test suites
- Build scripts
- Startup scripts
- Makefiles
- Task runners
- Terraform
- Ansible
- Kubernetes manifests
- GitHub Actions
- GitLab CI
- Jenkins files
- Other CI/CD configuration
- Deployment configuration
- Infrastructure configuration
- Example files
- Seed/sample data
- CLI utilities
- Repository scripts
- Existing architecture/design documents

Do not assume all of these exist. Inspect only what is present.

## Determine the Project Architecture

As part of the analysis, identify and document in the plan:

1. Primary programming languages
2. Frameworks
3. Major libraries
4. Frontend technologies
5. Backend technologies
6. Database technologies
7. External services
8. Authentication mechanisms
9. APIs
10. Background workers or scheduled jobs
11. Infrastructure dependencies
12. Containerization
13. CI/CD
14. Deployment model
15. Repository structure
16. Configuration system
17. Environment variables
18. Logging/monitoring
19. Testing strategy
20. Developer tooling

If the project contains multiple applications, services, packages, or workspaces, identify each one separately.

## README Sections to Evaluate

Determine which of the following sections should appear in the final README.

Only recommend sections that are relevant to this repository.

### Core Sections

- Project title
- Project overview
- Project purpose
- Key features
- Screenshots or diagrams, if useful
- Architecture overview
- Technology stack
- Repository structure
- Prerequisites
- Installation
- Configuration
- Environment variables
- Local development
- Running the application
- Running individual services
- Database setup
- Database migrations
- Seed/sample data
- Authentication setup
- API usage
- CLI usage
- Testing
- Linting
- Formatting
- Static analysis
- Security scanning
- Build process
- Docker usage
- Infrastructure setup
- Deployment
- CI/CD
- Monitoring/logging
- Troubleshooting
- Known limitations
- Development workflow
- Contribution guidelines
- Coding standards
- Branching strategy
- Release process
- License
- Maintainers/ownership

## Commands

Locate and verify commands for tasks such as:

- Installing dependencies
- Starting development servers
- Starting backend services
- Starting frontend services
- Running production builds
- Running tests
- Running specific test suites
- Running linters
- Running formatters
- Running type checking
- Running security checks
- Starting Docker services
- Stopping Docker services
- Running database migrations
- Seeding databases
- Building containers
- Deploying infrastructure
- Deploying the application

For every command included in the future README plan, identify the repository file that confirms the command.

Example:

```text
Command:
pytest tests/

Verified from:
pyproject.toml
```

Do not recommend undocumented commands unless they can be derived confidently from repository configuration.

## Environment Variables

Identify all meaningful environment variables used by the application.

For each variable, determine where possible:

- Variable name
- Purpose
- Required vs optional
- Default value
- Which service uses it
- Whether it contains a secret
- Where it is referenced
- Whether an example value can safely be documented

Never expose actual credentials, secrets, tokens, API keys, passwords, certificates, or private connection strings.

If the repository contains real secrets, flag this as a security concern without reproducing the secret.

## Repository Structure Documentation

Determine whether the README should contain a directory tree.

If useful, propose a concise structure such as:

```text
repo/
├── backend/
├── frontend/
├── tests/
├── scripts/
├── infrastructure/
└── docs/
```

For each important directory, explain what it contains and why a new developer would care.

Do not include every generated, cache, dependency, or build directory.

## Architecture Documentation

Determine whether the repository would benefit from an architecture diagram.

If so, specify what the diagram should show, for example:

```text
User
  |
Frontend
  |
Backend API
  |
Database
  |
External Services
```

Recommend Mermaid where appropriate so the diagram can live directly inside the README.

Do not invent architecture relationships that cannot be verified.

## API Documentation

If the repository exposes APIs, determine whether the README should include:

- Base URL
- API version
- Authentication requirements
- Major endpoints
- Example requests
- Example responses
- Swagger/OpenAPI location
- Error-handling conventions

Avoid duplicating a large API specification if dedicated API documentation already exists.

Instead, reference the appropriate documentation.

## Security Documentation

Inspect whether the project contains security-related requirements such as:

- Authentication
- Authorization
- Secret management
- TLS
- Security headers
- Dependency scanning
- Static analysis
- SAST
- DAST
- Container scanning
- Infrastructure scanning
- Secure development requirements

Recommend README security guidance only when supported by the repository.

Do not expose sensitive operational information.

## Testing Documentation

Identify:

- Test frameworks
- Test directories
- Unit tests
- Integration tests
- End-to-end tests
- Coverage configuration
- Test fixtures
- Mocking tools
- Test databases
- Required services

The plan should explain how the README should describe the project's testing workflow.

## CI/CD Documentation

Inspect available CI/CD configuration and identify:

- CI provider
- Pipeline stages
- Test jobs
- Build jobs
- Security jobs
- Deployment jobs
- Required secrets
- Environments
- Artifacts
- Release process

Recommend how much of this belongs in the README versus dedicated documentation.

## Deployment Documentation

Determine how the project is deployed.

Possible examples include:

- Bare-metal server
- Windows Server
- Linux
- IIS
- Nginx
- Docker
- Kubernetes
- AWS
- Azure
- GCP
- Terraform
- Ansible
- GitHub Actions
- GitLab
- Jenkins
- Other deployment tooling

Document only what is supported by repository evidence.

## Troubleshooting Plan

Identify likely troubleshooting topics based on:

- Existing issue notes
- Error handling
- Configuration requirements
- Dependency requirements
- Port conflicts
- Database setup
- Authentication
- Docker configuration
- Environment variables
- Build failures
- Test failures
- Deployment scripts

Do not speculate about undocumented problems.

## Existing Documentation Review

If a README already exists, evaluate:

- What is accurate
- What is outdated
- What is missing
- What is redundant
- What should be reorganized
- What should be preserved
- What conflicts with the repository
- What information belongs somewhere other than the README

Also inspect any `/docs`, wiki-style content, architecture documents, comments, or setup guides that should be referenced rather than duplicated.

## Target Audience

Plan the README so that it works for multiple audiences:

### New Developer
Needs to understand the project and start it locally.

### Existing Developer
Needs quick commands, architecture references, testing instructions, and development workflows.

### DevOps / Platform Engineer
Needs configuration, infrastructure, deployment, observability, and operational information.

### Security Engineer
Needs authentication, security tooling, secrets-handling expectations, and security workflow information.

### Technical Reviewer / Manager
Needs a concise explanation of the application's purpose, architecture, dependencies, and operational model.

## Quality Requirements

The final README should eventually be:

- Technically accurate
- Easy to navigate
- Concise where possible
- Detailed where necessary
- Free of unsupported claims
- Free of secret values
- Structured using clear Markdown headings
- Useful to someone unfamiliar with the repository
- Based on verified repository evidence
- Maintainable as the project evolves

## Required Output

Create a planning document named conceptually:

```text
README_IMPLEMENTATION_PLAN.md
```

Do **not** create the file unless explicitly instructed to do so.

Your response should contain the proposed contents of that plan.

The plan must include the following sections:

### 1. Repository Summary

Summarize what you discovered about the repository.

### 2. Documentation Evidence

List the important files inspected and what README information each file provides.

Use a table where useful.

Example:

| File | Information |
|---|---|
| `pyproject.toml` | Python dependencies, tooling, test configuration |
| `docker-compose.yml` | Local services and ports |
| `.env.example` | Required configuration |
| `.github/workflows/ci.yml` | CI workflow |

### 3. Proposed README Structure

Provide the complete proposed heading hierarchy.

Example:

```text
# Project Name
## Overview
## Features
## Architecture
## Technology Stack
## Repository Structure
## Prerequisites
## Installation
## Configuration
## Running Locally
## Testing
## Deployment
## Troubleshooting
## Contributing
```

Tailor this to the actual repository.

### 4. Section-by-Section Implementation Plan

For every proposed README section, explain:

- Purpose
- Information to include
- Source files that verify the information
- Commands that should be documented
- Examples that should be included
- Diagrams/tables that should be included
- Missing information requiring verification

### 5. Verified Commands

Create a table containing:

| Task | Command | Evidence |
|---|---|---|

Only include commands supported by repository evidence.

### 6. Configuration and Environment Variables

Create a table containing:

| Variable | Purpose | Required | Used By | Evidence |
|---|---|---|---|---|

Do not expose secrets.

### 7. Architecture Documentation Plan

Explain what architecture information should appear and whether Mermaid diagrams should be created.

### 8. Setup and Developer Experience Plan

Explain the exact flow the future README should use to take a developer from:

```text
git clone
   ↓
install dependencies
   ↓
configure environment
   ↓
initialize required services
   ↓
initialize database
   ↓
start application
   ↓
verify application works
   ↓
run tests
```

Adapt the sequence to the repository.

### 9. Testing Documentation Plan

Describe how testing should be documented.

### 10. Deployment and Operations Plan

Describe how deployment, infrastructure, logging, monitoring, and operations should be documented.

### 11. Troubleshooting Documentation Plan

List repository-supported troubleshooting topics.

### 12. Security Documentation Plan

Identify security information that belongs in the README.

### 13. Documentation Gaps

List anything that cannot currently be confirmed.

For each gap, include:

- Missing information
- Why it matters
- Where the information might be found
- Whether developer input is required

### 14. Existing README Gap Analysis

If an existing README exists, compare it against the proposed structure.

Classify findings as:

- Keep
- Update
- Remove
- Add
- Move to separate documentation

### 15. Recommended README Enhancements

Identify useful improvements such as:

- Mermaid architecture diagrams
- Quick-start section
- Command reference table
- Configuration table
- Development workflow
- Troubleshooting matrix
- API examples
- Screenshots
- Badges

Only recommend enhancements that provide actual value.

### 16. Implementation Order

Provide a recommended step-by-step order for writing the README.

Example:

1. Establish project overview.
2. Document verified prerequisites.
3. Document installation.
4. Document configuration.
5. Document local startup.
6. Document architecture.
7. Document testing.
8. Document deployment.
9. Add troubleshooting.
10. Validate all commands.
11. Perform final documentation review.

### 17. Validation Checklist

Create a checklist that should be completed before the README is considered finished.

Include checks such as:

- [ ] Every documented command was validated against repository configuration.
- [ ] No secrets or credentials are present.
- [ ] Environment variables match the source code.
- [ ] Installation instructions work from a clean environment.
- [ ] Repository structure is current.
- [ ] Architecture description matches implementation.
- [ ] Test instructions match actual test configuration.
- [ ] Deployment instructions match repository automation.
- [ ] Broken or obsolete documentation has been identified.
- [ ] Links and references are valid.
- [ ] Markdown renders correctly.

## Final Requirement

Do not begin writing the actual README.

Your only deliverable is a **detailed, evidence-based implementation plan for creating the README**.

The plan should be specific enough that another developer or AI agent could use it to create the final README without needing to rediscover the repository structure.
