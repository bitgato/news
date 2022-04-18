#!/usr/bin/env python3
import textwrap
import argparse
from termcolor import cprint
from termcolor import colored
from urllib import request
from bs4 import BeautifulSoup


class News(object):
    def __init__(self):
        self.headlines = []
        self.details = []
        self.links = []
        self.url = "https://www.indiatoday.in/india"
        self.parse_args()

    def parse_args(self):
        parser = argparse.ArgumentParser(prog="news",
                                         description="news - get news from indiatoday.in")
        parser.add_argument("-w", "--world", action="store_true",
                            help="show world news")
        parser.add_argument("-t", "--tech", action="store_true",
                            help="show technology news")
        parser.add_argument("-c", "--cricket", action="store_true",
                            help="show cricket news")
        parser.add_argument("-e", "--education", action="store_true",
                            help="show education news")
        args = parser.parse_args()
        if args.world:
            self.url = "https://www.indiatoday.in/world"
        if args.tech:
            self.url = "https://www.indiatoday.in/technology/news"
        if args.cricket:
            self.url = "https://www.indiatoday.in/sports/cricket"
        if args.education:
            self.url = "https://www.indiatoday.in/education-today/news"

    def get_news(self):
        with request.urlopen(self.url) as page:
            content = BeautifulSoup(page, features="lxml")
            divs = content.find_all("div", class_="catagory-listing")
            for div in divs:
                headline = div.find("h2")
                if headline is None:
                    continue
                headline = headline.get_text()
                detail = div.find("p")
                if detail is None:
                    continue
                detail = detail.get_text()
                link = div.find("a")['href']
                link = "https://www.indiatoday.in" + link
                self.headlines.append(headline)
                self.details.append(detail)
                self.links.append(link)

    def get_article(self, index):
        with request.urlopen(self.links[index]) as page:
            print()
            content = BeautifulSoup(page, features="lxml")
            divs = content.find_all("div", class_="description")
            for div in divs:
                cprint(self.headlines[index], 'yellow', attrs={"bold"})
                print()
                highlights = div.find_all("p")
                for text in highlights:
                    print(*textwrap.wrap(text.get_text(), width=70), sep="\n")

    def parse_choice(self):
        choice = input(colored("[#] Article you are interested in? ", 'green'))
        try:
            index = int(choice)
            if index <= len(self.headlines):
                self.get_article(index - 1)
            else:
                print()
                print("[!] INVALID CHOICE")
                self.parse_choice()
        except ValueError:
            exit(0)

    def main(self):
        self.get_news()
        length = len(self.headlines)
        for i in range(length):
            cprint(str(i + 1) + ": " + self.headlines[i], 'blue', attrs={'bold'})
            print(self.details[i])
            print()
        self.parse_choice()


if __name__ == "__main__":
    obj = News()
    try:
        obj.main()
    except KeyboardInterrupt:
        pass
    except EOFError:
        pass
