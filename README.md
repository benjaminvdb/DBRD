# 110kDBRD: 110k Dutch Book Reviews Dataset

This dataset contains book reviews along with associated binary sentiment polarity labels. It is greatly influenced by the [Large Movie Review Dataset](http://ai.stanford.edu/~amaas/data/sentiment/) and intended as a benchmark for sentiment classification in Dutch. The scripts that were used to scrape the reviews from [Hebban](https://www.hebban.nl) can be found in the [110kDBRD GitHub repository](https://github.com/benjaminvdb/110kDBRD).

# Dataset

## Downloads

The dataset is ~74MB compressed and can be downloaded from here:

**[110k Dutch Book Reviews Dataset](http://bit.ly/2UTtbWh)**


A language model trained with [FastAI](https://github.com/fastai/fastai) on Dutch Wikipedia can be downloaded from here:

**[Dutch language model trained on Wikipedia](http://bit.ly/2trOhzq)**


## Overview

### Directory structure

The dataset includes three folders with data: `test` (test split), `train` (train split) and `unsup` (remaining reviews).
Each review is assigned a unique identifier and can be deduced from the filename, as well as the rating: `[ID]_[RATING].txt`. *This is different from the Large Movie Review Dataset, where each file in a directory has a unique ID, but IDs are reused between folders.*

The `urls.txt` file contains on line `L` the URL of the book review on Hebban for the book review with that ID, i.e., the URL of the book review in `48091_5.txt` can be found on line 48091 of `urls.txt`. It cannot be guaranteed that these pages still exist.

````
.
├── test          // balanced 10% test split
│   ├── neg
│   └── pos:
├── train:        // balanced 90% train split
│   ├── neg
│   └── pos
└── unsup         // unbalanced positive and neutral
└── urls.txt      // urls to reviews on Hebban
````

### Size
````
  #all:           110000 (= #supervised + #unsupervised)
  #supervised:     20928 (= #training + #testing)
  #unsupervised:   89072
  #training:       18836
  #testing:         2092
````

### Labels

Distribution of labels `positive/negative/neutral` in rounded percentages.
````
  training: 50/50/ 0
  test:     50/50/ 0
  unsup:    71/ 0/29
````

Train and test sets are balanced and contain no neutral reviews (for which `rating==3`).

# Reproduce data

Since scraping Hebban induces a load on their servers, it's best to download the prepared dataset instead. This also makes sure your results can be compared to those of others. The scripts and instructions should be used mostly as a starting point for building a scraper for another website.

## Install dependencies

### ChromeDriver
I'm making using of [Selenium](https://www.seleniumhq.org) for automating user actions such as clicks. This library requires a browser driver that provides the rendering backend. I've made use of [ChromeDriver](http://chromedriver.chromium.org/).

#### macOS
If you're on macOS and you have Homebrew installed, you can install ChromeDriver by running:

    brew install chromedriver
    
#### Other OSes
You can download ChromeDriver from the official [download page](http://chromedriver.chromium.org/downloads).

### Python
The scripts are written for **Python 3**=. To install the Python dependencies, run:     

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

### Post-process

The third and final step is to prepare the dataset using the scraped reviews. By default, we limit the number of reviews to 110k, filter out some reviews and prepare train and test sets of 0.9 and 0.1 the total amount, respectively.

```
Usage: post_process.py [OPTIONS] INFILE OUTDIR

Options:
  --encoding TEXT              Input file encoding
  --keep-incorrect-date TEXT   Whether to keep reviews with invalid dates.
  --sort TEXT                  Whether to sort reviews by date.
  --maximum INTEGER            Maximum number of reviews in output
  --valid-size-fraction FLOAT  Fraction of total to set aside as validation.
  --shuffle TEXT               Shuffle data before saving.
  --help                       Show this message and exit.
```

## Acknowledgements

This dataset was created for testing out the [ULMFiT](https://arxiv.org/abs/1801.06146) (by Jeremy Howard and Sebastian Ruder) deep learning algorithm for text classification. It is implemented in the [FastAI](https://github.com/fastai/fastai) Python library that has taught me a lot. I'd also like to thank [Timo Block](https://github.com/tblock) for making his [10kGNAD](https://github.com/tblock/10kGNAD) dataset publicly available and giving me a starting point for this dataset. The dataset structure based on the [Large Movie Review Dataset](http://ai.stanford.edu/~amaas/data/sentiment/) by Andrew L. Maas et al.

## License

All code in this repository is licensed under a MIT License.

The dataset is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).
