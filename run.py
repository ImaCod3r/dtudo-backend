from app import init_app

app = init_app()

if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True, threaded=False, use_reloader=False)
