import jinja2
import yaml
from fetch import fetch
import schedule
import time
import datetime
import os

def gen():
    TEMPLATE_FILE = os.path.join(os.path.dirname(__file__), "index.jinja2")
    GENERATE_FILE = os.path.join(os.path.dirname(__file__), "gen.yaml")
    CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.yaml")
    INDEX_FILE = os.path.join(os.path.dirname(__file__), "web/index.html")

    with open(TEMPLATE_FILE) as f:
        template = jinja2.Template(f.read())

    with open(GENERATE_FILE) as f:
        gen = yaml.load(f.read())

    with open(CONFIG_FILE) as f:
        conf = yaml.load(f.read())

    with open(INDEX_FILE, "w") as f:
        f.write(template.render(title=conf["title"], update_time=gen["update_time"], entries=gen["entries"], victims=gen["fail_list"]))

def job():
    fetch()
    gen()

job()

schedule.every().hour.do(job)
while True:
    schedule.run_pending()
    time.sleep(30)