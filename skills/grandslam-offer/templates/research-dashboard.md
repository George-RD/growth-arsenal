# Research Dashboard Report

This file is a compatibility pointer. Do not generate HTML from prose instructions.

After research or gap state changes, run:

```sh
python3 ../growth-arsenal-workspace/scripts/arsenal.py render \
  --workspace {project-name}.arsenal.json \
  --surface research-dashboard
```

The renderer reads structured market identity, personas, gaps and sources from the canonical workspace. Missing fields remain visibly missing; the report does not invent content for visual completeness.
