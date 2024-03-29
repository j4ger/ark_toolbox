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

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome("chromedriver", options=options)

op_url = "http://prts.wiki/w/%E5%B9%B2%E5%91%98%E4%B8%80%E8%A7%88"

driver.get(op_url)
select = Select(driver.find_element_by_id("per-page"))
select.select_by_visible_text("500")
op_content = driver.page_source
op_soup = BeautifulSoup(op_content, "html5lib")

with open(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "tags.json",
    ),
    "r",
) as f:
    tags_dict = json.load(f)

success = 0

operators = []

for each in op_soup.find_all("tr", class_="result-row"):
    codename = each.contents[1].div.contents[1].string
    name = each.contents[1].div.a.div.string
    profile_url = "http:" + each.contents[0].div.a.img["data-src"]
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

    retry = 5
    while retry > 0:
        try:
            detail_url = "http://prts.wiki" + each.contents[1].div.a["href"]
            driver.get(detail_url)
            detail_content = driver.page_source
            detail_soup = BeautifulSoup(detail_content, "html5lib")

            acquire_method = detail_soup.find(
                "th", style="width:25%; background-color:#797979;", string="获得方式\n"
            ).next_sibling.next_sibling.get_text()
            break
        except Exception:
            if retry > 0:
                retry -= 1
            else:
                raise ConnectionError(f"获取 {name} 详情错误")

    if "公开招募" in acquire_method:
        tag += tags_dict["公招可见"]

    new_operator = {
        "name": name,
        "codename": codename,
        "rareness": rareness,
        "tag": tag,
    }

    retry = 5
    profile_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f"profiles/{codename}.png",
    )

    if not os.path.exists(profile_file):
        while retry > 0:
            try:
                res = requests.get(profile_url)
                if res.status_code == 200:
                    with open(
                        profile_file,
                        "wb",
                    ) as f:
                        f.write(res.content)
                        break
                else:
                    raise ConnectionError(res.status_code)
            except Exception:
                if retry > 0:
                    retry -= 1
                else:
                    raise ConnectionError(f"5次尝试后下载 {name} 图片仍错误")

    operators.append(new_operator)
    success += 1
    print(f"添加新干员：{name}")
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "operators.json"),
        "w",
    ) as f:
        json.dump(operators, f)

print("结束，新增总数" + str(success))

purge_response = requests.get(
    "https://purge.jsdelivr.net/gh/V04/ark_toolbox@latest/scraper/operators.json"
).json()
print(f"jsDelivr刷新缓存状态：{purge_response}")
