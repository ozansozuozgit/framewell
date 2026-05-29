# Deployment checklist

Framewell is static and can be deployed to any static host.

## Preflight

- Run `npm run validate`.
- Serve locally with `npm run start`.
- Open `http://localhost:4173`.
- Confirm browser console has no errors.
- Confirm archive count is 195 and preview count is 195.
- Confirm no card shows an empty placeholder background.
- Confirm generated concept-sketch previews are visually descriptive and not labeled as screenshots.
- Review `THIRD_PARTY_PROMPTS.md` before making public claims about source/licensing.

## Static host notes

Upload the whole directory contents except:

- `.git/`
- `node_modules/`
- local `.env` files

Required public paths:

- `/index.html`
- `/styles.css`
- `/app.js`
- `/data/posts.json`
- `/data/prompts.json`
- `/assets/**`
- `/THIRD_PARTY_PROMPTS.md`
