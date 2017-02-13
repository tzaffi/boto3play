'''
usage: listBuckets.py [-h] [--bucket BUCKET]

optional arguments:
  -h, --help       show this help message and exit
  --bucket BUCKET  provide a bucket name

EG: to analyze the storage inside the S3 bucket 'edlab-glacier-test' run:
python3 listbuckets.py --bucket edlab-glacier-test 

EG: to analyze the storage inside all the S3 buckets of the configured AWS account run:
python3 listbuckets.py
'''


import sys
import argparse
import timeit
#import json
#import os
#import ntpath
#import datetime as dt
import pprint
import boto3
from functools import reduce

def getBuckets():
    s3 = boto3.resource('s3')
    return {x.name:x for x in s3.buckets.all()}

def getBucketObjects(bucket_name):
    buckets = getBuckets()
    bucket = buckets[bucket_name]
    return {key.key: key for key in bucket.objects.all()}

def getBucketStats(bucket_name):
    start_time = timeit.default_timer()
    objs = getBucketObjects(bucket_name)
    stats = { 'count': 0,
              'size_bytes': 0
    }
    def agg(x_stats, y_key):
        return {'count': x_stats['count'] + 1,
                'size_bytes': x_stats['size_bytes'] + objs[y_key].size
                }
    result = reduce(agg, objs.keys(), stats)
    result['elapsed_time'] = timeit.default_timer() - start_time
    return result

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    buckets = getBuckets()
    print("buckets are:")
    pp.pprint(buckets)

    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket",
                        required=False,
                        type=str,
                        help="provide a bucket name")
    args = parser.parse_args()

    bucketsForConsideration = [x for x in buckets]
    if args.bucket:
        bucketsForConsideration = [args.bucket]

    print("\n\nComputing statistics for the following buckets:")
    pp.pprint(bucketsForConsideration)

    stats = {x:getBucketStats(x) for x in bucketsForConsideration}
    print("\n\nFinal statistics:")
    pp.pprint(stats)
