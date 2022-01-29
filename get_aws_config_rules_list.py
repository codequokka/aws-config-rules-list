import re
import csv
import requests
from bs4 import BeautifulSoup


def get_config_rule_uls(target_url):
    response = requests.get(target_url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "lxml")
    unordered_lists = soup.select("#main-col-body > div.highlights > ul")
    return unordered_lists


def get_config_rules_list(unordered_lists, base_url):
    config_rules = []
    for unordered_list in unordered_lists:
        for list_item in unordered_list.find_all("li"):
            name = list_item.text.strip()
            url = base_url + re.sub("^./", "", list_item.a.get("href"))
            config_rules.append({"name": name, "url": url})

    for config_rule in config_rules:
        name = config_rule["name"]
        url = config_rule["url"]
        response = requests.get(url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "lxml")
        paragraph = soup.select("#main-col-body > p")
        config_rule["detail"] = paragraph[0].text

    return config_rules


def main():
    base_url = "https://docs.aws.amazon.com/ja_jp/config/latest/developerguide/"
    target_url = (
        "https://docs.aws.amazon.com/ja_jp/config/latest/developerguide/"
        "managed-rules-by-aws-config.html"
    )
    counfig_rules_list_file = "aws_config_rules_list.csv"

    uls = get_config_rule_uls(target_url)
    config_rules = get_config_rules_list(uls, base_url)

    with open(file=counfig_rules_list_file, mode="w", encoding="utf-8") as file:
        writer = csv.DictWriter(file, ["name", "detail", "url"])
        writer.writeheader()
        writer.writerows(config_rules)
        print("success!")


main()
