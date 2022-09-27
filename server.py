import socket
import sys
from threading import Thread
from typing import List, Tuple

from frame.app import application


# "200 OK  [('Content-Type', 'text/html;')]"


class Server(object):
    def __init__(self, port=9090):
        self.port = port
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.sock.bind(("", port))
        self.sock.listen(1024)

    def start_response(self, code, headers: List[Tuple[str]]):
        pass

    def parse(self, req: str):
        pass
        return ""

    def deal(self, sock, ip_addr):
        temp_len = 4096
        recv_content = ""
        while True:
            recv_data = sock.recv(temp_len)
            print(recv_data.decode("utf-8"))
            recv_content += recv_data.decode("utf-8")
            if not recv_data:
                break

        env = dict()
        method, url, header = self.parse(recv_content)
        res = application(env, self.start_response)
        sock.send(res.encode("utf-8"))
        sock.close()

    def run(self):

        while True:
            new_sock, ip_addr = self.sock.accept()
            t = Thread(target=self.deal, args=(new_sock, ip_addr))
            t.setDaemon(True)
            t.start()
        self.sock.close()


if __name__ == '__main__':
    args = sys.argv
    port = int(args[1])
    server = Server(port=port)
    server.run(port)