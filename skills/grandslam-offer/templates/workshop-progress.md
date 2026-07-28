# Workshop Progress Report

This file is a compatibility pointer. Do not generate HTML from prose instructions.

After every material phase transition, run:

```sh
python3 ../growth-arsenal-workspace/scripts/arsenal.py render \
  --workspace {project-name}.arsenal.json \
  --surface workshop-progress
```

The renderer calculates phase state, review counts, open critical issues, revisions and stale dependencies from the canonical workspace. Do not estimate those values in the prompt.
