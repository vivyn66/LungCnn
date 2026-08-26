from App import app
import os

if __name__ == "__main__":
    from waitress import serve
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting production server on http://0.0.0.0:{port} ...")
    serve(app, host="0.0.0.0", port=port)
