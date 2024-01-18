import tkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
import requests
import json
import pymysql
from tkinter import messagebox
API_KEY = "DZrqnb4HOnh3Nhiffy4N0Hk9"#百度api调用
SECRET_KEY = "xPfWDaiwvl5qTidDjbBmYcmXwvdtfRNo"#百度api调用
content_list = []
pd="zhangze030131"
text_entry = None
combox_box2 = None
combo_var2 = None
text_zujian = {}
response_dict={}
def print_value():
    conn = pymysql.connect(host="localhost", port=3306, user="root", password=pd, db='eat', charset='utf8')
    cur = conn.cursor()
    try:
        content_list.clear()  # 清空content_list，确保每次函数执行时是空列表
        sql = "select Canteenname from canteen where Locationname=" + "\"" + combo_var2.get() + "\"" + ";"
        cur.execute(sql)
        for i in range(2, 7):#获取文本框内的数据
            content = text_zujian['text_var' + str(i)].get()
            content_list.append(content)
        selected_value = combox_box2.get()
        if len(content_list) == 5:  # 确保content_list有3个元素，防止索引越界
            sql2 = "INSERT INTO canteenrestaurant (canteenname, floorname, restaurantname)" \
                   "value('" + selected_value + "','" + content_list[0] + "层','" + content_list[1] + "');"
            sql3 = "INSERT INTO restaurantdish (restaurantname, dishname)" \
                   "value('" + content_list[1] + "','" + content_list[2] + "');"
            sql4 = "INSERT INTO dishinformation (restaurantname, dishname,price,taste)" \
                   "value('" + content_list[1] + "','" + content_list[2] + "','" + content_list[3] + "','" + content_list[4] + "');"
            cur.execute(sql2)
            cur.execute(sql3)
            cur.execute(sql4)
            conn.commit()
            messagebox.showinfo("消息", "添加成功")
        else:
            messagebox.showinfo("ERROR", "content_list 中元素不足，无法执行插入操作")
    except Exception as e:
        if e.args[0]==1452:
            messagebox.showinfo("消息", "请输入元素")
        else:
            messagebox.showinfo("ERROR", f"发生异常: {e}")
    finally:
        conn.close()
def find_value():#什么都没有选中时,打印所有的信息,选中location时,打印location下的信息,选中餐厅时,打印餐厅的信息,选中店铺时,打印店铺的信息
    conn = pymysql.connect(host="localhost", port=3306, user="root", password=pd, db='eat',
                           charset='utf8')  # 连接本地数据库
    cur = conn.cursor()  # 生成游标对象r
    content_list = []
    print(f"combo_value: {combo_var2.get()}")  # 打印combo_value的值，检查是否正确
    try:
        for i in range(2, 5):  # 获取Entry对象中的文本
            content = text_zujian['text_var' + str(i)].get()
            content_list.append(content)
        if combo_var2.get().strip() == '':
            sql4="SELECT canteenrestaurant.canteenname,  canteenrestaurant.floorname,  canteenrestaurant.restaurantname,    restaurantdish.dishname, dishinformation.price,dishinformation.taste FROM   canteenrestaurant LEFT JOIN restaurantdish ON canteenrestaurant.restaurantname = restaurantdish.restaurantname LEFT JOIN dishinformation ON restaurantdish.dishname = dishinformation.dishname;"
            cur.execute(sql4)
            data = cur.fetchall()  # 通过fetchall方法获得数据
            formatted_data = "\n".join([" | ".join(map(str, row)) for row in data])#排版
            # 显示带有良好排版的消息框
            messagebox.showinfo("林科大校内食堂及附近小吃", formatted_data)
        elif combo_var2.get().strip() == '后街':
            sql5="SELECT canteenrestaurant.canteenname,  canteenrestaurant.floorname,  canteenrestaurant.restaurantname,    restaurantdish.dishname, dishinformation.price,dishinformation.taste FROM   canteenrestaurant LEFT JOIN restaurantdish ON canteenrestaurant.restaurantname = restaurantdish.restaurantname LEFT JOIN dishinformation ON restaurantdish.dishname = dishinformation.dishname where canteenname=\"后街小吃\";"
            cur.execute(sql5)
            data = cur.fetchall()  # 通过fetchall方法获得数据
            formatted_data = "\n".join([" | ".join(map(str, row)) for row in data])
            # 显示带有良好排版的消息框
            messagebox.showinfo("后街小吃", formatted_data)
        elif combo_var2.get().strip() == "东园":
            sql6="SELECT canteenrestaurant.canteenname,  canteenrestaurant.floorname,  canteenrestaurant.restaurantname,    restaurantdish.dishname, dishinformation.price,dishinformation.taste FROM   canteenrestaurant LEFT JOIN restaurantdish ON canteenrestaurant.restaurantname = restaurantdish.restaurantname LEFT JOIN dishinformation ON restaurantdish.dishname = dishinformation.dishname where canteenname=\"林海食堂\" or canteenname=\"林语食堂\";"
            cur.execute(sql6)
            data = cur.fetchall()  # 通过fetchall方法获得数据
            formatted_data = "\n".join([" | ".join(map(str, row)) for row in data])
            # 显示带有良好排版的消息框
            messagebox.showinfo("东园食堂", formatted_data)
        elif combo_var2.get().strip() == "西园":
             sql7 = "SELECT canteenrestaurant.canteenname,  canteenrestaurant.floorname,  canteenrestaurant.restaurantname,    restaurantdish.dishname, dishinformation.price,dishinformation.taste FROM   canteenrestaurant LEFT JOIN restaurantdish ON canteenrestaurant.restaurantname = restaurantdish.restaurantname LEFT JOIN dishinformation ON restaurantdish.dishname = dishinformation.dishname where canteenname=\"林冠食堂\" or canteenname=\"林苑食堂\";"
             cur.execute(sql7)
             data = cur.fetchall()  # 通过fetchall方法获得数据
             formatted_data = "\n".join([" | ".join(map(str, row)) for row in data])
             # 显示带有良好排版的消息框
             messagebox.showinfo("西园食堂", formatted_data)
    except Exception as e:
            messagebox.showinfo("ERROR", f"发生异常: {e}")
    finally:
         conn.close()
def delete_value():#输入店铺名字,删除店铺相关信息
     conn = pymysql.connect(host="localhost", port=3306, user="root", password=pd, db='eat',charset='utf8')  # 连接本地数据库
     cur = conn.cursor()  # 生成游标对象r
     content_list = []
     try:
         for i in range(2, 7):  # 获取Entry对象中的文本
            content = text_zujian['text_var' + str(i)].get()
            content_list.append(content)
         sql1="delete from canteenrestaurant where restaurantname='"+content_list[1]+"';"
         sql2 = "delete from restaurantdish where restaurantname='" + content_list[1]+"';"
         sql3="delete from dishinformation where restaurantname='" + content_list[1]+"';"
         cur.execute(sql3)
         cur.execute(sql2)
         cur.execute(sql1)
         if content_list[1]=="":
             messagebox.showinfo("消息", "请输入店铺")
         else:
             messagebox.showinfo("消息", "删除成功")
        # data = cur.fetchall()  # 通过fetchall方法获得数据
         conn.commit()  # 向服务器提交修改
     except Exception as e:
             messagebox.showinfo("ERROR", f"发生异常: {e}")
     finally:
         conn.close()
def get_all_data():#获取eat数据库的所有数据
    conn = pymysql.connect(host="localhost", port=3306, user="root", password=pd, db='eat',
                           charset='utf8')  # 连接本地数据库
    cur = conn.cursor()  # 生成游标对象r
    try:
        # 获取所有的表名
        cur.execute("SHOW TABLES")
        tables = cur.fetchall()
        # 创建一个字典来存储所有的数据
        data_dict = {}
        # 对每个表执行SELECT查询并将结果存储到字典中
        for table in tables:
            cur.execute(f"SELECT * FROM {table[0]}")
            results = cur.fetchall()
            data_dict[table[0]] = results
        # 关闭数据库连接
    finally:
        conn.close()
    return data_dict
def main():#调用千帆大平台
    # 获取所有的数据库信息
    data_dict = get_all_data()
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_access_token()
    messages = []
    messages.append({
        "role": "user",
        "content": "你现在是一个智能餐品推荐助手,你需要根据用户提供的信息和倾向为用户提供你认为的最好的选择,提供数据库里面的所有信息,包括地址位置,餐厅,店铺的名字以及主品,请不要回复与数据库无关的信息,如果用户提问的方式无法理解,就告诉用户你无法理解,并随机推荐几个食物,若用户没有提供任何信息也随机推荐食物。以下是数据库。"#+str(data_dict)
    })
    # 添加数据库信息到消息中
    payload = json.dumps({
        "messages": messages
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response_dict = json.loads(response.text)
    messages.append({
        "role": "assistant",
        "content": response_dict['result']
    })
    # 添加第二条消息
    messages.append({
        "role": "user",
        "content":"你推荐的数据需要包括数据库里面的信息,包括地址位置(当用户输入了地址,如东园,则不要推荐位于西园或者后街的食品),餐厅,店铺的名字以及主品,以下是我的需求(如果我没有提供任何信息,请随机推荐几个不同的食物,最多不要超过3个)"+ content_list[0]
    })
    # 再次发送请求并接收回复
    payload = json.dumps({
        "messages": messages
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    response_dict = response.json()
    label1111 = tkinter.Label(background_frame, text=response_dict['result'], wraplength=500)
    label1111.pack()
    messages.append({
        "role": "assistant",
        "content": response_dict['result']
    })
def get_access_token():#百度提供的调用函数
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))
text_widgets = {}
def output_ai():#运行main函数
    content = text_entry.get('1.0', 'end')
    content_list.append(content)
    main()
def raise_frame(frame):#模块切换的函数
    frame.tkraise()
#模块1
def update_combobox(*args):
    if combo_var2.get() == "后街":
        combox_box2['values'] = ["后街小吃"]
    elif combo_var2.get() == "东园":
        combox_box2['values'] = ["林海食堂", "林语食堂"]
    else:
        combox_box2['values'] = ["林涛食堂", "林苑食堂"]
def open_f2_window():
    f2_window = tk.Toplevel(root)
    f2_window.title("数据库修改")
    combox_box2 = ttk.Combobox(f2_window)
    combo_var2 = tk.StringVar()
    combox_box3 = ttk.Combobox(f2_window, textvariable=combo_var2)
    combox_box3["value"] = ["后街", "西园", "东园"]
    btn1 = tk.Button(f2_window, text="添加数据", command=print_value)
    btn2 = tk.Button(f2_window, text="查找数据", command=find_value)
    btn3 = tk.Button(f2_window, text="删除数据", command=delete_value)
    text_widgets1 = {}  # 创建一个字典来存放文本输入
    text_zujian = {}
    for i in range(2, 7):
        text_zujian['entertext' + str(i)] = tk.Entry(f2_window)
        text_zujian['entertext' + str(i)].grid(row=i + 1, column=2)
    label44 = tk.Label(f2_window, text="店铺名称")
    label55 = tk.Label(f2_window, text="主品名称")
    label77 = tk.Label(f2_window, text="楼层(仅需输入阿拉伯数字)")
    label11 = tk.Label(f2_window, text="选择食堂")
    label88 = tk.Label(f2_window, text="选择东/西/后街")
    label99 = tk.Label(f2_window, text="价格")
    label111 = tk.Label(f2_window, text="口味")
    combox_box3.grid(row=1, column=2)
    combox_box2.grid(row=2, column=2)
    label11.grid(row=2, column=1)
    label88.grid(row=1, column=1)
    label44.grid(row=4, column=1)
    label55.grid(row=5, column=1)
    label77.grid(row=3, column=1)
    label99.grid(row=6, column=1)
    label111.grid(row=7, column=1)
    btn1.grid(row=15, column=20)
    btn2.grid(row=20, column=20)
    btn3.grid(row=25, column=20)
root = tk.Tk()
root.title("今天吃什么")
background_frame = tk.Frame(root, bg="#F5F5F5")
background_frame.grid(row=0, column=0, sticky="nsew")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
values = {"后街", "西园食堂", "东园食堂"}
root.geometry('800x500')
root.title("今天吃什么")
root.configure(bg="#F5F5F5")
text_entry = tk.Text(root, height=10, width=120)
text_entry.grid(row=1, column=0, columnspan=2, rowspan=2, sticky='s', pady=10)  # 占据底部中间
btn33 = tk.Button(root, height=6,text="发送", command=output_ai)
btn33.grid(row=1, column=2, sticky='e', pady=10)  # 粘贴在右侧
tk.Button(root, text='修改食品库', command=open_f2_window).grid(row=0, column=0, sticky="ne")
root.mainloop()