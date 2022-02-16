import json
import pathlib
import socket
import urllib.parse


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
    url = 'http://www.bcliquorstores.com/ajax/browse?category=beer&sort=name.raw:asc&size=24&page=1'

    headers = 'headers.txt'
    res: bytearray = get(url, headers)

    # write to disk
    pathlib.Path('res.txt').write_bytes(res)

    # read from disk
    data = json.loads(pathlib.Path('res.txt').read_text().splitlines()[-1])
    print(data)


if __name__ == '__main__':
    main()
