from pprint import pprint
import requests
from bs4 import BeautifulSoup
from lxml import etree
import json

url_main = "https://quotes.toscrape.com/"
url_author = "http://quotes.toscrape.com/author/"

QUOTES_LIST = []
author_list = []


def main():
    response = requests.get(url_main)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")

        tree = etree.HTML(str(soup))

        quote_divs = tree.xpath("//div[@class='quote']")

        for div in quote_divs:
            # print("---------------------------------------------------------------------")
            # Tags
            tag_list = []
            tags_elements = div.xpath(".//div[@class='tags']/a")

            for tags in tags_elements:
                tag_list.append(tags.text)

            # Author
            span_elements = div.xpath(".//span/small")
            if span_elements:
                author = str(span_elements[0].text).strip()

                if not (author in author_list):
                    author_list.append(author)

            # Quot
            span_elements = div.xpath(".//span[@class='text']")

            if span_elements:
                quote = span_elements[0].text

            QUOTES_LIST.append({"tags": tag_list, "author": author, "quote": quote})

        for author in author_list:
            response = requests.get(f"{url_author}/{author}/")
            if response.status_code == 200:
                print(author, "OK")


if __name__ == "__main__":
    main()
    pprint(QUOTES_LIST)
    print(author_list)
