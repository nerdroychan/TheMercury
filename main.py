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
        f.write(template.render(title=conf["title"], update_time=gen["update_time"], entries=gen["entries"], victims=gen["fail_list"], subscriptions=sorted(conf["subscriptions"], key=lambda x: x["title"])))

    return len(gen["fail_list"])

def job():
    fetch()
    f = gen()
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").join(["[", "]"]) + " Job finished with " + str(f) + " failures.")

job()

schedule.every().day.at("00:00").do(job)
schedule.every().day.at("01:00").do(job)
schedule.every().day.at("06:00").do(job)
schedule.every().day.at("07:30").do(job)
schedule.every().day.at("09:00").do(job)
schedule.every().day.at("10:00").do(job)
schedule.every().day.at("11:00").do(job)
schedule.every().day.at("12:00").do(job)
schedule.every().day.at("13:00").do(job)
schedule.every().day.at("14:00").do(job)
schedule.every().day.at("15:00").do(job)
schedule.every().day.at("16:00").do(job)
schedule.every().day.at("17:00").do(job)
schedule.every().day.at("18:00").do(job)
schedule.every().day.at("19:00").do(job)
schedule.every().day.at("20:00").do(job)
schedule.every().day.at("21:00").do(job)
schedule.every().day.at("22:00").do(job)
schedule.every().day.at("23:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(schedule.idle_seconds())