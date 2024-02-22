import requests
from bs4 import BeautifulSoup
from dynaconf import Dynaconf
import argparse
import pprint

SEARCH_VALUE = "black hat python"
COL_NAMES = [
    "ID",
    "Author",
    "Title",
    "Publisher",
    "Year",
    "Pages",
    "Language",
    "Size",
    "Extension",
    "Mirror_1",
    "Mirror_2",
    "Mirror_3",
    "Mirror_4",
    "Mirror_5",
    "Edit",
]


def load_data(search_value):
    source = requests.get("https://www.libgen.is/search.php", {"req": search_value})

    return source.content


def get_table(content):
    soup = BeautifulSoup(content, "html.parser")
    return soup.find("table", {"class": "c"})


def strip_i_tag_from_soup(soup):
    subheadings = soup.find_all("i")
    for subheading in subheadings:
        subheading.decompose()


def aggregate_request_data(information_table):
    raw_data = [
        [
            td.a["href"]
            if td.find("a")
               and td.find("a").has_attr("title")
               and td.find("a")["title"] != ""
            else "".join(td.stripped_strings)
            for td in row.find_all("td")
        ]
        for row in information_table.find_all("tr")[
                   1:
                   ]
    ]

    output_data = [dict(zip(COL_NAMES, row)) for row in raw_data]
    return output_data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query", help="Searching query for library", nargs="*", required=True)
    args = parser.parse_args()
    search_str = args.query

    table = get_table(load_data(search_str))
    result = aggregate_request_data(table)

    for i in result:
        pprint.pprint(i, depth=6)
        print("\t")
