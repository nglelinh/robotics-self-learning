# GitHub setup

```bash
cd robotics-self-learning
git init -b main   # if needed
git add -A
git commit -m "Initial robotics self-learning course"
gh repo create nglelinh/robotics-self-learning --public --source=. --remote=origin --push
```

If `gh` auth fails:

```bash
gh auth login
# or create empty repo nglelinh/robotics-self-learning on GitHub, then:
git remote add origin git@github.com:nglelinh/robotics-self-learning.git
git push -u origin main
```

Enable GitHub Pages via Actions (workflow from template `.github/workflows/`).
