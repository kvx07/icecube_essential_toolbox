import tkinter as tk
import os
import sys
import subprocess
def open_selected_function():
    selected_function = function_var.get()
    x_position = root.winfo_x()
    y_position = root.winfo_y()
    root.destroy()
    if selected_function == "手机号生成和空号检测":
        subprocess.run([sys.executable, '手机号跑现.py', str(x_position), str(y_position)])
    elif selected_function == "QQ查询":
        subprocess.run([sys.executable, 'qq查询.py', str(x_position), str(y_position)])
    elif selected_function == "IP查询":
        subprocess.run([sys.executable, 'ip查询.py', str(x_position), str(y_position)])
    elif selected_function == "要素核验":
        subprocess.run([sys.executable, '要素核验.py', str(x_position), str(y_position)])

# 创建主窗口
root = tk.Tk()
root.title("冰块sg工具箱")
root.geometry("400x300+200+200")  # 窗口大小和位置

# 根据是否打包设置图标路径
if getattr(sys, 'frozen', False):
    # 如果被打包，使用临时路径
    icon_path = os.path.join(sys._MEIPASS, "icon.ico")
else:
    # 如果未打包，使用当前目录路径
    icon_path = os.path.abspath("icon.ico")

root.iconbitmap(icon_path)

# 创建标题标签
label_title = tk.Label(root, text="冰块sg工具箱", font=("宋体", 16))
label_title.pack(pady=20)

# 创建功能选择下拉列表
function_var = tk.StringVar(root)
function_var.set("选择功能")
function_menu = tk.OptionMenu(root, function_var, "手机号生成和空号检测", "QQ查询", "IP查询", "要素核验")
function_menu.config(font=("宋体", 12))
function_menu.pack(pady=20)

# 创建确认按钮
button_confirm = tk.Button(root, text="确认", command=open_selected_function, font=("宋体", 12))
button_confirm.pack(pady=20)

# 创建页脚标签
label_footer = tk.Label(root, text="by c0t1n3nt5l", font=("宋体", 10))
label_footer.pack(side="bottom", pady=10)

# 运行主循环
root.mainloop()
