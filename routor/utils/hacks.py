import contextlib
import logging
from functools import partial
from unittest import mock

import requests
from tqdm import tqdm

logger = logging.getLogger()


def download_with_progressbar(method, *args, **kwargs):
    # add stream argument, so we can iterate over the response.
    response = method(*args, **kwargs, stream=True)

    # get the total size
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024

    # display download progress
    progressbar = tqdm(total=total_size, unit='iB', unit_scale=True)
    data = b''
    for chunk in response.iter_content(block_size):
        data += chunk
        progressbar.update(len(chunk))
    progressbar.close()

    response._content = data
    return response


@contextlib.contextmanager
def progressbar_for_requests(method_name):
    method = getattr(requests, method_name)
    new_method = partial(download_with_progressbar, method)
    with mock.patch.object(requests, method_name) as mocked_request:
        mocked_request.side_effect = new_method
        yield
