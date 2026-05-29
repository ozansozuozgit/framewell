# Lafys local copy

Local static archive/recreation of the public Lafys homepage captured from https://lafys.com.

Included:
- `index.html`, `styles.css`, `app.js`: local static UI
- `assets/`: public logo, avatars, thumbnails, and preview videos/images
- `data/posts-original.json`: public API response from `/api/posts/list`
- `data/posts.json`: normalized card metadata used by the local UI
- `prompts/`: paste prompt `.txt` files here
- `scripts/add_prompt.py`: save clipboard/stdin prompt into `prompts/` and rebuild `data/prompts.json`

Not included:
- stealth/incognito/quota-reset bypasses
- gated prompts unless you paste them manually

Run locally:

```bash
cd /Users/ozansozuoz/programming-files/lafys-copy
python3 -m http.server 4173
# open http://localhost:4173
```

Add a copied prompt from the clipboard:

```bash
cd /Users/ozansozuoz/programming-files/lafys-copy
python3 scripts/add_prompt.py synex --from-clipboard
```

Or paste via stdin:

```bash
python3 scripts/add_prompt.py synex < my-prompt.txt
```
