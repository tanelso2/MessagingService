import message
import select
import socket


class MessagingServer:
    def __init__(self, host: str, port: int):
        self.connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockets_list = [self.connect_socket]
        self.connection_names = dict()

        self.connect_socket.bind((host, port))
        self.connect_socket.listen()

    def run(self):
        while True:
            read_sockets, _, _ = select.select(self.sockets_list, [], [])

            for sock in read_sockets:
                if sock == self.connect_socket:
                    (new_sock, _) = self.connect_socket.accept()
                    self.sockets_list.append(new_sock)
                    
                else:
                    try:
                        msg = message.read_message(sock)
                        if sock not in self.connection_names:
                            self.connection_names[sock] = msg
                            print("Added user {}".format(msg))
                            self.send_to_all(self.connect_socket, "User {} joined".format(msg))
                        else:
                            username = self.connection_names[sock]
                            msg = "{} said: {}".format(username, msg)
                            print(msg)
                            self.send_to_all(sock, msg)
                    except:
                        self.remove_socket(sock)
                        
    def send_to_all(self, orig_sock, msg: str):
        for s in self.sockets_list:
            if s != orig_sock and s != self.connect_socket:
                try: 
                    message.send_message(s, msg)
                except:
                    self.remove_socket(s)
                    
    def remove_socket(self, s):
        s.close()
        self.sockets_list.remove(s)
        if s in self.connection_names:
            print("Connection for user {} closed. Terminating".format(self.connection_names[s]))
            username = self.connection_names[s]
            del self.connection_names[s]
            self.send_to_all(s, "User {} left".format(username))

if __name__ == '__main__':
    server = MessagingServer("localhost", 8080)
    server.run()
