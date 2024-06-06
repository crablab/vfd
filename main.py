from infosys import display
from domain import update_display_record
from serial import SerialException
import flask
from time import sleep
from flask import request
import os
import threading
import socket
import logging
import markdown.extensions.fenced_code
from pygments.formatters import HtmlFormatter

def create_app(test_config=None):
  time_event = threading.Event()
  text_event = threading.Event()
  app = flask.Flask(__name__)

  app.config['DISPLAY'] = display()

  # Try to get the IP address of the device
  # Print it to the display and update the DNS record
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))

  ip = socket.gethostbyname(s.getsockname()[0])

  app.config['DISPLAY'].write_text(ip, "split", True)

  domain_status = update_display_record(os.environ['NAME'], ip)

  if domain_status:
      logging.info('Domain Updated')
      app.config['DISPLAY'].write_text("Domain Updated", "split", True)
  else:
      logging.info('Domain Update Failed')
      app.config['DISPLAY'].write_text("Domain Update Failed", "split", True)

  # Background Helper Functions
  def time_background():
      while time_event.is_set():
          d = app.config['DISPLAY']
          try:
            d.print_time()
            time_event.wait(10)
          except SerialException as e:
            logging.warn('Time could not get lock')
            return
  
  def text_background(msg: str, effect: str, wipe: bool):
      while text_event.is_set():
          d = app.config['DISPLAY']
          try:
            d.write_text(msg, effect, wipe)
            text_event.wait(10)
          except SerialException as e:
            logging.warn('Text could not get lock')
            return

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
  
  @app.route("/message", methods=["POST"])
  def message():
      time_event.clear()
      text_event.clear()
      text_event.set()
      
      d = app.config['DISPLAY']

      msg = request.form["message"]
      effect = request.form["effect"] if "effect" in request.form else "split"
      wipe = request.form["wipe"] if "wipe" in request.form else False

      if len(msg) > 48:
          return "Text too long", 400
      
      thread = threading.Thread(target=text_background, args=(msg, effect, wipe))
      thread.start()

      sleep(1)

      if(thread.is_alive()):
          return "OK", 200
      else:
          return "Display is locked", 503

  @app.route("/time", methods=["GET"])
  def time():
      text_event.clear()
      time_event.clear()
      time_event.set()
      
      thread = threading.Thread(target=time_background)
      thread.start()
      
      sleep(1)
      
      if(thread.is_alive()):
          return "OK", 200

      return "Display is locked", 503

  return app

app = create_app()

if __name__ == "__main__":
    app.run()