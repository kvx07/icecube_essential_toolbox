import tkinter as tk
from tkinter import messagebox
import requests
import os
import sys

def query_qq(qq_number):
    url = f"https://zy.xywlapi.cc/qqapi?qq={qq_number}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        return {"error": str(e)}

def query_phone(phone_number):
    url = f"https://zy.xywlapi.cc/qqphone?phone={phone_number}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        return {"error": str(e)}

def start_qq_lookup():
    qq_number = entry_qq.get()
    if not qq_number.isdigit():
        messagebox.showerror("错误", "QQ号码必须是数字。")
        return
    result = query_qq(qq_number)
    if 'error' in result:
        result_str = result['error']
    else:
        phone = result.get('phone', '未知')
        phonediqu = result.get('phonediqu', '未知')
        result_str = f"QQ号码: {qq_number}\n手机号: {phone}\n归属地: {phonediqu}"
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, result_str)
    text_area.config(state=tk.DISABLED)

def start_phone_lookup():
    phone_number = entry_phone.get()
    if not phone_number.isdigit():
        messagebox.showerror("错误", "手机号必须是数字。")
        return
    result = query_phone(phone_number)
    if 'error' in result:
        result_str = result['error']
    else:
        qq = result.get('qq', '未知')
        result_str = f"手机号: {phone_number}\nQQ号码: {qq}"
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, result_str)
    text_area.config(state=tk.DISABLED)

def go_back():
    x_position = root.winfo_x()
    y_position = root.winfo_y()
    root.destroy()
    os.system(f'python main.py {x_position} {y_position}')

x_position = int(sys.argv[1]) if len(sys.argv) > 1 else 200
y_position = int(sys.argv[2]) if len(sys.argv) > 2 else 200

root = tk.Tk()
root.title("QQ查询")
root.geometry(f"1200x800+{x_position}+{y_position}")  # 窗口大小和位置
root.iconbitmap('icon.ico')

label_qq = tk.Label(root, text="请输入QQ号码:", font=("宋体", 12))
label_qq.pack()
entry_qq = tk.Entry(root)
entry_qq.pack()

button_qq_to_phone = tk.Button(root, text="QQ号查手机号", command=start_qq_lookup, font=("宋体", 12))
button_qq_to_phone.pack(pady=10)

label_phone = tk.Label(root, text="请输入手机号:", font=("宋体", 12))
label_phone.pack()
entry_phone = tk.Entry(root)
entry_phone.pack()

button_phone_to_qq = tk.Button(root, text="手机号查QQ号", command=start_phone_lookup, font=("宋体", 12))
button_phone_to_qq.pack(pady=10)

button_back = tk.Button(root, text="返回主页", command=go_back, font=("宋体", 12))
button_back.pack(pady=10)

text_area = tk.Text(root, width=150, height=40, state=tk.DISABLED, font=("宋体", 10))
text_area.pack(pady=10)

root.mainloop()
