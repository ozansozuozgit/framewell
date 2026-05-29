# Prompts

Paste prompts you copy manually into individual `.txt` files here, preferably named by slug, for example:

- `synex.txt`
- `synergeus.txt`
- `interactive-loader.txt`

Then run:

```bash
cd /Users/ozansozuoz/programming-files/lafys-copy
python3 scripts/build_prompts_json.py
```

The local UI will then use `data/prompts.json` so Copy Prompt works locally for pasted prompts.
