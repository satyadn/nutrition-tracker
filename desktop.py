import threading
import webview

from app import app


def run_flask():
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )


threading.Thread(
    target=run_flask,
    daemon=True
).start()

webview.create_window(
    "Nutrition Tracker",
    "http://127.0.0.1:5000",
    width=1400,
    height=900
)

webview.start()