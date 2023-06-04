import socket
import threading
from datetime import datetime, timedelta

# サーバーの情報
SERVER_IP = 'localhost'  # サーバーのIPアドレス
SERVER_PORT = 5000       # サーバーのポート番号
TIMEOUT = 30             # メッセージのやり取りがない場合のタイムアウト時間（秒）

# ソケットと通信処理用のスレッド
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sockets = []
client_addresses = []

# 最新のメッセージのタイムスタンプ
last_message_time = datetime.now()

# 接続が確立したかどうかのフラグ
connected = False

# タイムアウト判定用のタイマースレッド
def timeout_thread():
    global connected
    while True:
        if connected and (datetime.now() - last_message_time) > timedelta(seconds=TIMEOUT):
            print("[System]: Connection timeout. Closing the application.")
            for client_socket in client_sockets:
                client_socket.close()
            sock.close()
            break

# クライアントからのメッセージ受信処理
def client_thread(client_socket, client_address):
    global connected, last_message_time
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
            last_message_time = datetime.now()
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
    global connected
    while True:
        sock.listen(5)
        client_socket, client_address = sock.accept()
        client_sockets.append(client_socket)
        client_addresses.append(client_address)
        threading.Thread(target=client_thread, args=(client_socket, client_address), daemon=True).start()
        print("[System]: Client connected: " + str(client_address))
        connected = True

# サーバーの起動
sock.bind((SERVER_IP, SERVER_PORT))
listen()


