#!/usr/bin/env python2

import click
import requests
from bs4 import BeautifulSoup


TEMPLATE_URL = 'https://www.hebban.nl/main/Review/more?offset={}&step={}'


@click.command()
@click.argument('outfile')
@click.option('--offset', default=0, help='Review offset.')
@click.option('--step', default=1000, help='Number of review urls to fetch per request.')
def gather(outfile, offset, step):
    """
    This script gathers review urls from Hebban and writes them to OUTFILE.
    """
    urls = []
    while True:
        target_url = TEMPLATE_URL.format(offset, step)
        r = requests.get(target_url)
        data = r.json()

        if not data['html']:
            break

        soup = BeautifulSoup(data['html'], 'lxml')
        new_urls = [div['data-url'] for div in soup('div', {'class': 'item'})]
        print(f"Fetched {len(new_urls)} urls from {len(target_url)}")
        urls.extend(new_urls)
        offset += 1000

    with open(outfile, 'w') as f:
        for url in urls:
            f.write(url)
            f.write('\n')


if __name__ == '__main__':
    gather()