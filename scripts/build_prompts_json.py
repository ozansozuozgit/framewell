#!/usr/bin/env python3
import json, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
prompts_dir = root / 'prompts'
out = {}
for path in sorted(prompts_dir.glob('*.txt')):
    text = path.read_text(encoding='utf-8').strip()
    if text:
        out[path.stem] = text
(root / 'data' / 'prompts.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(f'wrote {len(out)} prompts to data/prompts.json')
