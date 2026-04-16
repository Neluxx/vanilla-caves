# Syncing with the Template

This repository is based on [beet-datapack-template](https://github.com/Neluxx/beet-datapack-template.git).
Each sync is recorded as a single squashed commit, with a `template-sync` tag
marking the last synced template commit.

## Initial Setup (once per local clone)

```bash
git remote add template https://github.com/Neluxx/beet-datapack-template.git
git fetch template --tags
```

## First Sync (only if the repo has never been synced)

```bash
git fetch template
git merge --squash template/main --allow-unrelated-histories
git commit -m "chore: sync with beet template"
git tag -f template-sync template/main
git push origin main
git push origin template-sync --force
```

## Regular Sync

```bash
git fetch template --tags
git merge --squash template-sync..template/main
git commit -m "chore: sync with beet template"
git tag -f template-sync template/main
git push origin main
git push origin template-sync --force
```

If conflicts occur, resolve them, `git add` the files, then continue with the `git commit` step.

## Why this works

- `git merge --squash` applies the template's changes without creating a merge commit — the result is a single clean commit.
- The `template-sync` tag records which template commit was last synced. The range `template-sync..template/main` ensures only *new* template changes are applied on subsequent syncs, preventing duplicate work or phantom conflicts.
- Force-pushing the tag is safe — it's just a pointer, not a branch people work on.