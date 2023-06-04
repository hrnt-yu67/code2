import tkinter as tk
import socket
import threading
from datetime import datetime, timedelta


# サーバーの情報
SERVER_IP = 'localhost'  # サーバーのIPアドレス
SERVER_PORT = 5000       # サーバーのポート番号

# Tkinterのウィンドウを作成
window = tk.Tk()
window.title("Server GUI")
window.geometry("400x300")

# メッセージ表示用のテキストボックス
message_textbox = tk.Text(window)
message_textbox.pack(fill=tk.BOTH, expand=True)

# ソケットと通信処理用のスレッド
sock = None
client_sockets = []
client_addresses = []

# クライアントからのメッセージ受信処理
def client_thread(client_socket, client_address):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("[System]: Connection closed by the client: " + str(client_address))
                client_socket.close()
                client_sockets.remove(client_socket)
                client_addresses.remove(client_address)
                break
            message = data.decode("shift-jis")
            print("[Client " + str(client_address) + "]: " + message)
            message_textbox.insert(tk.END, "[Client " + str(client_address) + "]: " + message + "\n")
            message_textbox.see(tk.END)
            for socket in client_sockets:
                if socket != client_socket:
                    socket.sendall(data)
        except Exception as e:
            print("[System]: An error occurred while receiving the message from client " + str(client_address) + ": " + str(e))
            client_socket.close()
            client_sockets.remove(client_socket)
            client_addresses.remove(client_address)
            break

# 接続待機処理
def listen():
    while True:
        sock.listen(5)
        client_socket, client_address = sock.accept()
        client_sockets.append(client_socket)
        client_addresses.append(client_address)
        threading.Thread(target=client_thread, args=(client_socket, client_address), daemon=True).start()
        print("[System]: Client connected: " + str(client_address))

# サーバーの起動
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((SERVER_IP, SERVER_PORT))
listen()

window.deiconify()

# GUIのメインループ
window.mainloop()
