# PDF Rotate API

A small Flask REST API that rotates a single page of an uploaded PDF by 90°, 180°, or 270° and saves the result locally. Comes with a minimal Bootstrap web form for manual use, plus a JSON endpoint for programmatic use.

## How it works

1. You upload a PDF (via the web form at `/` or a `POST` to `/Rotate`) along with a page number and rotation angle.
2. The server validates the upload — file present, `.pdf` extension, page number within range.
3. Every page is copied to a new PDF; only the requested page is rotated clockwise by the given angle.
4. The result is written to a local `Converted/` folder (created automatically on startup) as `Converted_<angle>_<original-filename>.pdf`, and a JSON status message is returned.

## Tech stack

- **Python 3.8+**
- **Flask** + **Flask-RESTful** — routing and the `/Rotate` resource
- **PyPDF2 (< 3.0)** — PDF reading/writing and page rotation
- **Bootstrap 5** (CDN) — the upload form UI

## Setup

> **Important:** this project uses the legacy PyPDF2 API (`PdfFileReader`, `rotateClockwise`), which was removed in PyPDF2 3.0. The pinned `requirements.txt` installs a compatible version — don't install PyPDF2 manually without the pin.

```bash
# 1. Clone
git clone https://github.com/vinayassrao/pdfrotate.git
cd pdfrotate

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python app.py
```

The app starts at **http://127.0.0.1:5000** in debug mode.

## Usage

### Option A — web form

Open http://127.0.0.1:5000 in a browser, choose a PDF, enter a page number and rotation angle (90 / 180 / 270), and click **Convert PDF**. The rotated file appears in the `Converted/` folder next to `app.py`.

### Option B — API call

```bash
curl -X POST http://127.0.0.1:5000/Rotate \
  -F "pdf=@sample.pdf" \
  -F "degree=90" \
  -F "pagenum=1"
```

**Form fields**

| Field     | Type    | Description                                   |
|-----------|---------|-----------------------------------------------|
| `pdf`     | file    | The PDF to modify                             |
| `degree`  | integer | Clockwise rotation angle: 90, 180, or 270     |
| `pagenum` | integer | 1-based page number to rotate                 |

**Responses** (JSON)

| `status_code` in body | Meaning                                      |
|-----------------------|----------------------------------------------|
| `200`                 | Page rotated; file saved to `Converted/`     |
| `301`                 | No file was uploaded                         |
| `302`                 | File is not a PDF                            |
| `303`                 | Page number exceeds the document's page count|

## Project structure

```
pdfrotate/
├── app.py                 # Flask app: validation, rotation logic, /Rotate resource
├── templates/
│   └── upload.html        # Bootstrap upload form
└── Converted/             # Output folder (created at runtime, not committed)
```

## Known limitations

- The API always returns HTTP 200; error conditions are signalled only through the `status_code` field in the JSON body rather than real HTTP status codes.
- Rotated files are stored on the server's disk and are not returned in the response or offered as a download.
- The rotation angle is not validated — values outside 90/180/270 are passed straight to PyPDF2.
- Built on the legacy PyPDF2 1.x/2.x API; migrating to `pypdf` (`PdfReader`/`PdfWriter`, `page.rotate()`) is the natural next step.
