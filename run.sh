#!/usr/bin/env sh

python ./gather_urls.py urls.txt
python ./scrape_reviews.py urls.txt reviews.json