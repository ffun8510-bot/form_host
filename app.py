from flask import Flask, request, jsonify, render_template
import requests
import json

app = Flask(__name__)

# Your JSONBin details
JSONBIN_URL = "https://api.jsonbin.io/v3/b/690e205243b1c97be99f2a05"
HEADERS = {
    "Content-Type": "application/json",
    "X-Master-Key": "$2a$10$WU7PPo/z/W99mt.UMHbcSuHe3BW1x/Dn.CrJcCtb.vw8iXyJZUlM6"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Prepare current submission
    new_entry = {
        "name": name,
        "email": email,
        "message": message
    }

    try:
        # 1️⃣ Fetch existing data
        existing = requests.get(JSONBIN_URL, headers=HEADERS)
        if existing.status_code == 200:
            data = existing.json()
            current_list = data.get("record", [])
            if not isinstance(current_list, list):
                current_list = []
        else:
            current_list = []

        # 2️⃣ Append new entry
        current_list.append(new_entry)

        # 3️⃣ Save updated list back to JSONBin
        response = requests.put(JSONBIN_URL, headers=HEADERS, data=json.dumps(current_list))

        if response.status_code == 200:
            return jsonify({"message": "✅Success"})
        else:
            return jsonify({"message": "❌ Failed "}), 400

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "⚠️ Server error, please try again."}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)



