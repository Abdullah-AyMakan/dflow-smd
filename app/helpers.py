import json
import os
import re
from datetime import datetime

MEDIA_TYPE = ["jpg", "mp4"]


class NoStoriesFound(Exception):
    pass


class APIResponseError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


def strf_time(timestamp, format_str):
    return datetime.utcfromtimestamp(timestamp).strftime(format_str)


def fetch_user_info(content: dict):
    if "userProfile" in content["props"]["pageProps"]:
        user_profile = content["props"]["pageProps"]["userProfile"]
        field_id = user_profile["$case"]
        return user_profile[field_id]
    else:
        raise UserNotFoundError


def fetch_user_story(content: dict):
    stories_list = []

    gen = content['props']['pageProps']
    has_curated = gen['userProfile']['publicProfileInfo']['hasCuratedHighlights']
    has_spotlight = gen['userProfile']['publicProfileInfo']['hasSpotlightHighlights']
    has_story = "story" in gen

    if has_curated:
        for s in gen['curatedHighlights']:
            [stories_list.append(s['snapList'][ss]) for ss in range(len(s['snapList']))]

    if has_spotlight:
        for s in gen['spotlightHighlights']:
            [stories_list.append(s['snapList'][ss]) for ss in range(len(s['snapList']))]

    if has_story:
        [stories_list.append(gen["story"]['snapList'][ss]) for ss in range(len(gen["story"]["snapList"]))]

    return stories_list


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def banner():
    return """
  ______   _______ __                
 |   _  \ |   _   |  .-----.--.--.--.
 |.  |   \|.  1___|  |  _  |  |  |  |
 |.  |    |.  __) |__|_____|________|
 |:  1    |:  |                      
 |::.. . /|::.|                      
 `------' `---'                                 SMD v69.0
 ________________________________________________________                                           
"""
