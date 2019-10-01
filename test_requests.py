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


def hash_md5(filename, chunk_size=2 ** 16):
    """
    Computes the *Message Digest 5 (MD5)* hash of given file.

    Parameters
    ----------
    filename : unicode
        File to compute the *MD5* hash of.
    chunk_size : int, optional
        Chunk size to read from the file.

    Returns
    -------
    unicode
        *MD5* hash of given file.
    """

    md5 = hashlib.md5()

    with open(filename, 'rb') as file_object:
        while True:
            chunk = file_object.read(chunk_size)
            if not chunk:
                break

            md5.update(chunk)

    return md5.hexdigest()


class TqdmUpTo(tqdm):
    """
    :class:`tqdm` sub-class used to report the progress of an action.
    """

    def update_to(self, chunks_count=1, chunk_size=1, total_size=None):
        """
        Reports the progress of an action.

        Parameters
        ----------
        chunks_count : int, optional
            Number of blocks transferred.
        chunk_size : int, optional
            Size of each block (in tqdm units).
        total_size : int, optional
            Total size (in tqdm units).
        """

        if total_size is not None:
            self.total = total_size

        self.update(chunks_count * chunk_size - self.n)


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
