from __future__ import division, unicode_literals

import functools
import gzip
import hashlib
import json
import os
import random
import setuptools.archive_util
import shutil
import sys
from six.moves import urllib
from tqdm import tqdm


def url_download(url, filename, md5=None, retries=3):
    """
    Downloads given url and saves its content at given file.

    Parameters
    ----------
    url : unicode
        Url to download.
    filename : unicode
        File to save the url content at.
    md5 : unicode, optional
        *Message Digest 5 (MD5)* hash of the content at given url. If provided
        the saved content at given file will be hashed and compared to ``md5``.
    retries : int, optional
        Number of retries in case where a networking error occurs or the *MD5*
        hash is not matching.

    Examples
    --------
    >>> import os
    >>> url_download(
    ...     'https://github.com/colour-science/colour-datasets', os.devnull)
    """

    attempt = 0
    while attempt != retries:
        try:
            with TqdmUpTo(
                    unit='B',
                    unit_scale=True,
                    miniters=1,
                    desc='Downloading "{0}" file'.format(
                        url.split('/')[-1])) as progress:
                urllib.request.urlretrieve(
                    url,
                    filename=filename,
                    reporthook=progress.update_to,
                    data=None)

            if md5 is not None:
                if md5.lower() != hash_md5(filename):
                    raise ValueError(
                        '"MD5" hash of "{0}" file '
                        'does not match the expected hash!'.format(filename))

            attempt = retries
        except (urllib.error.URLError, IOError, ValueError) as error:
            attempt += 1
            print('An error occurred while downloading "{0}" file '
                  'during attempt {1}, retrying...'.format(filename, attempt))
            if attempt == retries:
                raise error


i = 0
while True:
    i += 1
    print('Attempt {0}'.format(i))
    url_download('https://github.com/colour-science/colour-datasets', os.devnull)
