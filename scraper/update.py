#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select as Select
from bs4 import BeautifulSoup
from urllib.parse import unquote

output = "./operators.json"


def new_op(name, codename, rareness, tag, profile_url):
    if not os.path.exists(f"./profiles/{codename}.png"):
        res = requests.get(profile_url)
        if res.status_code == 200:
            with open(f"./profiles/{codename}.png", "wb") as f:
                f.write(res.content)
        else:
            raise ConnectionError(res.status_code)

    return {
        "name": name,
        "codename": codename,
        "rareness": rareness,
        "tag": tag,
    }


options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome("chromedriver", options=options)

op_url = "http://prts.wiki/w/%E5%B9%B2%E5%91%98%E4%B8%80%E8%A7%88"

driver.get(op_url)
select = Select(driver.find_element_by_id("per-page"))
select.select_by_visible_text("500")
op_content = driver.page_source
op_soup = BeautifulSoup(op_content, "html5lib")


def update_data(new_op):
    if not os.path.exists(output):
        current = []
    else:
        f = open(output, "r")
        current = json.loads(f.read())
        f.close()
    if new_op is not None:
        f = open(output, "w")
        current.append(new_op)
        json.dump(current, f)
        f.close()


with open("./tags.json", "r") as f:
    tags_dict = json.load(f)


success = 0

for each in op_soup.find_all("tr", class_="result-row"):
    name = each.contents[1].div.a.div.string
    codename = each.contents[1].div.contents[1].string
    profile_url = each.contents[0].div.a.img["data-src"]
    detail_url = "http://prts.wiki" + each.contents[1].div.a["href"]
    rareness = int(each.contents[0].div.a.contents[1].img["src"][-5:-4]) + 1

    tag = 0

    profession = unquote(each.contents[0].div.a.contents[2].img["src"])[-6:-4]
    tag += tags_dict[profession]

    for each_tag in filter(lambda x: x.name != "br", each.contents[11].div.contents):
        tag += tags_dict[each_tag]
    if rareness == 5:
        tag += tags_dict["资深干员"]
    if rareness == 6:
        tag += tags_dict["高级资深干员"]

    detail_url = "http://prts.wiki" + each.contents[1].div.a["href"]
    driver.get(detail_url)
    detail_content = driver.page_source
    detail_soup = BeautifulSoup(detail_content, "html5lib")

    acquire_method = detail_soup.find(
        "th", style="width:25%; background-color:#797979;", string="获得方式\n"
    ).next_sibling.next_sibling.get_text()
    if "公开招募" in acquire_method:
        tag += tags_dict["公招可见"]

    try:
        add_op = new_op(name, codename, rareness, tag, profile_url)
    except Exception as e:
        print("错误：", e)
        break

    success += 1
    print("添加干员：" + name)
    update_data(add_op)

print("结束，添加总数" + str(success))
