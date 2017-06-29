import jinja2
import yaml
from fetch import fetch
import schedule
import time
import datetime

def gen():
    TEMPLATE_FILE = "./index.jinja2"
    GENERATE_FILE = "./gen.yaml"
    CONFIG_FILE = "./config.yaml"
    INDEX_FILE = "./web/index.html"

    with open(TEMPLATE_FILE) as f:
        template = jinja2.Template(f.read())

    with open(GENERATE_FILE) as f:
        gen = yaml.load(f.read())

    with open(CONFIG_FILE) as f:
        conf = yaml.load(f.read())

    with open(INDEX_FILE, "w") as f:
        f.write(template.render(title=conf["title"], update_time=gen["update_time"], entries=gen["entries"], victims=gen["fail_list"]))

def job():
    try:
        fetch()
    except:
        with open("error.log", "w+") as f:
            f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Error while fetching.")
    try:
        gen()
    except:
        with open("error.log", "w+") as f:
            f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Error while generating.")

job()

schedule.every(30).minutes.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)