import tkinter as tk
from tkinter import messagebox
import requests
import os
import sys

def query_ip(ip_address):
    api_url = "https://api.oioweb.cn/api/ip/ipaddress"
    params = {"ip": ip_address}
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as errh:
        return {"error": f"Http Error: {errh}"}
    except requests.exceptions.ConnectionError as errc:
        return {"error": f"Error Connecting: {errc}"}
    except requests.exceptions.Timeout as errt:
        return {"error": f"Timeout Error: {errt}"}
    except requests.exceptions.RequestException as err:
        return {"error": f"OOps: Something Else: {err}"}

def start_ip_lookup():
    ip_address = entry_ip.get()
    result = query_ip(ip_address)
    if 'error' in result:
        result_str = result['error']
    else:
        result_str = f"IP地址: {ip_address}\n位置: {result.get('data', {}).get('location', '未知')}\nISP: {result.get('data', {}).get('isp', '未知')}"
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
root.title("IP查询")
root.geometry(f"1200x800+{x_position}+{y_position}")  # 窗口大小和位置
root.iconbitmap('icon.ico')

label_ip = tk.Label(root, text="请输入IP地址:", font=("宋体", 12))
label_ip.pack()
entry_ip = tk.Entry(root)
entry_ip.pack()

button_lookup = tk.Button(root, text="查询", command=start_ip_lookup, font=("宋体", 12))
button_lookup.pack(pady=10)

button_back = tk.Button(root, text="返回主页", command=go_back, font=("宋体", 12))
button_back.pack(pady=10)

text_area = tk.Text(root, width=150, height=40, state=tk.DISABLED, font=("宋体", 10))
text_area.pack(pady=10)

root.mainloop()
