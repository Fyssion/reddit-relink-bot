# MIT License
# Copyright (c) 2019-2020 Fyssion
# See LICENSE for license details
#
# This is a rather simple async reddit module,
# but it's good enough for what I need.

import asyncio
import json
from datetime import datetime, timedelta

import aiohttp
from async_timeout import timeout


# Specify the endpoints (urls)
BASE_URL = "https://www.reddit.com"
SUBREDDIT_URL = BASE_URL + "/r/"
REDDITOR_URL = BASE_URL + "/u/"
JSON_URL = "/about.json"
ACCESS_TOKEN_URL = BASE_URL + "/api/v1/access_token"


class Redditor:
    def __init__(self, data):
        # Here we go though the json data and convert
        # each value into an attribute.
        data = data["data"]
        self.data = data
        self.is_employee = data["is_employee"]
        self.name = data["name"]
        self.name_prefixed = "u/" + self.name
        self.link_karma = data["link_karma"]
        self.icon_img = data["icon_img"]
        self.comment_karma = data["comment_karma"]
        self.has_verified_email = data["has_verified_email"]
        self.created_at = datetime.utcfromtimestamp(data["created_utc"])

    def __str__(self):
        return self.name_prefixed


class Subreddit:
    def __init__(self, data):
        data = data["data"]
        self.data = data
        self.display_name = data["display_name"]
        self.display_name_prefixed = data["display_name_prefixed"]
        self.title = data["title"]
        self.header_img = data["header_img"]
        self.icon_img = data["icon_img"]
        self.subscribers = data["subscribers"]
        self.public_description = data["public_description"]
        self.over18 = data["over18"]
        self.description = data["description"]
        self.url = BASE_URL + data["url"]
        self.created_at = datetime.utcfromtimestamp(data["created_utc"])

    def __str__(self):
        return self.display_name_prefixed


class RedditClient:
    def __init__(self, *, loop=None, session=None):
        self.log_in = None
        self.loop = loop or asyncio.get_event_loop()
        self.session = session or aiohttp.ClientSession(loop=self.loop)

    def error_detector(self, data):
        if "error" in data:
            return data["error"]

    async def get_headers(self):
        # You can ignore this section
        if not self.log_in:
            return {}
        else:
            raise NotImplementedError

    async def _fetch(self, url):
        try:
            # Set a timeout of 30 seconds
            async with timeout(30.0):
                headers = await self.get_headers()

                # Fetch the url
                async with self.session.get(url, headers=headers) as resp:
                    # If the get request failed in some way, return None
                    if resp.status != 200:
                        return None

                    # Convert the data to json format
                    data = await resp.json()

        # If the request times out, raise a better error
        except asyncio.TimeoutError:
            raise asyncio.TimeoutError(f"Timed out while fetching '{url}'")

        # This is probably useless, but just in case
        if self.error_detector(data):
            return None

        return data

    async def fetch_subreddit(self, query):
        url = SUBREDDIT_URL + query + JSON_URL

        data = await self._fetch(url)

        # Subreddit kind is t5
        if data["kind"] != "t5":
            return None

        # Convert the json data into something more usable
        subreddit = Subreddit(data)

        return subreddit

    async def fetch_redditor(self, query):
        url = REDDITOR_URL + query + JSON_URL

        data = await self._fetch(url)

        # Redditor kind is t2
        if data["kind"] != "t2":
            return None

        # Convert the json data into something more usable
        redditor = Redditor(data)

        return redditor
