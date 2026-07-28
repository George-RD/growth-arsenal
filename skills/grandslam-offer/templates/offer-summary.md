# Offer Summary Report

This file is a compatibility pointer. Do not generate HTML from prose instructions.

After Phase 5 is approved, render the canonical workspace:

```sh
python3 ../growth-arsenal-workspace/scripts/arsenal.py render \
  --workspace {project-name}.arsenal.json \
  --surface offer-summary
```

The shared template lives at `../growth-arsenal-workspace/assets/templates/offer-summary.html`. Its tokens, CSS and behaviour live under the workspace skill's `assets/design/` directory.

Change workspace state or shared assets, then regenerate. Never patch the generated HTML.
