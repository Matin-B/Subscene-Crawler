#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: matin
"""
import requests
from bs4 import BeautifulSoup as bs4


def popular_movie():
    try:
        response = requests.get(base_url)
        soup = bs4(response.text, 'html.parser')
        subs = soup.find_all('div', {'class': 'box'})[0]
        subtitles = dict()
        for sub in subs.find_all('div', {'class': 'title'}):
            name = sub.find('a').text.strip()
            link = base_url + sub.find('a')['href']
            subtitles[name] = link
        return subtitles
    except Exception as e:
        return f'Error, {e}'


def popular_tv():
    try:
        response = requests.get(base_url)
        soup = bs4(response.text, 'html.parser')
        subs = soup.find_all('div', {'class': 'box'})[1]
        subtitles = dict()
        for sub in subs.find_all('div', {'class': 'title'}):
            name = sub.find('a').text.strip()
            link = base_url + sub.find('a')['href']
            subtitles[name] = link
        return subtitles
    except Exception as e:
        return f'Error, {e}'


def search(name):
    name = name.replace(' ', '+')
    url = base_url + f'/subtitles/searchbytitle?query={name}'
    try:
        response = requests.get(url)
        soup = bs4(response.text, 'html.parser')
        subs = dict()
        if 'Exact' in response.text:
            box = soup.select_one('.exact+ ul').find_all('a')
            for item in box:
                item_name = item.text.strip()
                item_link = base_url + item['href']
                subs[item_name] = item_link
        if 'TV-Series' in response.text:
            box = soup.select_one('ul:nth-child(2)').find_all('a')
            for item in box:
                item_name = item.text.strip()
                if 'Season' in item_name:
                    item_link = base_url + item['href']
                    subs[item_name] = item_link
        if 'Close' in response.text:
            box = soup.select_one('ul:nth-child(4)').find_all('a')
            for item in box:
                item_name = item.text.strip()
                item_link = base_url + item['href']
                subs[item_name] = item_link
        if 'Popular' in response.text:
            box = soup.select_one('#left').find_all('a')
            count = 1
            for item in box:
                if count <= 5:
                    item_name = item.text.strip()
                    item_link = base_url + item['href']
                    subs[item_name] = item_link
                    count += 1
        subtitles = dict()
        for key, value in subs.items():
            if value not in subtitles.values():
                subtitles[key] = value
        return subtitles
    except Exception as e:
        return f'Error, {e}'


def download(url, file_name=None):
    response = requests.get(url)
    try:
        soup = bs4(response.text, 'html.parser')
        preview = str(soup.find('p'))
        preview = preview.replace('<p>', '')
        preview = preview.replace('</p>', '')
        preview = preview.replace('\r', '')
        preview = preview.replace('\t', '')
        preview = preview.replace('&gt;', '>')
        preview = preview.replace('<br/>', '\n')
        download_link = soup.find('a', {'id': 'downloadButton'})['href']
        download_link = base_url + download_link
        author = soup.find('li', {'class': 'author'}).find('a')
        author_name = author.text.strip()
        author_link = base_url + author['href']
        if file_name is None:
            name = requests.get(download_link)
            name = name.headers.get('content-disposition')
            name = name.split('filename=')[-1]
            final_file_name = name
        else:
            name = requests.get(download_link)
            name = name.headers.get('content-disposition')
            name = name.split('filename=')[-1]
            final_file_name = str(file_name) + name
        return (download_link,
                preview,
                author_name,
                author_link,
                final_file_name)
    except Exception as e:
        return f'Error, {e}'


base_url = 'https://subscene.com'
