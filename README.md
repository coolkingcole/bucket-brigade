# bucket-brigade
Brute force aws and google cloud platform buckets

# Help
You must use the s3 or the gc flag.
```
usage: brute_custom_multithread_v2.py [-h] [-t [THREAD_COUNT]] -k KEYWORD
                                      [-s3] [-gc] [-p PERM_FILE]
                                      
optional arguments:
  -h, --help            show this help message and exit
  -t [THREAD_COUNT], --thread-count [THREAD_COUNT] Custom number of threads for requests
  -k KEYWORD, --keyword KEYWORD bucket root to make permutations
  -s3, --s3-bucket      Brute force AWS buckets permutations
  -gc, --google-bucket  Brute force GCP buckets permutations
  -p PERM_FILE, --perm-file PERM_FILE Permutations file
```
