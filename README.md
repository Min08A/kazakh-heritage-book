# Kazakh Heritage — an interactive book

A page-turning web book of **34 Kazakh words** in two parts:

* **Part 1. Textbook Vocabulary** — Khan Shatyr, Kiiz Ui (yurt), Kyz Zhibek, Aisha Bibi, Karakhan, Ayran.
* **Part 2. Proposed Vocabulary** — Aitys, Asyk, At Arba, Baige, Baursak, Besik, Dombyra, Zhailau, Kazakh Kuresi, Keruen, Kosh, Kymyz, Kui, Qorzhyn, Qudyq, Qurt, Qystau, Saba, Shanyraq, Sheber, Torsyq, Usta, Zerger, Zhyr, Kobyz, Saukele, Shapan, Beshbarmak.

The book layout (contents pages, part openers, chapters, credits) is generated from `js/data.js`, so chapters can be added or reordered there.

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
* Videos: `media/videos/<slug>.mp4` (H.264/AAC; an optional `.webm` is used if present); posters `media/images/<slug>.jpg`.
  The videos are **animated illustrations with captions and synthesized music** created for this project — there is no spoken voice and no live-action footage.
* Narration: `media/audio/<slug>.mp3` — recorded narration for the 29 words that have a recording (all except Karakhan, Kobyz, Saukele, Shapan, Beshbarmak). Where there is no file, the object page reads the transcript with the **browser's built-in English voice** (labelled as such). Drop a new recording into `media/audio/` to replace or add one.

### 3D models
Each chapter's model is listed in `js/data.js` and credited on the Credits pages of the book and under each 3D viewer.
* **Sketchfab, CC BY 4.0:** Kyz Zhibek (girl's takiya), Asyk, Baige (qamshy), Baursak, Dombyra, Usta (anvil), Zhyr (Umbetai Zhyrau monument), Kobyz, Shapan.
* **Sketchfab, license not stated on the model page** (confirm with the creators before a public launch): Khan Shatyr, Kiiz Ui, Aisha Bibi, Karakhan, Aitys, Kazakh Kuresi, Kui, Qystau, Besik, Saukele.
* **Simplified models made for this project** (`models/*.glb`): Ayran, At Arba, Zhailau, Keruen, Kosh, Kymyz, Qorzhyn, Qudyq, Qurt, Saba, Shanyraq, Sheber, Zerger, Torsyq, Beshbarmak. Every chapter also has a simplified model as an offline fallback.

The Sketchfab viewer is loaded with AR/VR buttons switched off. If a Sketchfab model fails (or you press **Use simplified model**) the page shows the local `.glb` in a small built-in WebGL viewer (`js/glbviewer.js`, no external libraries). The credit line under the viewer always names the creator and license.

## Regenerating media (optional)
Needs Python 3, `numpy`, `Pillow`, `opencv-python`, `ffmpeg`, and the Lora/Poppins fonts (paths at the top of `tools/render.py`).

```bash
cd tools
python3 render.py [slug ...] # videos + posters (about 1 min per video); add --no-webm to skip WebM
python3 make_models.py       # shapan, beshbarmak, besik, torsyk
python3 make_models2.py      # dombra, kobyz, yurt, saukele
python3 make_models3.py      # the 26 chapters added in the two-part edition
```

## Project layout
```
index.html  object.html  css/style.css
js/  data.js book.js video.js qrpanel.js qr.js qrtarget.js model3d.js glbviewer.js audio.js progress.js config.js
media/{videos,images,audio}   models/*.glb   tools/*.py
serve.py  vercel.json  netlify.toml  _redirects  serve.json
```
