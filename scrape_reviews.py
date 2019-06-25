#!/usr/bin/env python3

import time
import codecs
import json

import click
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from progressbar import ProgressBar


# NOTE: this is often needed when a page is still loading
def retry(fun, arg, max_retries=10, sleep=0.5):
    """
    Retry executing function FUN with arguments ARG.
    :param fun: function to execute
    :param arg: argument to pass to FUN
    :param max_retries: maximum number of retries
    :param sleep: number of seconds to sleep in between retries
    :return:
    """
    data = fun(arg)
    retries = 0
    while not data and retries < max_retries:
        time.sleep(sleep)
        data = fun(arg)
        retries = retries + 1
    return data if data else []


@click.command()
@click.argument('infile')
@click.argument('outfile')
@click.option('--encoding', default='utf-8', help='Output file encoding.')
@click.option('--indent', default=2, help='Output JSON file with scraped data.')
def scrape(infile, outfile, encoding, indent):
    """
    Iterate over review urls in INFILE text file, scrape review data and output to OUTFILE.
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    urls = [line.strip() for line in open(infile)]

    reviews = []
    bar = ProgressBar()
    errors = []
    for url in bar(urls):
        try:
            driver.get(url)
            title = retry(driver.find_elements_by_css_selector, "div[itemprop='itemReviewed']")
            author = retry(driver.find_elements_by_css_selector, "a[class='author']")
            reviewer = retry(driver.find_elements_by_class_name, 'user-excerpt-name')
            rating = retry(driver.find_elements_by_css_selector, '.fa-star.full')
            text = retry(driver.find_elements_by_xpath, '//../following-sibling::p')
            published = retry(driver.find_elements_by_css_selector, "meta[itemprop='datePublished'")

            if text and rating:
                text = '\n'.join([p.text.strip() for p in text]).strip()
                if text:
                    reviews.append({
                        'url': url,
                        'title': title[0].get_attribute('data-url').strip() if title else None,
                        'author': author[0].get_attribute('href').strip() if author else None,
                        'reviewer': reviewer[0].get_attribute('href').strip() if reviewer else None,
                        'rating': len(rating),
                        'text': text,
                        'published': published[0].get_attribute('content').strip() if published else None
                    })
        except Exception:
            errors.append(url)
            print("Error {len(errors)}: {url}")
            continue

    print(f"Finished scraping {len(urls)} urls with {len(errors)}")

    print(f"Writing reviews to {outfile}")
    with codecs.open(outfile, 'w', encoding=encoding) as f:
        json.dump(reviews, f, ensure_ascii=False, indent=indent)


if __name__ == '__main__':
    scrape()