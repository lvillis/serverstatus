from environs import Env

env = Env()

HOST = env.str('HOST', '0.0.0.0')
PORT = env.int('PORT', 35601)
