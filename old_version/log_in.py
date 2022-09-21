import tkinter
from tkinter import messagebox
import socket


class SignWin:
    def __init__(self):
        self.root = tkinter.Tk()
        self.radioBtnValue = tkinter.IntVar(value=1)
        self.__setRoot()
        self.__loadWidgets()
        self.__setWidget()
        self.__placeWidget()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __setRoot(self):
        self.root.title("登录")
        self.root.geometry(f"400x300"
                           f"+{int(self.root.winfo_screenwidth() / 2) - 200}"
                           f"+{int(self.root.winfo_screenheight() / 2) - 250}")
        self.root.config(bg='lightgreen')

    def __loadWidgets(self):
        self.titleLabel = tkinter.Label()
        self.ipLabel = tkinter.Label()
        self.portLabel = tkinter.Label()
        self.nameLabel = tkinter.Label()

        self.ipEntry = tkinter.Entry(self.root)
        self.portEntry = tkinter.Entry(self.root)
        self.nameEntry = tkinter.Entry(self.root)
        self.logButton = tkinter.Button()

        self.radioBtn1 = tkinter.Radiobutton(master=self.root)
        self.radioBtn2 = tkinter.Radiobutton(master=self.root)

    def __placeWidget(self):
        self.titleLabel.place(x=110, y=20)
        self.ipLabel.place(x=90, y=120)
        self.portLabel.place(x=80, y=150)
        self.nameLabel.place(x=80, y=180)

        self.ipEntry.place(x=130, y=120)
        self.portEntry.place(x=130, y=150)
        self.nameEntry.place(x=130, y=180)

        self.logButton.place(x=180, y=250)

        self.radioBtn1.place(x=110, y=210)
        self.radioBtn2.place(x=240, y=210)

    def __setWidget(self):
        self.titleLabel.config(text='联机贪吃蛇\n登录界面', font=('', 24, 'bold'), bg='lightgreen')
        self.ipLabel.config(text='IP:', bg='lightgreen', font=('', 12, 'bold'))
        self.portLabel.config(text='port:', bg='lightgreen', font=('', 12, 'bold'))
        self.nameLabel.config(text='name:', bg='lightgreen', font=('', 12, 'bold'))

        self.ipEntry.insert(0, "127.0.0.1")
        self.portEntry.insert(0, "25565")
        self.ipEntry.config(font=('', 12, 'bold'))
        self.portEntry.config(font=('', 12, 'bold'))
        self.nameEntry.config(font=('', 12, 'bold'))

        self.logButton.config(text='登录', font=('', 12, 'bold'), bg='white', command=self.logIn)

        self.radioBtn1.config(text='单人游戏', variable=self.radioBtnValue, value=1,bg='lightgreen')
        self.radioBtn2.config(text='多人游戏', variable=self.radioBtnValue, value=2,bg='lightgreen')

    def logIn(self):
        if self.radioBtnValue.get() == 1:
            messagebox.showinfo('登录','进入单人游戏')
            self.root.destroy()
            return
        ip = self.ipEntry.get()
        port = self.portEntry.get()
        name = self.nameEntry.get()

        if name not in ['', ' ']:
            self.data = (ip, port, name)
            self.logButton.config(text='登录中')
            messagebox.showinfo('登录', f'name为{name}的玩家将登录到{ip}:{port}')

            self.connect((ip, int(port)))

        else:
            messagebox.showinfo('登录', 'name不能为空')
            self.nameEntry.delete(0, len(name))

    def mainloop(self):
        print(self.radioBtnValue)
        self.root.mainloop()

    def connect(self, param):
        try:
            self.socket.connect(param)
        except:
            messagebox.showerror('登录', '连接服务器失败\n请重试')
            self.logButton.config(text='登录')
            return

        self.socket.send(f'4:name={self.nameEntry.get()}'.encode())

        recv_data = self.socket.recv(1024).decode().split(':')[1]

        if recv_data == 'Ok':
            messagebox.showinfo('登录', '登录成功')
            self.root.destroy()
            return
        if recv_data == 'Fail':
            messagebox.showerror('登录', '连接服务器失败\n请重试')
            self.logButton.config(text='登录')
            return

        messagebox.showerror('登录', f'未知错误:{recv_data}')
        print(recv_data)


if __name__ == '__main__':
    x = SignWin()

    print(x.radioBtnValue)
    x.mainloop()
