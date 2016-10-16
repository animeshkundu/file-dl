file-dl
=======

File Download Accelerator. Supports both HTTP and FTP downloads.

CLI tool for any *nix* system. Inspired by IDM on Windows.

PyPi package [file-dl](https://pypi.python.org/pypi/file-dl)


Installation
------------
pip install file-dl


Usage
-----

file-dl [-h] [--directory DIRECTORY] [--user USER]
               [--password PASSWORD] [--parallelism PARALLELISM]
               [--retries RETRIES] [--timeout TIMEOUT]
               [--min-chunk-size MIN_CHUNK_SIZE]
               url


positional arguments:

  url                   The link to downlaod


optional arguments:

  -h, --help            show this help message and exit

  --directory DIRECTORY, -d DIRECTORY  Directory where the file will be downloaded

  --user USER           Authentication - Username

  --password PASSWORD   Authentication - Password

  --parallelism PARALLELISM, -p PARALLELISM  Number of parallel downloads

  --retries RETRIES, -r RETRIES  Maximum number of retries

  --timeout TIMEOUT, -t TIMEOUT  Seconds to wait for retrying

  --min-chunk-size MIN_CHUNK_SIZE Minimum chunk size to download


