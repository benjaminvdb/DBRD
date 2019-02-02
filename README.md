# 110kDBRD: 110k Dutch Book Reviews Dataset
This repository contains scripts to scrape [Hebban](https://www.hebban.nl) for Dutch book reviews that can be used for research purposes, e.g. sentiment analysis.

## Install dependencies

### ChromeDriver
I'm making using of [Selenium](https://www.seleniumhq.org) for automating user actions such as clicks. This library requires a browser driver that provides the rendering backend. I've made use of [ChromeDriver](http://chromedriver.chromium.org/).

#### macOS
If you're on macOS and you have Homebrew installed, you can install ChromeDriver by running:

    brew install chromedriver
    
#### Other OSes
You can download ChromeDriver from the official [download page](http://chromedriver.chromium.org/downloads).

### Python
The scripts are written for **Python 2**, but I'm sure they'll work for Python 3 with minor adjustments. To install the Python dependencies, run:     

    pip install -r ./requirements.txt


## Run
Two scripts are provided that can be run in sequence. You can also run `run.sh` to run all scripts with defaults.

### Gather URLs
The first step is to gather all review URLs from [Hebban](https://www.hebban.nl). Run `gather_urls.py` to fetch them and save them to a text file.

```
Usage: gather_urls.py [OPTIONS] OUTFILE

  This script gathers review urls from Hebban and writes them to OUTFILE.

Options:
  --offset INTEGER  Review offset.
  --step INTEGER    Number of review urls to fetch per request.
  --help            Show this message and exit.
```

### Scrape URLs
The second step is to scrape the URLs for review data. Run `scrape_reviews.py` to iterate over the review URLs and save the scraped data to a JSON file.

```
Usage: scrape_reviews.py [OPTIONS] INFILE OUTFILE

  Iterate over review urls in INFILE text file, scrape review data and
  output to OUTFILE.

Options:
  --encoding TEXT   Output file encoding.
  --indent INTEGER  Output JSON file with scraped data.
  --help            Show this message and exit.
```

## License

All code in this repository is licensed under a MIT License.

The dataset is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).
