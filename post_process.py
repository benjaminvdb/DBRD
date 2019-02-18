#!/usr/bin/env python2

import codecs
import json
import os

import click
import sklearn
from progressbar import ProgressBar


def load(infile, keep_incorrect_date=False, unique=True, sort=True, maximum=110000):
    """
    Load reviews from JSON input file.
    """
    with codecs.open(infile, encoding="utf-8") as f:
        reviews = json.load(f)

        if not keep_incorrect_date:
            reviews = filter(lambda x: x is not None and x['published'] >= '2002-09-11T00:00:00+02:00', reviews)

        if unique:
            # Define a unique review as one with a unique review text
            u = {review['text']: review for review in reviews}
            reviews = u.values()

        if sort:
            reviews = sorted(reviews, key=lambda x: x['published'])

        if maximum:
            reviews = reviews[:maximum]

    return reviews


def zipper(list1, list2):
    """
    Zip two lists, alternating values. I.e.: zipper([1,2,3], [4,5,6]) == [1,4,2,5,3,6]
    :return:
    """
    result = [None] * (len(list1) + len(list2))
    result[::2] = list1
    result[1::2] = list2
    return result


def write_supervised(reviews, outdir, start_index):
    """
    Write reviews to OUTDIR with a separate folder for negative and positive reviews.
    """
    os.mkdir(outdir)
    pos_dir = os.path.join(outdir, 'pos')
    neg_dir = os.path.join(outdir, 'neg')
    os.mkdir(pos_dir)
    os.mkdir(neg_dir)
    index = start_index
    bar = ProgressBar()
    for review in bar(reviews):
        rating = review['rating']
        if rating > 3:
            target_dir = pos_dir
        elif rating < 3:
            target_dir = neg_dir
        else:
            raise Exception("rating should be negative or positive!")
        filename = "{}_{}.txt".format(index, rating)
        with codecs.open(os.path.join(target_dir, filename), 'w', encoding='utf-8') as f:
            f.write(review['text'])
        index += 1
    return index


def write_unsupervised(reviews, outdir, start_index):
    """
    Write reviews to OUTDIR (no separate folder for positive and negative).
    """
    os.mkdir(outdir)
    index = start_index
    bar = ProgressBar()
    for review in bar(reviews):
        rating = review['rating']
        filename = "{}_{}.txt".format(index, rating)
        with codecs.open(os.path.join(outdir, filename), 'w', encoding='utf-8') as f:
            f.write(review['text'])
        index += 1
    return index


def write_urls(reviews, outfile):
    """
    Write a provenance file containing an URL for each review.
    """
    with codecs.open(outfile, 'w', encoding='utf-8') as f:
        for review in reviews:
            f.write(review['url'])
            f.write('\n')


@click.command()
@click.argument('infile')
@click.argument('outdir')
@click.option('--encoding', default='utf-8', help='Input file encoding')
@click.option('--keep-incorrect-date', default=False, help='Whether to keep reviews with invalid dates.')
@click.option('--sort', default=True, help='Whether to sort reviews by date.')
@click.option('--maximum', default=110000, help='Maximum number of reviews in output')
@click.option('--valid-size-fraction', default=0.1, help='Fraction of total to set aside as validation.')
@click.option('--shuffle', default=True, help='Shuffle data before saving.')
def process(infile, outdir, encoding, keep_incorrect_date, sort, maximum, valid_size_fraction, shuffle):
    reviews = load(infile, keep_incorrect_date, sort, encoding, maximum)

    if shuffle:
        sklearn.utils.shuffle(reviews)

    pos = filter(lambda x: x['rating'] > 3, reviews)
    neg = filter(lambda x: x['rating'] < 3, reviews)
    neut = filter(lambda x: x['rating'] == 3, reviews)  # set aside for model fine-tuning

    # Balance dataset
    train_size = min(len(pos), len(neg))
    train_size -= train_size % 2  # make even
    sup = zipper(pos[:train_size], neg[:train_size])  # alternate positive and negative samples
    unsup = pos[train_size:] + neg[train_size:] + neut

    end = int(round(float(len(sup)) * valid_size_fraction))
    end -= end % 2  # make even

    # Because sup contains alternating labels like [pos, neg, pos, neg...] we can split anywhere as long as end is even
    test = sup[:end]
    train = sup[end:]

    print("Size all data:\t{}".format(len(reviews)))
    print("Size supervised:\t{}".format(len(sup)))
    print("Size unsupervised:\t{}".format(len(unsup)))
    print("Size training:\t{}".format(len(train)))
    print("Size testing:\t{}".format(len(test)))

    os.mkdir(outdir)

    index = 1
    print("Writing train data...")
    index = write_supervised(train, os.path.join(outdir, 'train'), index)

    print("Writing test data...")
    index = write_supervised(test, os.path.join(outdir, 'test'), index)

    print("Writing unsupervised data...")
    index = write_unsupervised(unsup, os.path.join(outdir, 'unsup'), index)

    print("Writing URLs...")
    write_urls(train + test + unsup, os.path.join(outdir, 'urls.txt'))

    print("DONE! :)")


if __name__ == '__main__':
    process()
