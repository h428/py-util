import os
import requests
from bs4 import BeautifulSoup


def parse_markdown_line(line):
    indexes = [i for i, c in enumerate(line) if c == '|']
    prev_index = indexes[2]
    name_set = set()
    for i in indexes[3:]:
        name = line[prev_index + 1: i].strip()
        name_set.add(name)
        prev_index = i
    return name_set


def parse_markdown_names(path):
    with open(path, "r", encoding="utf-8") as file:
        found = False
        lines = file.readlines()

        file_name_set = set()
        repeat_name_set = set()

        for line in lines:

            if line == "":
                break

            if line.find("蒋长志") != -1:
                found = True

            if not found:
                continue

            line = line.strip()

            if not line.startswith("|"):
                continue

            line_name_set = parse_markdown_line(line)
            line_repeat_name_set = file_name_set.intersection(line_name_set)

            if len(line_repeat_name_set) != 0:
                # 有重合
                repeat_name_set = repeat_name_set.union(line_repeat_name_set)

            file_name_set = file_name_set.union(line_name_set)

    return file_name_set, repeat_name_set


def get_wikipedia_name_set():
    headers = {'Accept-Language': 'zh-CN,zh;q=0.9'}
    url = "https://zh.wikipedia.org/wiki/%E5%9B%BE%E7%81%B5%E5%A5%96"
    response = requests.get(url, headers=headers)
    html_content = response.content

    soup = BeautifulSoup(html_content, "html.parser")

    table = soup.select(".wikitable")[0]
    trs = table.select("tr:not([bgcolor])")

    count = 0
    wiki_name_set = set()
    for tr in trs:
        name = tr.select("td a")[0].string
        if name == "[5]":
            name = tr.select("td a")[1].string
        wiki_name_set.add(name)
        count = count + 1

    return wiki_name_set


if __name__ == '__main__':
    file_name_set, repeat_name_set = parse_markdown_names(r"D:\code\dmci\book-of-turing-award\任务分工表.md")
    wiki_name_set = get_wikipedia_name_set()
    union = file_name_set.union(wiki_name_set)
    intersection = file_name_set.intersection(wiki_name_set)

    print(f"图灵奖数量：{len(wiki_name_set)}")
    print(f"并集长度：{len(union)}")
    print(f"名字不规范集合：{file_name_set - intersection}")
    print(f"重名集合：{repeat_name_set}")
    print(f"交集长度：{len(intersection)}")
    print(f"未提交集合：{wiki_name_set - intersection}")
