# Syncing with the Template

This repository is based on [beet-datapack-template](https://github.com/Neluxx/beet-datapack-template.git) and can be synced with it using a `template` Git remote.

## Initial Setup

Add the template as a remote. This only needs to be done **once per local clone**:

```bash
git remote add template https://github.com/Neluxx/beet-datapack-template.git
```

## Syncing

Run these steps whenever you want to pull in changes from the template:

**1. Fetch the latest template changes**
```bash
git fetch template
```

**2. Merge**
```bash
git merge template/main -m "chore: sync with beet template"
```

**3. Push**
```bash
git push origin main
```

If there are conflicts during the merge, resolve them, `git add` the resolved files, and then `git commit` before pushing.

## Notes

- The `--allow-unrelated-histories` flag is only needed on the very first merge, after which the histories are linked and it can be omitted.
- A regular merge commit is used (not `--squash`) so that Git automatically tracks the sync point, preventing already-synced changes from being re-applied on future syncs.