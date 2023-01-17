import os
import re

import requests
from bs4 import BeautifulSoup
import time
import sys

URL = 'https://www.nhk.or.jp/s-media/news/podcast/list/v1/all.xml'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}


class NHKNews:
    def __init__(self):
        self.counter = 0
        if sys.platform == 'darwin':
            self.DOWNLOADDIR = os.path.expanduser('~/Downloads')
        self.titles, self.urls = self.get_data()

    def get_data(self):
        """get news titles and urls"""
        res = requests.get(URL, headers=HEADERS)
        if res.status_code == 200:
            xml = res.text
            soup = BeautifulSoup(xml, features='xml')
            titles = [tag.text for tag in soup.find_all('title')]
            urls = [tag['url'] for tag in soup.find_all('enclosure')]
            return titles[1:], urls
        else:
            if self.counter < 5:
                print('Source Connecting Error, 5 seconds later try again...')
                time.sleep(5)
                self.get_data()
            else:
                print('Connection Failed')

    def refresh(self):
        self.__init__()

    @staticmethod
    def print_list(ls: list):
        for n, item in enumerate(ls):
            print(n + 1, ls[n])

    def print_titles(self):
        self.print_list(self.titles)

    def write(self, title: str, data: bin):
        path = os.path.join(self.DOWNLOADDIR, title + '.mp3')
        with open(path, 'wb') as f:
            f.write(data)

    def download(self, news_number: int) -> None:
        res = requests.get(self.urls[int(news_number)], headers=HEADERS)
        if res.status_code == 200:
            self.write(self.titles[news_number], res.content)
            print(f'News titled {self.titles[int(news_number)]} downloaded successfully.')
            print('-' * 79)

    def print_download_menu(self):
        menu = [f'Input a number range from 1 to {len(self.urls)}',
                'Input "all" to download all',
                'Input a range like "3-5" to download multiple news links',
                'Input "q" to quit']
        self.print_list(menu)

    # TODO Print Command Menu


def main():
    nhknews = NHKNews()
    while True:
        nhknews.print_titles()
        nhknews.print_download_menu()
        user_input = input()
        if user_input.isdigit():
            nhknews.download(int(user_input) - 1)
        if user_input.lower() == 'q':
            return
        if user_input.lower() == 'all':
            [nhknews.download(number) for number in range(len(nhknews.titles))]
        if m := re.match('\s*(\d+)\s*-\s*(\d+)\s*', user_input):
            # TODO check range invalidation
            [nhknews.download(number) for number in range(int(m.group(1)) - 1, int(m.group(2)))]


if __name__ == '__main__':
    main()
