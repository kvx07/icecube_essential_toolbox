import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import requests
import threading
from queue import Queue
import os
import sys

def generate_custom_mobile_numbers(prefix, suffix):
    if not prefix.isdigit() or not suffix.isdigit():
        raise ValueError("前缀和后缀必须是数字。")
    middle_length = 11 - len(prefix) - len(suffix)
    if middle_length <= 0:
        raise ValueError("前缀和后缀的总长度必须小于11位。")
    count = 10 ** middle_length
    mobile_numbers = set()  # 使用集合确保生成的号码唯一
    while len(mobile_numbers) < count:
        middle_digits = ''.join(str(random.randint(0, 9)) for _ in range(middle_length))
        mobile_number = prefix + middle_digits + suffix
        mobile_numbers.add(mobile_number)
    return list(mobile_numbers)

def check_mobile_number(mobile_number):
    api_url = f'https://ps.szqxt.com/qxt600?mobile={mobile_number}'
    try:
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error: {response.status_code} - {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def worker(queue, results, progress, total_numbers):
    while True:
        number = queue.get()
        if number is None:
            break
        result = check_mobile_number(number)
        if 'error' not in result:
            results.append(number)
        progress['checked'] += 1
        update_progress(progress['checked'], total_numbers)
        queue.task_done()

def update_progress(checked, total):
    remaining = total - checked
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, f"已检测 {checked} 个, 剩余 {remaining} 个\n")
    text_area.config(state=tk.DISABLED)
    root.update_idletasks()

def generate_and_check_numbers():
    prefix = entry_prefix.get()
    suffix = entry_suffix.get()
    try:
        text_area.config(state=tk.NORMAL)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, "生成中...\n")
        text_area.config(state=tk.DISABLED)
        root.update_idletasks()
        mobile_numbers = generate_custom_mobile_numbers(prefix, suffix)
        queue = Queue()
        results = []
        progress = {'checked': 0}
        total_numbers = len(mobile_numbers)
        num_threads = 10
        threads = []
        for _ in range(num_threads):
            t = threading.Thread(target=worker, args=(queue, results, progress, total_numbers))
            t.start()
            threads.append(t)
        for number in mobile_numbers:
            queue.put(number)
        queue.join()
        for _ in range(num_threads):
            queue.put(None)
        for t in threads:
            t.join()
        results_str = "非空号：\n" + "\n".join(results)
        text_area.config(state=tk.NORMAL)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, results_str)
        text_area.config(state=tk.DISABLED)
    except ValueError as e:
        messagebox.showerror("错误", str(e))

def start_thread():
    threading.Thread(target=generate_and_check_numbers).start()

def go_back():
    x_position = root.winfo_x()
    y_position = root.winfo_y()
    root.destroy()
    os.system(f'python main.py {x_position} {y_position}')

x_position = int(sys.argv[1]) if len(sys.argv) > 1 else 200
y_position = int(sys.argv[2]) if len(sys.argv) > 2 else 200

root = tk.Tk()
root.title("手机号生成和空号检测")
root.geometry(f"1200x800+{x_position}+{y_position}")  # 窗口大小和位置
root.iconbitmap('icon.ico')

label_prefix = tk.Label(root, text="请输入自定义的前缀数字:", font=("宋体", 12))
label_prefix.pack()
entry_prefix = tk.Entry(root)
entry_prefix.pack()

label_suffix = tk.Label(root, text="请输入自定义的后缀数字:", font=("宋体", 12))
label_suffix.pack()
entry_suffix = tk.Entry(root)
entry_suffix.pack()

button_generate = tk.Button(root, text="生成并检测手机号", command=start_thread, font=("宋体", 12))
button_generate.pack(pady=10)

button_back = tk.Button(root, text="返回主页", command=go_back, font=("宋体", 12))
button_back.pack(pady=10)

text_area = scrolledtext.ScrolledText(root, width=150, height=40, state=tk.DISABLED, font=("宋体", 10))
text_area.pack(pady=10)

root.mainloop()
