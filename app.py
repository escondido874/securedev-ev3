from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)

@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response

@app.route('/hello')
def hello():
    raw_name = request.args.get('name', 'Invitado')
    safe_name = escape(raw_name)
    return f"Hello, {safe_name}!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)