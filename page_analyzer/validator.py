from urllib.parse import urlparse
from validators import url

def normalization(url):
    urls = urlparse(url)
    norm_url = f'{urls.scheme}://{urls.netloc}'
    return norm_url

