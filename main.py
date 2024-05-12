from infosys import display
import flask
from flask import request
import threading
import socket

thread_event = threading.Event()
app = flask.Flask(__name__)

def backgroundTask():
    while thread_event.is_set():
        d = app.config['DISPLAY']
        d.print_time()
        thread_event.wait(10)

@app.route("/message", methods=["POST"])
def message():
    thread_event.set()
    thread_event.clear()

    d = app.config['DISPLAY']

    msg = request.form["message"]
    effect = request.form["effect"] if "effect" in request.form else "split"
    wipe = request.form["wipe"] if "wipe" in request.form else False
    
    try: 
        d.write_text(msg, effect, wipe)
    except ValueError as e:
        return str(e), 400
    except ConnectionError as e:
        return str(e), 503
    
    return "OK", 200

@app.route("/time", methods=["GET"])
def time():
    thread_event.clear()
    thread_event.set()
    
    thread = threading.Thread(target=backgroundTask)
    thread.start()

    return "OK", 200


if __name__ == "__main__":
    app.config['DISPLAY'] = display()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))

    app.config['DISPLAY'].write_text(socket.gethostbyname(s.getsockname()[0]), "split", True)
    app.run()