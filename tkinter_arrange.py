import socket
import tkinter as tk
from tkinter import ttk
import threading
from datetime import datetime, timedelta


def send_message():
    message = textbox.get("1.0", "end-1c")
    selected_option = option.get()
#    result_text.delete("1.0", "end")
#    result_text.insert("1.0", f"\nメッセージ: {message}\n選択したオプション: {selected_option}")
    dt_now = datetime.datetime.now()
    result_text.insert("1.0", f"\n {dt_now}: {message}")


def set_textA(): 
    textbox.delete("1.0", "end")
    textbox.insert("1.0", f"GET,SDIV,3")

def set_textB():
    textbox.delete("1.0", "end")
    textbox.insert("1.0", f"Torq,Start,3")

def set_textC():
    textbox.delete("1.0", "end")
    textbox.insert("1.0", f"WEGHING,START,3")


# ウィンドウの作成
window = tk.Tk()
window.title("GUIプログラム")

# タイトルのラベル
title_label = tk.Label(window, text="タイトル")
title_label.pack()

# テキストボックス
textbox = tk.Text(window, width=60, height=3)
textbox.pack()

# 送信ボタン
send_button = tk.Button(window, text="送信", command=send_message)
send_button.pack()

# ラジオボタン
option = tk.StringVar()
#option.set("A送信")
radio_button1 = tk.Radiobutton(window, text="A送信", variable=option, value="A送信", command=set_textA)
radio_button1.pack()

radio_button2 = tk.Radiobutton(window, text="B送信", variable=option, value="B送信",command=set_textB)
radio_button2.pack()

radio_button3 = tk.Radiobutton(window, text="c送信", variable=option, value="c送信",command=set_textC)
radio_button3.pack()


# 結果表示用のテキストボックス
result_text = tk.Text(window,width=60, height=20)

result_text.pack()

# ウィンドウの表示
window.mainloop()
