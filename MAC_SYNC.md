# Sync onto MacBook (machineId cbecf7d8-4473-4909-a9c2-eadeced14735)

Target: `/Users/nguyenlelinh/teaching/robotics-self-learning`

## Box artifact

Built on the agent computer when Mac local-exec is unavailable:

- Tree: `/workspace/robotics-self-learning`
- Tarball: `/workspace/robotics-self-learning.tar.gz`

## On Mac

```bash
mkdir -p /Users/nguyenlelinh/teaching
cd /Users/nguyenlelinh/teaching
# after copying the tarball:
tar xzf robotics-self-learning.tar.gz
# Prefer copying from local course-self-learning-template only for structure;
# this tree is already filled—do not re-clone teaching repos from GitHub.
```

Then `gh auth login` if needed and push per README / GITHUB_SETUP.md.
