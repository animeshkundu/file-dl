from accelerator.multiget import MultiGet, HashFailedException, CanceledException
import accelerator.utils

__version__ = '0.0.1'

import os
import sys
import logging
import argparse

def main():
    parser = argparse.ArgumentParser(description="File [ HTTP / FTP ] Download Accelerator")
    parser.add_argument("url", help="The link to download")

    parser.add_argument("--directory", "-d", default=".", help="Directory where the file will be downloaded")
    parser.add_argument("--user", default=None, help="Authentication - Username ")
    parser.add_argument("--password", default=None, help="Authentication - Password")
    parser.add_argument("--parallelism", "-p", default=16, help="Number of parallel downloads")
    parser.add_argument("--retries", "-r", default=4, help="Maximum number of retries")
    parser.add_argument("--timeout", "-t", default=4, help="Seconds to wait for retrying")
    parser.add_argument("--min-chunk-size", default=1024**2*2, help="Minimum chunk size to download")

    args = parser.parse_args()
    print "file-dl running on %r [ %s ]" % (sys.platform, sys.version_info)

    obj = MultiGet(urls=args.url, dest=args.directory, max_parallelism=int(args.parallelism),
                    timeout=int(args.timeout), max_retries=int(args.retries), minimum_chunk_size=int(args.min_chunk_size))
    if args.user and args.password :
        obj.add_basic_authentication(username=args.user, password=args.password)
    obj.start()

    return obj.get_dest()

if __name__ == "__main__" :
    main()
