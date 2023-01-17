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
        print('\n' + '-' * 79 + '\n')

    def print_titles(self):
        self.print_list(self.titles)

    def write(self, title: str, data: bin):
        path = os.path.join(self.DOWNLOADDIR, title + '.mp3')
        with open(path, 'wb') as f:
            f.write(data)

    def download_single_url(self, news_number: int) -> None:
        res = requests.get(self.urls[int(news_number)], headers=HEADERS)
        if res.status_code == 200:
            self.write(self.titles[news_number], res.content)
            print(f'News titled {self.titles[int(news_number)]} downloaded successfully.')
            print('-' * 79)

    def download(self, command):
        if command.isdigit():
            self.download_single_url(int(command) - 1)
        if command.lower() == 'q':
            return
        if command.lower() == 'all':
            [self.download_single_url(number) for number in range(len(self.titles))]
        if m := re.match('\s*(\d+)\s*-\s*(\d+)\s*', command):
            # download a range
            # TODO check range invalidation
            [self.download_single_url(number) for number in range(int(m.group(1)) - 1, int(m.group(2)))]

    def print_download_menu(self):
        menu = [f'Input a number range from 1 to {len(self.urls)}',
                'Input "all" to download all',
                'Input a range like "3-5" to download multiple news links',
                'Input "q" to quit']
        self.print_list(menu)

    def print_commands_list(self):
        menu = ['List news',
                'Refresh News List',
                'Download']
        self.print_list(menu)

    def run(self):
        while True:
            self.print_commands_list()
            command = input('Enter command number(q to quit): ')
            if command == '1':
                self.print_titles()
            elif command == '2':
                self.refresh()
            elif command == '3':
                self.print_download_menu()
                download_command = input('Enter a download command: ')
                self.download(download_command)
            elif command.lower() == 'q':
                print('See you tomorrow!!!')
                return
            else:
                print("Command is not defined, try again!")


def main():
    nhknews = NHKNews()
    nhknews.run()


if __name__ == '__main__':
    main()
