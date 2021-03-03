from urllib.parse import urlparse, parse_qs
import requests
import dataclasses
import time
import os

@dataclasses.dataclass
class RequestParams():
    url: str = "https://disk.yandex.ru/i/5VUzafO0YwMIyw"

body = RequestParams()



base_url = "https://cloud-api.yandex.net:443/v1/disk/public/resources/download?public_key={}"
url_format = base_url.format(body.url)

response = requests.get(url_format)

if response.status_code != 200:
    raise Error.make(_message="Failed getting download url")

download_url = response.json()["href"]

query_params = parse_qs(urlparse(download_url).query)

filetype = query_params["filename"].rsplit(".", 1)[1]

dir_path = "{}".format(filetype)
file_name = '{}.{}'.format(
    time.time(),
    filetype
)

full_path_dir = os.path.join(
    "./storage/" # config.app.storage_path,
    dir_path
)
full_path_file = os.path.join(full_path_dir, file_name)

if not os.path.exists(full_path_dir):
    os.makedirs(full_path_dir)

response = requests.get(download_url, stream=True)

with open(full_path_file, '+wb') as f:
    response.raw.decode_content = True
    for chunk in response:
        f.write(chunk)
    f.close()

def _get_loader():
    ...