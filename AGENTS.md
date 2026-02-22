# AGENTS.md

Instructions for AI coding agents (Codex/Claude/etc.) working in this repository.

## Workflow & Branching

- Long-lived branches:
  - `dev` (integration)
  - `main` (release/publish)
- Do all work on **feature branches** from `dev`.
- Merge feature branches into `dev` via PR.
- Promote `dev` -> `main` via PR when ready to release.
- Never commit directly to protected branches.

## Commit Message Standard

Use **Conventional Commits**: https://www.conventionalcommits.org/en/v1.0.0/

Examples:
- `feat(memory): add vector recall endpoint`
- `fix(api): handle missing auth token`
- `chore(ci): tighten coverage gates`
- `docs(readme): add local setup notes`

Breaking changes:
- `feat!: change memory schema`
- or include `BREAKING CHANGE:` in commit body.

## Quality Gates

- Tests must pass before merge.
- Coverage gate: **>= 70%** (enforced by CI).
- Keep CI green on PRs to `dev` and `main`.
- Use lint/format tooling where configured.

## Pull Request Expectations

- Keep PRs focused and reasonably small.
- Include:
  - What changed
  - Why it changed
  - How it was tested
  - Risks/rollback notes if relevant
- Update docs if behavior or setup changes.

## CI/CD Rules

- Docker publish must run **only from `main`**.
- Do not add publish-from-`dev` paths.

## Safety / Change Discipline

- Prefer additive, reversible changes.
- Avoid destructive operations/migrations without explicit note in PR.
- If uncertain, leave a clear TODO and raise in PR description.
