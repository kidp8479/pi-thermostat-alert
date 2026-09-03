# Contributing

Small solo project, but run like a real one.

## Workflow

- One unit of work = one branch = one PR. No direct commits to `main`.
- Rebase the branch on `main` before opening/merging the PR; keep a linear
  history (merge commits only at the actual merge).
- Re-read your own diff before merging.

## Commits

- Conventional Commits: `type: summary` (`feat`, `fix`, `refactor`, `docs`,
  `build`, `ci`, `test`, `style`, `chore`).
- Atomic: one logical change per commit. The body explains *why* when the diff
  does not.

## Before committing

```bash
make check   # ruff format --check + ruff check + pytest
```

`make install` enables a pre-commit hook that runs the format/lint checks; the
same checks plus the test suite and a gitleaks scan run in CI on every push and
PR. Don't bypass them (`--no-verify`) without a reason.

## Code

- Ship a test with every new behaviour (client method, monitor logic).
- Comment the *why*, not the *what*.
- Everything in the repo is in English (code, comments, commits, docs).
- Config comes from the environment (`.env`, git-ignored); never commit a
  secret. Document new variables in `.env.example`.
- Ruff enforces a complexity budget (mccabe <= 10): split the function, don't
  disable the rule.
