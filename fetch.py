import yaml
import feedparser
import os
import shutil
import datetime
import time

def fetch():
    CONF_FILE = os.path.join(os.path.dirname(__file__), "config.yaml")
    FEED_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
    GENERATE_FILE = os.path.join(os.path.dirname(__file__), "gen.yaml")
    DATE_RANK = 30

    fetch_time = datetime.datetime.now()

    # Read the config file first, get the site list to fetch

    with open(CONF_FILE, "r") as f:
        conf = yaml.load(f.read())

    # Clean all the stuffs

    if (os.path.exists(FEED_DATA_DIR)):
        shutil.rmtree(FEED_DATA_DIR)
    os.makedirs(FEED_DATA_DIR)

    # Fetch all the configured sites, save to FEED_DATA_DIR

    for s in conf["subscriptions"]:
        output = None
        try:
            entries = []
            f = feedparser.parse(s["url"])
            for e in f.entries:
                if abs(fetch_time-datetime.datetime.fromtimestamp(time.mktime(e.updated_parsed))).days <= DATE_RANK:
                    c = e.summary
                    if e.get("content"):
                        c = ".".join([e.content[i].value for i in range(len(e.content))])
                    entries.append({
                        "title": e.title,
                        "date": e.updated_parsed,
                        "link": e.link,
                        "content": c,
                        "subscription": s
                    })
            if f.entries == []:
                output = {"status": 0, "subscription": s, "entries": None}
            else:
                output = {"status": 1, "subscription": s, "entries": entries}
        except:
            output = {"status": 0, "subscription": s, "entries": None}
        with open(os.path.join(FEED_DATA_DIR, ".".join([s["title"], "yaml"])), "w") as f:
            yaml.dump(output, f, allow_unicode=True)

    # Generate the time-sorted YAML file to GENERATE_FILE

    gen = {
        "success_list": [],
        "fail_list": [],
        "entries": [],
        "update_time": fetch_time.strftime("%Y-%m-%d %H:%M:%S")
    }
    for root, dirs, files in os.walk(FEED_DATA_DIR):
        for file in files:
            if file.endswith(".yaml"):
                with open(os.path.join(FEED_DATA_DIR, file)) as f:
                    s = yaml.load(f.read())
                    if s["status"] == 0:
                        gen["fail_list"].append(s["subscription"])
                    else:
                        gen["success_list"].append(s["subscription"])
                        gen["entries"] += s["entries"]

    gen["entries"].sort(key=lambda x: x["date"], reverse=True)
    for e in gen["entries"]:
        e["date"] = time.strftime("%Y-%m-%d %H:%M:%S", e["date"])

    with open(".".join([GENERATE_FILE, "tmp"]), "w") as f:
        yaml.dump(gen, f, allow_unicode=True)

    if (os.path.exists(GENERATE_FILE)):
        os.remove(GENERATE_FILE)

    os.rename(".".join([GENERATE_FILE, "tmp"]), GENERATE_FILE)