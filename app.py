# app.py
#
# Main app definition
#
# Author: Matt Harrison, Set 4B, A00875065

import connexion
import requests
from connexion import NoContent
import json
import yaml
import datetime
from pykafka import KafkaClient
import logging
import logging.config

DATE_FORMAT_STR = "%Y-%m-%dT%H:%M:%SZ"

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

# TODO: block=False in topic.get_simple_consumer; process_messages function


# Functions
def pickup(**test_params):
    # headers = {"Content-Type": "application/json"}
    # r = requests.post("http://localhost:8090/pickup", json=test_params["body"], headers=headers)

    client = KafkaClient(hosts=app_config["kafka"]["server"] + ':' + str(app_config["kafka"]["port"]))
    topic = client.topics[app_config["kafka"]["topic"]]
    producer = topic.get_sync_producer()
    msg = {"type": "pickup_order",
           "datetime":
               datetime.datetime.now().strftime(DATE_FORMAT_STR),
           "payload": test_params["body"]}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    logging.info("Pickup order submitted")

    # return NoContent, r.status_code
    return NoContent, 200


def delivery(**test_params):
    # headers = {"Content-Type": "application/json"}
    # r = requests.post("http://localhost:8090/delivery", json=test_params["body"], headers=headers)

    client = KafkaClient(hosts=app_config["kafka"]["server"] + ':' + str(app_config["kafka"]["port"]))
    topic = client.topics[app_config["kafka"]["topic"]]
    producer = topic.get_sync_producer()
    msg = {"type": "delivery_order",
           "datetime":
               datetime.datetime.now().strftime(DATE_FORMAT_STR),
           "payload": test_params["body"]}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    logging.info("Delivery order submitted")

    # return NoContent, r.status_code
    return NoContent, 200


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
