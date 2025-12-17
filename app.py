from flask import Flask, render_template, request, redirect
import gspread
import os
import json
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# --- Google Sheets Setup ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

if os.getenv("GOOGLE_CREDENTIALS"):
    creds_json = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
    credentials = Credentials.from_service_account_info(creds_json, scopes=scope)
else:
    credentials = Credentials.from_service_account_file("file_credentials.json", scopes=scope)

client = gspread.authorize(credentials)
sheet = client.open("FileDirectory").sheet1

# --- ROUTES ---
@app.route('/', methods=['GET', 'POST'])
def home():
    results = None
    if request.method == 'POST':
        keyword = request.form['keyword'].lower()
        records = sheet.get_all_records()
        results = [r for r in records if keyword in r['Title'].lower()]
    return render_template('index.html', results=results)


@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    unit = request.form['unit']
    location = request.form['location']
    file_number = request.form['file_number']
    sheet.append_row([title, unit, location, file_number])
    return redirect('/')

# --- MAIN ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
