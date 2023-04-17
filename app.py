from dataclasses import asdict
import json
import os
from flask import Flask, request

from data_types.base_types import BaseResponse
from utils.redis_cache_helper import RedisCache

app = Flask(__name__)


@app.route("/index")
def index():
    print(request.environ)
    return {"msg": "Hello World"}


@app.route("/set_cache", methods=["POST"])
def set_redis_cache():
    response = BaseResponse()
    try:
        if request.data == None or request.data == "" or request.data == b"":
            raise Exception("body is none.")

        body = json.loads(request.data)
        project = body.get("project", None)
        key = body.get("key", None)
        value: str = body.get("value", None)
        uid: str = body.get("uid", "")
        checksum: str = body.get("checksum", "")

        if project == None or key == None:
            raise Exception("'project' and 'key' must be required.")
        if value == None:
            raise Exception("'value' can not be none.")
        if not isinstance(value, str):
            raise Exception("'value' must be string.")

        if not isinstance(uid, str):
            raise Exception("'uid' must be string.")
        if not isinstance(checksum, str):
            raise Exception("'checksum' must be string.")

        handle = RedisCache()
        handle.set(project, key, uid, value, checksum)

    except Exception as ex:
        response.errorCode = -1
        response.errorMessage = str(ex)

    return asdict(response)


@app.route("/cache", methods=["POST"])
def redis_cache():
    response = BaseResponse()

    try:
        if request.data == None or request.data == "" or request.data == b"":
            raise Exception("body is none.")

        body = json.loads(request.data)
        project = body.get("project", None)
        key = body.get("key", None)
        if project == None or key == None:
            raise Exception("'project' and 'key' must be required.")

        handle = RedisCache()
        redis_data = handle.get(project, key)
        if redis_data == None:
            raise Exception("can not found any data.")

        response.data = asdict(redis_data)

    except Exception as ex:
        response.errorCode = -1
        response.errorMessage = str(ex)

    return asdict(response)


if __name__ == "__main__":
    port = os.environ.get("WEB_PORT", "8080")
    app.run(host="0.0.0.0", debug=True, port=int(port))