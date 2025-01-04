from decouple import config

MQTT_BROKER = config("MQTT_BROKER")
MQTT_PORT = config("MQTT_PORT", cast=int)
REDIS_HOST = config("REDIS_HOST")
REDIS_PORT = config("REDIS_PORT", cast=int)