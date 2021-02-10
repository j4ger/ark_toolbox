#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

sm_ms_upload_url = "https://sm.ms/api/v2/upload"


def new_op(name, codename, rareness, tag, profile_url):
    profile = requests.get(profile_url).content

    post_request = requests.post(sm_ms_upload_url, files={"smfile": profile})

    if not (post_request.json()["success"]):
        raise Exception("Upload process for " + name + " failed")

    return {
        "profile": post_request.json()["url"],
        "name": name,
        "codename": codename,
        "rareness": rareness,
        "tag": tag,
    }
