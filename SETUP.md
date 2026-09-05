# Setup

## 1. Copy the package into your profile repository

Your GitHub profile repository is:

`rohitkr8527/rohitkr8527`

Copy these items to its root:

- `README.md`
- `assets/`
- `scripts/`
- `tests/`
- `.github/workflows/update-profile.yml`

The `docs/` folder is optional; it documents the design and implementation plan.

## 2. Add the GitLab secret (Optional)

If you want to merge private or personal GitLab activity alongside GitHub:

In GitHub:

**rohitkr8527/rohitkr8527 → Settings → Secrets and variables → Actions → New repository secret**

Create:

- Name: `GITLAB_TOKEN`
- Value: your GitLab Personal Access Token with read-only `read_user` scope

> [!NOTE]
> `GITLAB_TOKEN` is **optional**. If omitted, the workflow and scripts automatically pull your real GitHub contributions without errors.
> You do **not** need to create a `GITHUB_TOKEN` secret. GitHub Actions supplies `${{ secrets.GITHUB_TOKEN }}` automatically.

## 3. Enable workflow write access if necessary

Open:

**Settings → Actions → General → Workflow permissions**

Choose **Read and write permissions** if your account/repository policy does not already permit the workflow to push generated assets.

The workflow also declares `contents: write`, but repository policy still controls the maximum permission available.

## 4. Run once manually

Open:

**Actions → Update unified engineering activity → Run workflow**

After the first successful live run, the preview activity files will be replaced by your real merged GitHub + GitLab data.

## 5. Privacy behavior

The GitLab API response is held only in memory during the workflow. The generated public JSON contains only:

- date
- GitHub count
- GitLab count
- total count
- aggregate streak/activity statistics

Private project names, project IDs, URLs, issue/MR titles, and commit messages are never written to disk.

## 6. Local verification

```bash
python -m unittest discover -s tests -v
python scripts/update_profile.py --sample
```

The second command intentionally generates preview data. Do not use `--sample` in the scheduled workflow.
