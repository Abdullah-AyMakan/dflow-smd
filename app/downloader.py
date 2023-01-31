import os
import requests


def download_snaps(url: str, dest: str):

    if len(os.path.dirname(dest)) > 0:
        os.makedirs(os.path.dirname(dest), exist_ok=True)

    if not os.path.isfile(dest):
        try:
            response = requests.get(url, stream=True, timeout=10)
        except requests.exceptions.ConnectTimeout:
            response = requests.get(url, stream=True, timeout=10)

        if response.status_code != requests.codes.get("ok"):
            raise response.raise_for_status()

        if os.path.isfile(dest) and os.path.getsize(dest) == 0:
            os.remove(dest)

        try:
            with open(dest, "xb") as handle:
                try:
                    for data in response.iter_content(chunk_size=4194304):
                        handle.write(data)
                    handle.close()
                except requests.exceptions.RequestException as e:
                    pass
        except FileExistsError as e:
            pass
