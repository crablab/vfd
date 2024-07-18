from domain import update_display_record
import flask
from infosys import display
from rabbit import time_background, text_background, display_tasks
from time import sleep
from flask import request, render_template
import os
import threading
import socket
import logging
import markdown.extensions.fenced_code
from pygments.formatters import HtmlFormatter

logging.basicConfig(level=logging.INFO)

def create_app(test_config=None):
  time_event = threading.Event()
  text_event = threading.Event()
  app = flask.Flask(__name__)

  display = display()

  # Try to get the IP address of the device
  # Print it to the display and update the DNS record
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))

  ip = socket.gethostbyname(s.getsockname()[0])

  display.write_text(ip, "split", True)

  domain_status = update_display_record(os.environ['NAME'], ip)

  if domain_status:
      logging.info('Domain Updated')
      display.write_text("Domain Updated", "split", True)
  else:
      logging.info('Domain Update Failed')
      display.write_text("Domain Update Failed", "split", True)

  # Endpoints 
  @app.route("/")
  def index():
      formatter = HtmlFormatter(style="emacs",full=True,cssclass="codehilite")
      css_string = formatter.get_style_defs()
      readme_file = open("README.md", "r")

      md_template_string = markdown.markdown(
          readme_file.read(), extensions=["fenced_code"]
      )

      md_css_string = "<style>" + css_string + "</style>"
      md_template = md_css_string + md_template_string
      return md_template
  
  @app.route("/demo")
  def demo():
      return render_template("demo.html")

  @app.route("/message", methods=["POST"])
  def message():
      msg = request.form["message"]
      effect = request.form["effect"] if "effect" in request.form else "split"
      wipe = request.form["wipe"] if "wipe" in request.form else False

      if len(msg) > 48:
          return "Text too long", 400
      
      text_background.delay(msg, effect, wipe)

      return "OK - Task Enqueued", 200

  @app.route("/time", methods=["GET"])
  def time():
      time_background.delay()

      return "OK - Task Enqueued", 200

  return app

app = create_app()

if __name__ == "__main__":
    app.run()

    sleep(20)
    # Starts the Celery worker
    worker = display_tasks.Worker()
    worker.start()