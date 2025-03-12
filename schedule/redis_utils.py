from redis_client import redis_client, LOCK_EXPIRATION_TIME
def lock_schedule(id):
    key = id
    acquired = redis_client.set(key, "locked", ex=LOCK_EXPIRATION_TIME, nx=True)
    return acquired
    
def unlock_schedule(id):
    key = id
    redis_client.delete(key)
    return "Seat unlocked"