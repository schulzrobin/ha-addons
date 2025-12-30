from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <html>
        <head>
            <title>Home Assistant Ingress Add-on</title>
            <style>
                body { font-family: sans-serif; padding: 2em; }
            </style>
        </head>
        <body>
            <h1>🚀 Ingress Add-on läuft</h1>
            <p>Dieses Add-on nutzt Python 3 + Flask.</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    # Ingress nutzt immer 0.0.0.0
    app.run(host="0.0.0.0", port=8099)