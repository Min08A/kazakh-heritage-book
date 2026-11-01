# Kazakh Heritage — an interactive book

A page-turning web book about eight Kazakh cultural objects: **Dombra, Yurt, Kobyz, Saukele, Shapan, Beshbarmak, Besik, Torsyk**.

* Every chapter is a two-page spread: a **video** (with English captions) + a **QR code** on the left, the story and facts on the right.
* The QR code stays **locked until the video really ends** (HTML5 `ended` event). It opens `/object/<slug>`, a mobile page with an interactive **3D model**, **audio narration** + transcript, attribution and previous/next navigation.
* On phones the book switches to single pages (swipe / arrows). Progress is saved in `localStorage`.
* No AR / WebXR / native app. No build step, no npm, no framework: plain HTML + ES modules.

## Run locally

```bash
python3 serve.py 8000        # http://localhost:8000
```

`serve.py` supports HTTP Range requests (needed for video seeking) and rewrites `/object/<slug>` to `object.html`.
(Any static server works if you add the same rewrite; `npx serve` reads `serve.json`.)

On `localhost` / a LAN address the book shows a **"testing mode" warning** next to every QR code and a small *DEV: simulate end* button under each video (never saved to progress). Both disappear on a real public HTTPS domain.

## Deploy

The site must be served from the **root of a domain** (`https://example.com/`, not `https://example.com/sub/`), because QR codes point to `/object/<slug>`.
Publish the folder as it is — there is nothing to build.

### Vercel
1. Push this folder to a GitHub repository (or run `npx vercel` inside it).
2. *Add New → Project →* import the repo. Framework preset: **Other**. Build command: *empty*. Output directory: *empty* (root).
3. Deploy. `vercel.json` already contains the `/object/:slug → /object.html` rewrite.

### Netlify
* Drag the folder onto <https://app.netlify.com/drop>, **or** connect the repo (build command empty, publish directory `.`).
* `netlify.toml` / `_redirects` contain the rewrite.

### Cloudflare Pages
Connect the repo, framework preset *None*, build command empty, output directory `/`. `_redirects` is honoured.

### GitHub Pages
Not recommended: it cannot rewrite `/object/<slug>`.

### After deploying — checklist
1. Open `https://YOUR-DOMAIN/object/dombra` directly in a browser (must show the 3D page, not a 404).
2. Open the book, watch one video to the end → the QR code appears, **without** the yellow "testing mode" warning. Scan it with a phone.
3. Optional: set `PUBLIC_SITE_URL` in `js/config.js` (e.g. `'https://kazakh-heritage.example.com'`) if you want QR codes to always use a fixed domain instead of the address the book is opened from. It must be public HTTPS; otherwise the testing warning is shown.

## Content

* All texts, model links, credits and licenses: **`js/data.js`**.
* Videos: `media/videos/<slug>.mp4` (H.264/AAC) + `.webm` (VP9/Opus); posters `media/images/<slug>.jpg`.
  The videos are **animated illustrations with captions and synthesized music** created for this project — there is no spoken voice and no live-action footage.
* Narration: if `media/audio/<slug>.mp3` exists it is used. Otherwise the object page reads the transcript with the **browser's built-in English voice** (labelled as such). Drop your own recordings into `media/audio/` to replace it.

### 3D models
| Object | Primary | Fallback / alternative |
|---|---|---|
| Dombra, Kobyz | Sketchfab (Q3D_Library, CC BY 4.0) | simplified model in `models/` |
| Yurt, Saukele, Besik | Sketchfab (license *not stated* on the model pages — confirm with the creators before a public launch) | simplified model in `models/` |
| Shapan, Beshbarmak, Torsyk | simplified model in `models/` (made for this project) | — |

The Sketchfab viewer is loaded with AR/VR buttons switched off. If a Sketchfab model fails (or you press **Use simplified model**) the page shows the local `.glb` in a small built-in WebGL viewer (`js/glbviewer.js`, no external libraries). The credit line under the viewer always names the creator and license.

## Regenerating media (optional)
Needs Python 3, `numpy`, `Pillow`, `opencv-python`, `ffmpeg`, and the Lora/Poppins fonts (paths at the top of `tools/render.py`).

```bash
cd tools
python3 render.py            # all videos + posters (about 2 min per video)
python3 make_models.py       # shapan, beshbarmak, besik, torsyk
python3 make_models2.py      # dombra, kobyz, yurt, saukele
```

## Project layout
```
index.html  object.html  css/style.css
js/  data.js book.js video.js qrpanel.js qr.js qrtarget.js model3d.js glbviewer.js audio.js progress.js config.js
media/{videos,images,audio}   models/*.glb   tools/*.py
serve.py  vercel.json  netlify.toml  _redirects  serve.json
```
