import pathlib
import socket
import urllib.parse

import joblib


def get(url: str, headers: str) -> bytearray:
    port = 80
    parsed = urllib.parse.urlparse(url)
    filename = f'{parsed.path}?{parsed.query}'
    host = parsed.netloc
    headers = pathlib.Path(headers).read_text()
    cmd = bytes(f'GET {filename} HTTP/1.0\r\nHost: {host}\r\n{headers}\r\n\r\n', encoding='utf-8')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall(cmd)
    res = bytearray()
    while data := sock.recv(10000):
        res.extend(data)
    sock.close()
    return res


def main():
    urls = ['http://www.bcliquorstores.com/ajax/browse?category=beer&sort=name.raw:asc&size=24&page=1',
            'http://www.bcliquorstores.com/ajax/browse?category=beer&sort=name.raw:asc&size=24&page=2',
            'http://www.bcliquorstores.com/ajax/browse?category=beer&sort=name.raw:asc&size=24&page=3',
            'http://www.bcliquorstores.com/ajax/browse?category=beer&sort=name.raw:asc&size=24&page=4',
            'http://www.bcliquorstores.com/ajax/browse?category=beer&sort=name.raw:asc&size=24&page=5',
            'http://www.bcliquorstores.com/ajax/browse?category=beer&sort=name.raw:asc&size=24&page=6']
    headers = 'headers.txt'
    res = joblib.Parallel(n_jobs=-1, prefer='threads')(joblib.delayed(get)(url, headers) for url in urls)
    print(res)


if __name__ == '__main__':
    main()
