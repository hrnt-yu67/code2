import tkinter as tk
import socket

HOST = '127.0.0.1'
PORT = 12345

def send_message():
    message = message_entry.get()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    client_socket.sendall(message.encode())

    response = client_socket.recv(1024).decode()

    response_text.configure(state='normal')
    response_text.delete('1.0', 'end')
    response_text.insert('1.0', response)
    response_text.configure(state='disabled')

def close_connection():
    client_socket.close()
    window.destroy()


window = tk.Tk()
window.title("クライアントアプリ")

message_label = tk.Label(window, text="メッセージ:")
message_label.pack()

message_entry = tk.Entry(window)
message_entry.pack()

send_button = tk.Button(window, text="送信", command=send_message)
send_button.pack()

response_label = tk.Label(window, text="サーバーからの応答:")
response_label.pack()

response_text = tk.Text(window, state='disabled')
response_text.pack()

close_button = tk.Button(window, text="接続を閉じる", command=close_connection)
close_button.pack()

window.mainloop()
