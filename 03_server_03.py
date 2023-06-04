import tkinter as tk
import socket
import threading
import datetime

# クライアントアプリのIPアドレスとポート番号
CLIENT_HOST = '127.0.0.1'
CLIENT_PORT = 12345

def start_receiving():
    # クライアントとの接続
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    client_socket.connect((ip_entry.get(), int(port_entry.get())))
    client_socket.connect((CLIENT_HOST, CLIENT_PORT))

    # 受信ループ
    while True:
        message = client_socket.recv(1024).decode()
        
        # 受信時間とメッセージを表示
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        received_text.configure(state='normal')
        received_text.insert('end', f"{timestamp}: {message}\n")
        received_text.configure(state='disabled')

        # 応答として"OK"を送信
        response = "OK"
        client_socket.sendall(response.encode())

    client_socket.close()

def start_receiving_thread():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    received_text.insert('end', f"{timestamp}: 受信を開始します：{ip_entry.get()}\n")
    receive_thread = threading.Thread(target=start_receiving)
    receive_thread.start()

def close_connection():
    window.destroy()

window = tk.Tk()
window.title("メッセージ受信アプリ")

title_label = tk.Label(window, text="メッセージ受信アプリ")
ip_label = tk.Label(window, text="IPアドレス:")
ip_entry = tk.Entry(window)
port_label = tk.Label(window, text="ポート番号:")
port_entry = tk.Entry(window)

# 構成
title_label.pack()
ip_label.pack()
ip_entry.pack()
port_label.pack()
port_entry.pack()

start_button = tk.Button(window, text="受信開始", command=start_receiving_thread)
start_button.pack()

received_label = tk.Label(window, text="受信したメッセージ:")
received_label.pack()

received_text = tk.Text(window, state='disabled')
received_text.pack()

close_button = tk.Button(window, text="閉じる", command=close_connection)
close_button.pack()

window.mainloop()
