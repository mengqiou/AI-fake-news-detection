# Branch Protection Rules

This document describes the branch protection rules for this repository.

## Protected Branches

### `main` Branch

The `main` branch is protected with the following rules:

#### Required Settings

1. **Require pull request reviews before merging**
   - Required approving reviews: **1**
   - Dismiss stale pull request approvals when new commits are pushed: ✅
   - Require review from Code Owners: ❌ (optional)

2. **Require status checks to pass before merging**
   - Require branches to be up to date before merging: ✅
   - Required status checks:
     - `Lint & Format Check`
     - `Run Tests`
     - `Validate PR`

3. **Require linear history**
   - ✅ Enabled (prevents merge commits, requires rebase or squash)

4. **Do not allow bypassing the above settings**
   - ✅ Enabled (even admins must follow rules)

5. **Restrictions**
   - **Direct pushes to main: FORBIDDEN** ⛔
   - All changes must go through pull requests

#### Optional but Recommended

- **Require signed commits**: Consider enabling for security
- **Require deployments to succeed**: Enable when deployment pipeline is ready

---

## How to Set Up Branch Protection (GitHub)

1. Go to repository **Settings** → **Branches**

2. Click **Add rule** under "Branch protection rules"

3. Enter branch name pattern: `main`

4. Enable the following:

   ```
   ✅ Require a pull request before merging
      ✅ Require approvals (1)
      ✅ Dismiss stale pull request approvals when new commits are pushed
   
   ✅ Require status checks to pass before merging
      ✅ Require branches to be up to date before merging
      Status checks:
        - Lint & Format Check
        - Run Tests
        - Validate PR
   
   ✅ Require linear history
   
   ✅ Do not allow bypassing the above settings
   ```

5. Click **Create** or **Save changes**

---

## Development Workflow

### Creating a Feature

```bash
# 1. Create feature branch from main
git checkout main
git pull origin main
git checkout -b feat/your-feature-name

# 2. Make changes and commit
git add .
git commit -m "feat: add new feature"

# 3. Push to remote
git push -u origin feat/your-feature-name

# 4. Create Pull Request on GitHub
# - Fill out PR template
# - Wait for CI checks to pass
# - Request review
# - Address feedback
# - Merge after approval
```

### PR Title Format (Conventional Commits)

Use one of these prefixes:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `style:` - Formatting, missing semicolons, etc.
- `refactor:` - Code restructuring
- `test:` - Adding tests
- `chore:` - Maintenance tasks
- `ci:` - CI/CD changes

**Examples:**
```
feat: add platform verification tool
fix: resolve DynamoDB Decimal serialization issue
docs: update README with branch protection rules
refactor: simplify agent factory logic
test: add integration tests for fake news detector
```

---

## Merging Strategies

### Recommended: Squash and Merge

- Keeps main branch history clean
- One commit per feature/fix
- Easier to revert if needed

```bash
# GitHub will do this automatically when you select "Squash and merge"
```

### Alternative: Rebase and Merge

- Preserves individual commits
- Linear history
- Good for features with logical commit breakdown

```bash
# Before merging, rebase your branch
git checkout feat/your-feature
git rebase origin/main
git push --force-with-lease
```

---

## What Happens When You Try to Push to Main

```bash
$ git push origin main

remote: error: GH006: Protected branch update failed
remote: - Cannot push to protected branch main
remote: - All changes must be made through pull requests
```

**Solution**: Create a pull request instead!

---

## Emergency Hotfixes

For critical production issues:

1. Create branch: `git checkout -b hotfix/critical-issue`
2. Make minimal fix
3. Create PR with title: `fix: [HOTFIX] description`
4. Get expedited review
5. Merge after CI passes

**Never disable branch protection for hotfixes.**

---

## Questions?

See `CONTRIBUTING.md` for full development guidelines.
