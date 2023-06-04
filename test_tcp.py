import socket
import tkinter as tk
from tkinter import ttk
import threading
from datetime import datetime, timedelta

# サーバーの情報
SERVER_IP = '127.0.0.1'  # サーバーのIPアドレス
SERVER_PORT = 12345       # サーバーのポート番号
TIMEOUT = 30             # メッセージのやり取りがない場合のタイムアウト時間（秒）

# GUIの設定
window = tk.Tk()
window.title("TCP Chat")
window.geometry("500x400")
window.configure(bg='black')
window.option_add('*Scrollbar.Background', 'gray')

# 履歴表示用のテキストボックスとスクロールバー
text_box = tk.Text(window, bg='black', fg='white', insertbackground='white')
text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = ttk.Scrollbar(window, command=text_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_box.config(yscrollcommand=scrollbar.set)

# メッセージ入力欄
entry = tk.Entry(window, width=50)
entry.pack(side=tk.BOTTOM, pady=10)

# ソケットと通信処理用のスレッド
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 最新のメッセージのタイムスタンプ
last_message_time = datetime.now()

# メッセージ履歴のリスト
message_history = []

# 接続が確立したかどうかのフラグ
connected = False

# タイムアウト判定用のタイマースレッド
def timeout_thread():
    global connected
    while True:
        if connected and (datetime.now() - last_message_time) > timedelta(seconds=TIMEOUT):
            add_message("[System]: Connection timeout. Closing the application.")
            sock.close()
            window.quit()
            break

# メッセージの追加と履歴の制限
def add_message(message):
    global message_history
    message_history.append(message)
    if len(message_history) > 1000:
        message_history = message_history[-1000:]
    text_box.configure(state=tk.NORMAL)
    text_box.insert(tk.END, message + "\n")
    text_box.configure(state=tk.DISABLED)
    text_box.yview(tk.END)

# サーバーからのメッセージ受信処理
def receive_thread():
    global connected, last_message_time
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                add_message("[System]: Connection closed by the server.")
                connected = False
                sock.close()
                window.quit()
                break
            message = data.decode("shift-jis")
            add_message("[Server]: " + message)
            last_message_time = datetime.now()
        except Exception as e:
            add_message("[System]: An error occurred while receiving the message: " + str(e))
            connected = False
            sock.close()
            window.quit()
            break

# メッセージ送信処理
def send_message():
    global connected, last_message_time
    if not connected:
        add_message("[System]: Not connected to the server.")
        return
    message = entry.get()
    if message.strip().lower() == "quit":
        add_message("[Client]: Quit command received. Closing the application.")
        sock.sendall(message.encode("shift-jis"))
        sock.close()
        window.quit()
        return
    try:
        sock.sendall(message.encode("shift-jis"))
        add_message("[Client]: " + message)
        entry.delete(0, tk.END)
        last_message_time = datetime.now()
    except Exception as e:
        add_message("[System]: An error occurred while sending the message: " + str(e))
        connected = False
        sock.close()
        window.quit()

# 接続処理
def connect():
    global connected
    try:
        sock.connect((SERVER_IP, SERVER_PORT))
        connected = True
        add_message("[System]: Connected to the server.")
        threading.Thread(target=receive_thread, daemon=True).start()
        threading.Thread(target=timeout_thread, daemon=True).start()
    except Exception as e:
        add_message("[System]: An error occurred while connecting to the server: " + str(e))

# クライアントの起動
connect()

# GUIのメインループ
window.protocol("WM_DELETE_WINDOW", lambda: window.quit())  # ウィンドウの×ボタンを押した際にアプリを終了
window.mainloop()
