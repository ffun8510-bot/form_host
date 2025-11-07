from flask import Flask, request, render_template_string
import os, requests

app = Flask(__name__)

REMOTE_STORE_URL = os.environ.get("REMOTE_STORE_URL")

html_form = """
<!doctype html>
<html>
<head><title>Submit Form</title></head>
<body>
  <h2>Enter Details</h2>
  <form method="post" action="/submit">
    <label>Name:</label><br><input name="name" required><br>
    <label>Age:</label><br><input name="age" type="number" required><br>
    <label>Email:</label><br><input name="email" type="email" required><br><br>
    <button type="submit">Submit</button>
  </form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_form)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()

    if not REMOTE_STORE_URL:
        return "REMOTE_STORE_URL not set on server.", 500

    try:
        resp = requests.post(REMOTE_STORE_URL, json=data, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        return f"Error sending to receiver: {e}", 500

    return f"<h3>Form submitted successfully!</h3><p>Response: {resp.text}</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
