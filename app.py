from flask import Flask, request, jsonify, render_template
import requests
import json

app = Flask(__name__)

# Replace with your actual JSONBin info
JSONBIN_URL = "https://api.jsonbin.io/v3/b/690e205243b1c97be99f2a05"
HEADERS = {
    "Content-Type": "application/json",
    "X-Master-Key": "$2a$10$WU7PPo/z/W99mt.UMHbcSuHe3BW1x/Dn.CrJcCtb.vw8iXyJZUlM6"  # from your JSONBin dashboard
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    # Collect form data
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Create the JSON structure
    form_data = {
        "name": name,
        "email": email,
        "message": message
    }

    # Send to JSONBin
    response = requests.put(JSONBIN_URL, headers=HEADERS, data=json.dumps(form_data))

    if response.status_code == 200:
        return jsonify({"status": "success", "message": "Data saved to JSONBin!"})
    else:
        return jsonify({"status": "error", "message": f"Failed to save data: {response.text}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
