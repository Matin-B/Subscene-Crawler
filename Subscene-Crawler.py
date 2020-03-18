#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: matin
"""
import requests
from bs4 import BeautifulSoup as bs4


def popular_movie_subtitles():
    response = requests.get(base_url)
    try:
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


def popular_tv_subtitles():
    response = requests.get(base_url)
    try:
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


def download_subtitle(url, file_name=None):
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
        if file_name == None:
            name = requests.get(download_link)
            name = name.headers.get('content-disposition')
            name = name.split('filename=')[-1]
            final_file_name = name
        else:
            name = requests.get(download_link)
            name = name.headers.get('content-disposition')
            name = name.split('filename=')[-1]
            final_file_name = str(file_name) + name
        return (download_link, preview, author_name, author_link, final_file_name)
    except Exception as e:
        return f'Error, {e}'


base_url = 'https://subscene.com'
