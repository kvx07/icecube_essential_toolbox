import tkinter as tk
from tkinter import messagebox
import requests
import os
import sys

def verify_two_elements(name, id_card):
    url = f"http://auth.no1yx.com/api//index/?regtype=acc&uname=X9uYua9&password=Ww123456489&source=bt&type=xy.user.reg&session=0.01738807259391084&time=1714880420&realname={name}&idcard={id_card}&smccode=&mailcode=&device=1&gid=&channelid=&origin=&ip=&xy_channel_type=pt&xy_channelid=bt&xy_source_id=bt&xy_extra=&nickname=&userface=&xy_vip_qq=&xy_vip_weixin=&xy_vip_phone=&xy_package_id=&xy_system=%25E5%25AE%2589%25E5%258D%2593&imei=&xy_version=&xy_device_factory=&xy_clipboard=&xy_screen=&xy_language=&xy_uuid=&sign=d2c9518205c0d88f84101d244a63ec61&callback=jQuery34105324458169647628_1714880387760&_=1714880387766"
    try:
        response = requests.get(url)
        response.raise_for_status()
        if 'code":20' in response.text:
            return "二要素校验失败"
        elif "15" in response.text:
            return "二要素校验成功"
        else:
            return "响应不包含预期关键词。"
    except requests.RequestException as e:
        return f"请求失败：{e}"

def verify_three_elements(name, id_card, phone_number):
    url = "https://hebcaonline.hebca.com/Hebca/interface/verifyPhoneNum.action"
    headers = {
        "Host": "hebcaonline.hebca.com",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.48(0x18003030) NetType/WIFI Language/zh_CN",
        "Referer": "https://servicewechat.com/wx82e82080bf57acaa/116/page-frame.html",
    }
    data = {
        "verifyType": "106",
        "personName": name,
        "personIdcard": id_card,
        "personMobile": phone_number,
        "allCode": "20240430"
    }
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"请求失败：{e}"

def start_two_element_verification():
    name = entry_name.get()
    id_card = entry_id_card.get()
    if not name or not id_card:
        messagebox.showerror("错误", "姓名和身份证号不能为空。")
        return
    result = verify_two_elements(name, id_card)
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, result)
    text_area.config(state=tk.DISABLED)

def start_three_element_verification():
    name = entry_name.get()
    id_card = entry_id_card.get()
    phone_number = entry_phone.get()
    if not name or not id_card or not phone_number:
        messagebox.showerror("错误", "姓名、身份证号和手机号不能为空。")
        return
    result = verify_three_elements(name, id_card, phone_number)
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, result)
    text_area.config(state=tk.DISABLED)

def go_back():
    x_position = root.winfo_x()
    y_position = root.winfo_y()
    root.destroy()
    os.system(f'python main.py {x_position} {y_position}')

x_position = int(sys.argv[1]) if len(sys.argv) > 1 else 200
y_position = int(sys.argv[2]) if len(sys.argv) > 2 else 200

root = tk.Tk()
root.title("要素核验")
root.geometry(f"1200x800+{x_position}+{y_position}")  # 窗口大小和位置
root.iconbitmap('icon.ico')

label_name = tk.Label(root, text="姓名:", font=("宋体", 12))
label_name.pack()
entry_name = tk.Entry(root)
entry_name.pack()

label_id_card = tk.Label(root, text="身份证号:", font=("宋体", 12))
label_id_card.pack()
entry_id_card = tk.Entry(root)
entry_id_card.pack()

label_phone = tk.Label(root, text="手机号(仅三要素核验时需要):", font=("宋体", 12))
label_phone.pack()
entry_phone = tk.Entry(root)
entry_phone.pack()

button_two_element = tk.Button(root, text="二要素核验", command=start_two_element_verification, font=("宋体", 12))
button_two_element.pack(pady=10)

button_three_element = tk.Button(root, text="三要素核验", command=start_three_element_verification, font=("宋体", 12))
button_three_element.pack(pady=10)

button_back = tk.Button(root, text="返回主页", command=go_back, font=("宋体", 12))
button_back.pack(pady=10)

text_area = tk.Text(root, width=150, height=40, state=tk.DISABLED, font=("宋体", 10))
text_area.pack(pady=10)

root.mainloop()
