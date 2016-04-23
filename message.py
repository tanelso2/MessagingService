import pickle


def send_message(sock, msg: str):
    pickled_msg = pickle.dumps(msg)
    length = len(pickled_msg).to_bytes(8, byteorder='big')
    sock.send(length)
    sock.send(pickled_msg)


def read_message(sock) -> str:
    size = int.from_bytes(sock.recv(8), byteorder='big')
    pickled_data = sock.recv(size)
    m = pickle.loads(pickled_data)
    return m
