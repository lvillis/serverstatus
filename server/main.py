import uvicorn

from utils import check_config_json
from configs import *

if __name__ == '__main__':
    if not check_config_json():
        exit()
    uvicorn.run('api:app', host=HOST, port=PORT, log_level='info', reload=False)
