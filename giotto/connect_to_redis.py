from redis import Redis


def connect_to_redis():
    return Redis(host='case.tomlein.org', port=7777)
