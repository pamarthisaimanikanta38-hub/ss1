# A Little Universe for Sindhu 💗

A feature-rich, responsive FastAPI website made by Sai for Sindhu. Includes animated hearts, twinkling stars, a surprise modal, five personal notes, a wish generator, a photo gallery, and photo uploads.

## Run locally in VS Code (Windows)

1. Install Python 3.10+ and VS Code.
2. Extract this ZIP, then open the `sindhu_heart_deluxe` folder in VS Code.
3. Open **Terminal → New Terminal** and run:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn app:app --reload
```

4. Visit http://127.0.0.1:8000

Using `.venv\Scripts\python.exe` avoids the PowerShell activation-policy issue.

## Add photos

Use the **Our memory corner** section in the website. Select one or more JPG, PNG, WEBP, or GIF files, then click **Add photos**. Files are saved in `static/uploads/`. The filenames are used as simple captions, so you can rename files before uploading.

## Deploy online with Render

1. Create a GitHub repository and upload these project files.
2. Visit https://render.com and create a **New Web Service** connected to that repository.
3. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
4. Deploy and open the URL Render provides.

### Important deployment note
On a free web-service plan, local uploaded files may not persist across restarts or redeploys. For a permanent public gallery, use persistent storage or a cloud image service. Only upload photos you have permission to share; a public website may be accessible to anyone with its URL.

## Customise
- Change the text in `NOTES` near the top of `app.py`.
- Change the main letter in the HTML inside `page()`.
- Change colours in the CSS `:root` section.
- Add your own images using the gallery upload form.
