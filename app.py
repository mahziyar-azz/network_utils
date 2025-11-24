from flask import Flask, render_template, request, jsonify
from network_utils import calculate_subnet

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    ip = data.get('ip', '').strip()
    cidr = data.get('cidr', '').strip()
    
    # Basic validation before calling logic
    if not ip or not cidr:
        return jsonify({"success": False, "error": "Please provide both IP Address and CIDR."})
        
    result = calculate_subnet(ip, cidr)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)