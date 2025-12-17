🎅 Secret Santa
A simple Secret Santa web app built with **Flask**, **Pandas**, and plain **HTML/CSS/JS**. Participants enter an email, pick a number card, and get a randomly assigned giftee. Assignments are saved to an Excel file to prevent duplicates.
---

🚀 Getting Started

1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/secret-santa.git
cd secret-santa

2️⃣ Create a Virtual Environment (Optional but Recommended)
bash
Copy code
python -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows

3️⃣ Install Dependencies
bash
Copy code
pip install flask pandas openpyxl

4️⃣ Run the Application
bash
python app.py
The app will start on:
http://127.0.0.1:5000


How it works (one line)

User submits email → verified against the built-in list → picks a card → assignment saved to `secret_santa_assignments.xlsx`.

---

Files

* `app.py` — Flask app and logic
* `templates/index.html` — email entry page
* `templates/reveal.html` — pick-a-number & reveal page
* `secret_santa_assignments.xlsx` — created automatically when someone gets assigned

---

Notes

* Edit participant names/emails in `load_employees()` inside `app.py`.
* For production use replace Excel with a proper database and enable HTTPS.

---

License

MIT — feel free to adapt.
