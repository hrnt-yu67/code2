import tkinter as tk
import socket
import threading
import datetime

def start_server():
    # サーバーのIPアドレスとポート番号    
    HOST = ip_entry.get()
    PORT = port_entry.get()
 
    if len(HOST)==0  or  len(PORT)==0:
        HOST = '127.0.0.1'
        PORT = 12345
            
    # サーバーのソケットを作成
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    status_label.configure(text="サーバーが起動しました。クライアントの接続を待機中...")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
    received_text.configure(state='normal')
    received_text.insert('end', f"{timestamp}: 受信を開始します：\n")
    received_text.configure(state='disabled')

    client_socket, addr = server_socket.accept()
    status_label.configure(text=f"クライアントが接続しました。アドレス: {addr}")

    while True:
        message = client_socket.recv(1024).decode()

        if not message:
            break

        receive_message(message)

        response = "OK"
        client_socket.sendall(response.encode())
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        received_text.configure(state='normal')
        received_text.insert('end', f"{timestamp}: {response}\n")
        received_text.configure(state='disabled')


    client_socket.close()
    server_socket.close()

def receive_message(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    received_text.configure(state='normal')
    received_text.insert('end', f"{timestamp}: {message}\n")
    received_text.configure(state='disabled')

def start_server_thread():
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

def close_connection():
    window.destroy()

window = tk.Tk()
window.title("メッセージ受信アプリ")

status_label = tk.Label(window, text="サーバーが起動していません")
status_label.pack()

ip_label = tk.Label(window, text="IPアドレス:")
ip_entry = tk.Entry(window)
ip_label.pack()
ip_entry.pack()
port_label = tk.Label(window, text="ポート番号:")
port_entry = tk.Entry(window)
port_label.pack()
port_entry.pack()

received_label = tk.Label(window, text="受信したメッセージ:")
received_label.pack()

received_text = tk.Text(window, state='disabled')
received_text.pack()

start_button = tk.Button(window, text="受信開始", command=start_server_thread)
start_button.pack()

close_button = tk.Button(window, text="閉じる", command=close_connection)
close_button.pack()

window.mainloop()
