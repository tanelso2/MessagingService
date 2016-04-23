import message
import select
import socket
import threading
import tkinter as tk


class MessagingGUI:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.master = tk.Tk()
        self.master.title("TN Messenger")
        self.text = tk.Text(self.master)
        self.frame = tk.Frame(self.master)
        self.entry = tk.Entry(self.frame, width=100, state=tk.DISABLED)
        self.button = tk.Button(self.frame, text="Send", state=tk.DISABLED)
        self.top = tk.Toplevel()
        self.top.title("Select a name")
        self.top_entry = tk.Entry(self.top)

        self.top_button = tk.Button(self.top, text="Select", command=self.select_name)
        self.top_entry.pack(side=tk.LEFT)
        self.top_entry.focus_set()
        self.top_button.pack(side=tk.LEFT)

        self.text.pack()
        self.frame.pack()
        self.button.pack(side=tk.RIGHT)
        self.entry.pack(side=tk.RIGHT)

        self.listen_thread = threading.Thread(target=self.thread_fun)
        self.listen_thread.daemon = True
        self.listen_thread.start()

        self.top.focus_set()

    def start(self):
        self.master.mainloop()

    def thread_fun(self):
        while True:
            read_sockets, _, _ = select.select([self.sock], [], [])
            for s in read_sockets:
                msg = message.read_message(s)
                self.text.insert(tk.END, msg)
                self.text.insert(tk.END, '\n')

    def send_msg(self):
        msg = self.entry.get()
        message.send_message(self.sock, msg)
        self.entry.delete(0, tk.END)

    def return_callback(self, event):
        self.send_msg()

    def select_name(self):
        name = self.top_entry.get()
        message.send_message(self.sock, name)
        self.entry.config(state=tk.NORMAL)
        self.button.config(state=tk.NORMAL, command=self.send_msg)
        self.entry.focus_set()
        self.master.title("TN Messenger: User {}".format(name))
        self.master.bind('<Return>', self.return_callback)
        self.top.destroy()

if __name__ == '__main__':
    c = MessagingGUI("localhost", 8080)
    c.start()
