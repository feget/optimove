import redis
from flask import Flask, render_template
from flask import jsonify
from flask import request

USER_IP_STRING = "user_ip"


app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)


@app.route('/', methods=["GET"])
def index():
    requester_ip = request.remote_addr
    reversed_requester_ip = generate_reversed_ip(input_ip=requester_ip)
    reversed_requester_ip_patched = generate_reversed_ip_patched(input_ip=requester_ip)

    update_redis_info(user_ip="new", reversed_ip=reversed_requester_ip_patched)

    return render_template('index.html',
                           requester_ip=requester_ip,
                           reversed_requester_ip=reversed_requester_ip,
                           reversed_requester_ip_patched=reversed_requester_ip_patched,
                           redis_data=get_all_redis_data()
                           )


@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200


def generate_reversed_ip(input_ip):
    return input_ip[::-1]


def generate_reversed_ip_patched(input_ip):
    split_ip = input_ip.split(".")
    return ".".join(split_ip[::-1])


def update_redis_info(user_ip, reversed_ip):
    if not redis_client.exists("{}_{}".format(USER_IP_STRING, user_ip)):
        redis_client.set("{}_{}".format(USER_IP_STRING, user_ip), reversed_ip)


def get_all_redis_data():
    return_list = []
    redis_keys = redis_client.keys()
    for single_key in redis_keys:
        return_list.append({single_key.decode("utf-8"): redis_client.get(name=single_key).decode("utf-8")})
    return return_list
