import Queue
import threading
import urllib2
import time
import sys
from argparse import ArgumentParser

queue = Queue.Queue()
outqueue = Queue.Queue()

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def generate_bucket_permutations(keyword, my_file):
    permutation_templates = [
        '{keyword}-{permutation}',
        '{permutation}-{keyword}',
        '{keyword}_{permutation}',
        '{permutation}_{keyword}',
        '{keyword}{permutation}',
        '{permutation}{keyword}'
    ]
    with open(my_file, 'r') as f:
        permutations = f.readlines()
        buckets = []
        for perm in permutations:
            perm = perm.rstrip()
            for template in permutation_templates:
                generated_string = template.replace('{keyword}', keyword).replace('{permutation}', perm)
                buckets.append(generated_string)

    buckets.append(keyword)
    buckets.append('{}.com'.format(keyword))
    buckets.append('{}.net'.format(keyword))
    buckets.append('{}.org'.format(keyword))
    buckets = list(set(buckets))

    # Strip any guesses less than 3 characters or more than 63 characters
    for bucket in buckets:
        if len(bucket) < 3 or len(bucket) > 63:
            del buckets[bucket]

    print('\nGenerated {} bucket permutations.\n'.format(len(buckets)))
    return [keyword]+buckets

class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue, outqueue,s3bool,gcbool):
        threading.Thread.__init__(self)
        self.s3bool = s3bool
        self.gcbool = gcbool
        self.queue = queue
        self.out_queue = outqueue

    def run(self):
        while True:
            #grabs host from queue
            #print("in: %s" % self.queue.qsize())
            host = self.queue.get()
            chunk = ""
            try:
            #grabs urls of hosts and then grabs chunk of webpage
                if self.s3bool:
                    myurl= 'http://{}.s3.amazonaws.com'.format(host)
                    url = urllib2.urlopen(myurl, timeout=3)
                    if url.getcode() not in [000]:
                        chunk = "AWS: %s" % (host)
                if self.gcbool:
                    myurl='https://www.googleapis.com/storage/v1/b/{}'.format(host)
                    url = urllib2.urlopen(myurl, timeout=3)
                    if url.getcode() not in [000]:
                        chunk = "GCP: %s" % (host)
            except urllib2.HTTPError as e:
                if 'amazon' in myurl and e.code == 401:
                    chunk = "AWS: %s" % (host)
                if 'google' in myurl and e.code == 401:
                    chunk = "GCP: %s" % (host)
                pass    
            #place chunk into out queue
            self.out_queue.put(chunk)

            #signals to queue job is done
            self.queue.task_done()

class DatamineThread(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, out_queue):
        threading.Thread.__init__(self)
        self.out_queue = out_queue

    def run(self):
        while True:
            #print("out: %s" % self.out_queue.qsize())
            #grabs host from queue
            chunk = self.out_queue.get()
            if chunk is not "":
                if chunk[:3] == "AWS":
                    print(bcolors.YELLOW+chunk+bcolors.ENDC)
                if chunk[:3] == "GCP":
                    print(bcolors.GREEN+chunk+bcolors.ENDC)
            #signals to queue job is done
            self.out_queue.task_done()

start = time.time()

def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--thread-count", nargs='?', default=5, type=int, help="Custom number of threads for requests")
    parser.add_argument("-k", "--keyword", required=True, help="bucket root to make permutations")
    parser.add_argument("-s3", "--s3-bucket",action="store_true", help="Brute force AWS buckets permutations")
    parser.add_argument("-gc", "--google-bucket",action="store_true", help="Brute force GCP buckets permutations")
    parser.add_argument("-p", "--permutations-file", default="./permutations.txt", help="Permutations file")
    #parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
    args = parser.parse_args()
    #s3bool=args.s3_bucket
    #gcbool=args.google_bucket
    hosts = generate_bucket_permutations(args.keyword,args.permutations_file)
    #spawn a pool of threads, and pass them queue instance
    for i in range(args.thread_count):
        t = ThreadUrl(queue, outqueue, args.s3_bucket,args.google_bucket)
        t.setDaemon(True)
        t.start()
    #populate queue with data
    for host in hosts:
        queue.put(host)
    # the threads for the writer, it only needs one really.    
    for i in range(20):
        dt = DatamineThread(outqueue)
        dt.setDaemon(True)
        dt.start()
    #wait on the queue until everything has been processed
    queue.join()
    outqueue.join()


if __name__ == '__main__':
    main()
    print("Elapsed Time 4: %s" % (time.time()-start))
