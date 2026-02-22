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
- Use concise, human PR titles (avoid generic/bot-like wording).
- PR identity convention:
  - **Kite-authored PRs** must start with: `kite: `
  - **Human-authored PRs** may optionally start with: `fren: `
- Preferred PR title format after identity prefix:
  - `<type(scope)>: short outcome`
  - Example: `kite: ci(repo): enforce commit style and branch gates`
- PR description style:
  - 1 short summary paragraph
  - `Author: Kite` or `Author: fren`
  - "Validation" section (tests/checks run)
  - "Notes" only if truly needed
- Avoid long bullet dumps unless requested.
- Update docs if behavior or setup changes.
- Default flow is **feature -> dev**. Do not open feature PRs directly to `main`.

## CI/CD Rules

- Docker publish must run **only from `main`**.
- Do not add publish-from-`dev` paths.

## Safety / Change Discipline

- Prefer additive, reversible changes.
- Avoid destructive operations/migrations without explicit note in PR.
- If uncertain, leave a clear TODO and raise in PR description.
