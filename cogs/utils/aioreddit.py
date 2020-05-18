"""
This is a simple and incomplete async reddit module. Use at your own risk.


The MIT License (MIT)

Copyright (c) 2020 Fyssion

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import asyncio
import json
from datetime import datetime

import aiohttp
from async_timeout import timeout


BASE_URL = "https://www.reddit.com"
SUBREDDIT_URL = BASE_URL + "/r/"
REDDITOR_URL = BASE_URL + "/u/"
JSON_URL = "/about.json"


class Redditor:
    def __init__(self, data):
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
        self.loop = loop or asyncio.get_event_loop()
        self.session = session or aiohttp.ClientSession(loop=self.loop)

    def error_detector(self, data):
        if "error" in data:
            return data["error"]

    async def fetch_subreddit(self, query):
        try:
            async with timeout(30.0):
                async with self.session.get(SUBREDDIT_URL + query + JSON_URL) as resp:
                    raw = await resp.read()
                    data = json.loads(raw)
        except asyncio.TimeoutError:
            raise asyncio.TimeoutError(f"Timed out while fetching subreddit {query}")

        if self.error_detector(data):
            return None

        if data["kind"] != "t5":
            return None

        subreddit = Subreddit(data)

        return subreddit

    async def fetch_redditor(self, query):
        try:
            async with timeout(30.0):
                async with self.session.get(REDDITOR_URL + query + JSON_URL) as resp:
                    raw = await resp.read()
                    data = json.loads(raw)
        except asyncio.TimeoutError:
            raise asyncio.TimeoutError(f"Timed out while fetching redditor {query}")

        if self.error_detector(data):
            return None

        if data["kind"] != "t2":
            return None

        subreddit = Redditor(data)

        return subreddit
