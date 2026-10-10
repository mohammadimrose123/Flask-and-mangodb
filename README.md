# Flask & MongoDB Atlas Assignment

## Features
- `GET /api` reads `data/records.json` and returns a JSON list.
- `GET /` displays a form with name, email, and message.
- `POST /submit` validates fields and inserts a document into MongoDB Atlas.
- Successful insert redirects to `/success`, displaying **Data submitted successfully**.
- Validation/database errors are displayed on the original form page without a success redirect.

## Requirements
- Python 3.10+
- A MongoDB Atlas cluster and database user

## Setup (Windows PowerShell)
```powershell
cd Flask_and_MongoDB_MohammadImrose
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```
Edit `.env` and replace the example `MONGODB_URI` with your real Atlas connection string. Do not commit `.env` or share it in screenshots.

## MongoDB Atlas setup
1. Create/choose a cluster in MongoDB Atlas.
2. Under Database Access, create a database user and password.
3. Under Network Access, allow your current IP address.
4. Choose Connect > Drivers > Python and copy the connection string.
5. Paste it into `.env`, URL-encoding special characters in the password if necessary.
6. The app creates the `flask_assignment` database and `submissions` collection on first successful insert.

## Run
```powershell
python app.py
```
Open:
- Form: http://127.0.0.1:5000/
- JSON API: http://127.0.0.1:5000/api
- Success page: http://127.0.0.1:5000/success (normally reached after a successful form submission)

## Test checklist
1. Open `/api`; verify a JSON array appears.
2. Submit all three form fields with Atlas configured; verify redirect to `/success` and the exact success message.
3. Submit with a field blank; verify an error appears on the same form page.
4. Temporarily use an invalid MongoDB URI; submit valid fields and verify the connection error appears on the form page. Restore the valid URI afterward.
5. In Atlas Data Explorer, open `flask_assignment.submissions` and verify the inserted document.

## GitHub
Create a public repository named `Flask_and_MongoDB_MohammadImrose`, push this project, then replace the repository link in `documentation.docx` with your actual URL. Do not invent a GitHub URL: a repository must be created under your own account.

## Security notes
- Never put your real Atlas URI in source code, documentation screenshots, or GitHub.
- `.env` is ignored by Git. Submit `.env.example`, not `.env`.
- Debug mode is enabled for local development only. Disable debug mode for deployment.
