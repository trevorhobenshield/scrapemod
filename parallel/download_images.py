import hashlib
import logging

import joblib
import requests

from utils import set_logger


def get(url: str, headers: dict, session: requests.Session) -> any:
    try:
        dat = session.get(url=url, headers=headers).content
        unique_filename = hashlib.md5(url.encode("utf-8")).hexdigest()
        with open(f'{unique_filename}.png', 'wb') as fw:
            fw.write(dat)
    except Exception as e:
        logging.debug(f'Exception: {e} {url}')


def main():
    set_logger('downloaded_images.log')
    urls = ['https://c8.alamy.com/comp/WWH9YM/siberia-husky-sled-dog-dogphoto-dog-photo-dog-photos-WWH9YM.jpg',
            'https://thumbs.dreamstime.com/b/french-bulldog-small-breed-domestic-dog-were-result-s-cross-ancestors-imported-england-local-136021670.jpg',
            'https://images.all-free-download.com/images/graphiclarge/cute_dog_photo_picture_7_168843.jpg']
    session = requests.Session()
    joblib.Parallel(n_jobs=-1, prefer='threads')(joblib.delayed(get)(url, {}, session) for url in urls)


if __name__ == '__main__':
    main()
