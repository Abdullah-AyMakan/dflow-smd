from .downloader import download_snaps
from rich import print
from .helpers import *
import requests


class SnapchatScrapper:
    def __init__(
            self,
            directory_prefix="./data",
            max_workers=15,
    ):
        self.directory_prefix = os.path.abspath(os.path.normpath(directory_prefix))
        self.max_workers = max_workers
        self.endpoint_web = "https://story.snapchat.com/@{}"
        self.regexp_web_json = (
            r'<script\s*id="__NEXT_DATA__"\s*type="application\/json">([^<]+)<\/script>'
        )
        # self.response_ok = requests.codes.get("ok")
        self.total = 0

    def _call_api(self, username):
        web_url = self.endpoint_web.format(username)
        return requests.get(web_url).text

    def _fetch_info(self, username):

        response = self._call_api(username)
        response_json_raw = re.findall(self.regexp_web_json, response)

        try:
            response_json = json.loads(response_json_raw[0])
            user_info = fetch_user_info(response_json)
            stories = fetch_user_story(response_json)

            return stories, user_info

        except (IndexError, KeyError, ValueError):
            raise APIResponseError

    def download(self, username, executor):

        stories, snap_user = self._fetch_info(username)

        if len(stories) == 0:
            raise NoStoriesFound

        print(f"[[green bold]✔[/]] User '{username}' has {len(stories)} stories, Downloading them ...")
        self.total = self.total + len(stories)

        # executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers)
        # try:
        for media in stories:

            # snap_id = media["snapId"]["value"]
            media_url = media["snapUrls"]["mediaUrl"]
            media_type = media["snapMediaType"]
            try:
                timestamp = int(media["timestampInSec"]["value"])
            except Exception:
                timestamp = -2208988800

            date_str = strf_time(timestamp, "%Y-%m-%d")
            dir_name = os.path.join(
                self.directory_prefix,
                username,
                date_str,
                'images' if media_type == 0 else 'videos'
            )

            filename = strf_time(timestamp, f"[{username}]_%Y-%m-%d_%H:%M:%S.{MEDIA_TYPE[media_type]}")

            media_output = os.path.join(dir_name, filename)
            executor.submit(download_snaps, media_url, media_output)

        # except KeyboardInterrupt:
        #     executor.shutdown(wait=True)
