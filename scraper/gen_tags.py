#!/usr/bin/env python3
# -*- coding: utf-8 -*-

f = open("tags_list.txt", "r")
s = f.read()
f.close()

output = []
flag = 1
for line in s.split("\n"):
    sec = '"' + line + '":' + str(flag)
    output.append(sec)
    flag *= 2

res = "{" + ",\n".join(output) + "}"

f = open("tags.json", "w")
f.write(res)
f.close()
