# bucket-brigade
Brute force aws and google cloud platform buckets

# Help
usage: brute_custom_multithread_v2.py [-h] [-t [THREAD_COUNT]] -k KEYWORD
                                      [-s3] [-gc] [-p PERMUTATIONS_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -t [THREAD_COUNT], --thread-count [THREAD_COUNT]
                        Custom number of threads for requests
  -k KEYWORD, --keyword KEYWORD
                        bucket root to make permutations
  -s3, --s3-bucket      bucket root to make permutations
  -gc, --google-bucket  bucket root to make permutations
  -p PERMUTATIONS_FILE, --permutations-file PERMUTATIONS_FILE
                        bucket root to make permutations
