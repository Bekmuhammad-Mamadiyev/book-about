from environs import Env

env = str(Env())
env.read_env()
API_TOKEN = env("TOKEN")
