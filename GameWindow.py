import random
import tkinter
import tkinter.ttk as ttk


class Game_Win:
    def __init__(self):
        self.pFPosition = [10, 52, 95, 137]
        self.direction = (1, 0)
        self.keyPress = False
        self.root = tkinter.Tk()
        self.__setRoot()
        self.__loadWidgets()
        self.__placeWidget()

        # self.selectFrame()

    def __setRoot(self):
        self.root.title("贪吃蛇")
        self.root.geometry(f"900x604"
                           f"+{int(self.root.winfo_screenwidth() / 2) - 500}"
                           f"+{int(self.root.winfo_screenheight() / 2) - 300}")
        self.root.config(bg='lightcyan')
        self.root.resizable(0, 0)


    def __loadWidgets(self):
        self.canvas = tkinter.Canvas(self.root, width=600, height=600, bg='bisque')

        self.labelFrame1 = tkinter.LabelFrame(text="游戏模式", height=590, width=290, bg='lightcyan',
                                              font=("宋体", 18, "bold"), highlightcolor='lightgreen')
        self.singleModeBtn = tkinter.Button(self.labelFrame1, text='单人游戏', font=("宋体", 24, "bold"), bg='lightcyan',
                                            activebackground='lightcyan', activeforeground='lightskyblue',
                                            command=self.singleFrameShow)
        self.multiModeBtn = tkinter.Button(self.labelFrame1, text='多人游戏', font=("宋体", 24, "bold"), bg='lightcyan',
                                           activebackground='lightcyan',activeforeground='lightskyblue',
                                           command=self.multiFrameShow)

        # single Frame widget setting
        self.singleFrame = tkinter.LabelFrame(text='单人游戏', height=590, width=290, bg='lightcyan',
                                              font=("宋体", 12, "bold"), highlightcolor='lightgreen')
        self.headColorLbl = tkinter.Label(self.singleFrame, text=' 蛇头 ', font=("宋体", 14, "normal"),
                                          bg='green', relief='groove')
        self.bodyColorLbl = tkinter.Label(self.singleFrame, text=' 身体 ', font=("宋体", 14, "normal"),
                                          bg='lightgreen', relief='groove')

        self.startBtn = tkinter.Button(self.singleFrame, text='开始游戏', font=("宋体", 16, "bold"),
                                       padx=10, pady=10, bg='lightcyan')
        self.gameStateLbl = tkinter.Label(self.singleFrame, text='等待开始', font=("宋体", 32, "normal"), bg='lightcyan')
        self.scoreLbl = tkinter.Label(self.singleFrame, text='得分', font=("宋体", 24, "bold"), bg='lightcyan',
                                      relief='groove')
        self.scoreNumLbl = tkinter.Label(self.singleFrame, text='000', font=("华文琥珀", 52, "normal"), bg='lightcyan')
        self.singleBackBtn = tkinter.Button(self.singleFrame, text='返回', font=("华文琥珀", 12, "normal"),
                                            bg='lightcyan', command=self.back)

        # multiFrame widget setting
        self.multiFrame = tkinter.LabelFrame(text='多人游戏', height=590, width=290, bg='lightcyan',
                                             font=("宋体", 12, "bold"), highlightcolor='lightgreen')
        self.addressEntry = tkinter.Entry(master=self.multiFrame, font=('', 17, 'bold'), width=15)
        self.addressEntry.insert(0, '218.89.171.149:62872')
        self.connectBtn = tkinter.Button(self.multiFrame, text='连接', font=('', 12, 'bold'))
        self.roomEntry = tkinter.Entry(master=self.multiFrame, font=('', 17, 'bold'), width=12, )
        self.roomEntry.insert(0, 'Name')
        self.roomBtn = tkinter.Button(self.multiFrame, text='名字', font=('', 12, 'bold'))
        self.playerDataLF = tkinter.LabelFrame(self.multiFrame, text='  玩家  状态  得分  击杀  操作  ', height=230, width=276,
                                               bg='lightcyan',
                                               font=("宋体", 12, "normal"), highlightcolor='lightgreen')

        self.playerFrame1 = tkinter.Frame(self.playerDataLF, height=35, width=260, bg='pink', relief='groove')
        self.playerName1 = tkinter.Label(self.playerFrame1, text='明月清风', font=('', 12, 'normal'), bg='pink',
                                         wraplength=40, fg='coral')
        self.playerState1 = tkinter.Label(self.playerFrame1, text='等待\n加入', font=('', 11, 'normal'), bg='pink')
        self.playerScore1 = tkinter.Label(self.playerFrame1, text='000', font=('', 22, 'normal'), bg='pink')
        self.playerKill1 = tkinter.Label(self.playerFrame1, text='0', font=('', 22, 'normal'), bg='pink')
        self.playerBtn1 = tkinter.Button(self.playerFrame1, text='解散', font=('', 12, 'normal'), bg='pink')

        self.playerFrame2 = tkinter.Frame(self.playerDataLF, height=35, width=260, bg='pink', relief='groove')
        self.playerName2 = tkinter.Label(self.playerFrame2, text='昨日记忆', font=('', 12, 'normal'), bg='pink',
                                         wraplength=40)
        self.playerState2 = tkinter.Label(self.playerFrame2, text='未\n准备', font=('', 11, 'normal'), bg='pink')
        self.playerScore2 = tkinter.Label(self.playerFrame2, text='000', font=('', 22, 'normal'), bg='pink')
        self.playerKill2 = tkinter.Label(self.playerFrame2, text='0', font=('', 22, 'normal'), bg='pink')
        self.playerBtn2 = tkinter.Button(self.playerFrame2, text='请离', font=('', 12, 'normal'), bg='pink')

        self.playerFrame3 = tkinter.Frame(self.playerDataLF, height=35, width=260, bg='pink', relief='groove')
        self.playerName3 = tkinter.Label(self.playerFrame3, text='烟雨江南', font=('', 12, 'normal'), bg='pink',
                                         wraplength=40)
        self.playerState3 = tkinter.Label(self.playerFrame3, text='未\n准备', font=('', 11, 'normal'), bg='pink')
        self.playerScore3 = tkinter.Label(self.playerFrame3, text='000', font=('', 22, 'normal'), bg='pink')
        self.playerKill3 = tkinter.Label(self.playerFrame3, text='0', font=('', 22, 'normal'), bg='pink')
        self.playerBtn3 = tkinter.Button(self.playerFrame3, text='请离', font=('', 12, 'normal'), bg='pink')

        self.playerFrame4 = tkinter.Frame(self.playerDataLF, height=35, width=260, bg='pink', relief='groove')
        self.playerName4 = tkinter.Label(self.playerFrame4, text='起风了', font=('', 12, 'normal'), bg='pink',
                                         wraplength=40)
        self.playerState4 = tkinter.Label(self.playerFrame4, text='未\n准备', font=('', 11, 'normal'), bg='pink')
        self.playerScore4 = tkinter.Label(self.playerFrame4, text='000', font=('', 22, 'normal'), bg='pink')
        self.playerKill4 = tkinter.Label(self.playerFrame4, text='0', font=('', 22, 'normal'), bg='pink')
        self.playerBtn4 = tkinter.Button(self.playerFrame4, text='请离', font=('', 12, 'normal'), bg='pink')

        self.multiStartBtn = tkinter.Button(self.multiFrame, text='开始游戏', font=('', 22, 'normal'), bg='lightcyan')
        self.multiBackBtn = tkinter.Button(self.multiFrame, text='返回', font=("华文琥珀", 12, "normal"),
                                           bg='lightcyan', command=self.back)

    def __placeWidget(self):
        self.canvas.place(x=0, y=0)

        self.labelFrame1.place(x=606, y=10)
        self.singleModeBtn.place(x=65, y=110)
        self.multiModeBtn.place(x=65, y=250)

        self.singleFrame.place(x=1000, y=10)
        self.headColorLbl.place(x=20, y=45)

        self.bodyColorLbl.place(x=130, y=45)

        self.startBtn.place(x=75, y=100)
        self.gameStateLbl.place(x=45, y=190)
        self.scoreLbl.place(x=100, y=290)
        self.scoreNumLbl.place(x=75, y=360)
        self.singleBackBtn.place(x=200, y=500)

        self.multiFrame.place(x=1000, y=10)
        self.addressEntry.place(x=5, y=30)
        self.connectBtn.place(x=220, y=28)
        self.roomEntry.place(x=5, y=80)
        self.roomBtn.place(x=220, y=78)

        self.playerDataLF.place(x=6, y=135)

        self.playerFrame1.place(x=5, y=15)
        self.playerName1.place(x=15, y=0)
        self.playerState1.place(x=60, y=0)
        self.playerScore1.place(x=105, y=0)
        self.playerKill1.place(x=165, y=0)
        self.playerBtn1.place(x=205, y=3)

        self.playerFrame2.place(x=5, y=62)
        self.playerName2.place(x=15, y=0)
        self.playerState2.place(x=60, y=0)
        self.playerScore2.place(x=105, y=0)
        self.playerKill2.place(x=165, y=0)
        self.playerBtn2.place(x=205, y=3)

        self.playerFrame3.place(x=5, y=108)
        self.playerName3.place(x=15, y=0)
        self.playerState3.place(x=60, y=0)
        self.playerScore3.place(x=105, y=0)
        self.playerKill3.place(x=165, y=0)
        self.playerBtn3.place(x=205, y=3)

        self.playerFrame4.place(x=5, y=155)
        self.playerName4.place(x=15, y=0)
        self.playerState4.place(x=60, y=0)
        self.playerScore4.place(x=105, y=0)
        self.playerKill4.place(x=165, y=0)
        self.playerBtn4.place(x=205, y=3)

        self.multiStartBtn.place(x=70, y=400)
        self.multiBackBtn.place(x=200, y=500)

    def mainloop(self):
        self.root.mainloop()

    def singleFrameShow(self):
        self.labelFrame1.place(x=1000)
        self.multiFrame.place(x=1000)
        self.singleFrame.place(x=606)
        self.root.title('贪吃蛇-单人游戏')

    def multiFrameShow(self):
        self.labelFrame1.place(x=1000)
        self.singleFrame.place(x=1000)
        self.multiFrame.place(x=606)
        self.root.title('贪吃蛇-多人游戏')

    def setScore(self, score):
        self.scoreNumLbl.config(text=score)

    def startBtnBind(self, func):
        self.startBtn.config(command=func)

    def roomBtnBind(self, func):
        self.roomBtn.config(commanf=func)
        """
            调用此方法来为房间按钮绑定一个函数。
            绑定的函数需要完成如下功能：
                1.判断房间是否存在
                2.存在则 弹出窗口确认加入或者取消
                3.不存在则 弹出窗口询问是否要创建房间
                4.完成选择后改变self.roomLbl的文本为初始内容或者加入的房间名
                5.向服务器提交玩家名字
        """

    def connectBtnBind(self, func):
        self.connectBtn.config(command=func)
        """
            调用此方法来为连接按钮绑定一个函数。
            绑定的函数需要完成如下功能：
                1.尝试连接服务器
                2.发送 name
                3.失败弹出错误信息
        """

    def multiGStartBtnBind(self, func):
        self.multiStartBtn.config(command=func)

    def setPFColor(self, num, color):
        if num == 1:
            self.playerFrame1.config(bg=color)
            self.playerName1.config(bg=color)
            self.playerKill1.config(bg=color)
            self.playerState1.config(bg=color)
            self.playerScore1.config(bg=color)
            self.playerBtn1.config(bg=color)
            return
        if num == 2:
            self.playerFrame2.config(bg=color)
            self.playerName2.config(bg=color)
            self.playerKill2.config(bg=color)
            self.playerState2.config(bg=color)
            self.playerScore2.config(bg=color)
            self.playerBtn2.config(bg=color)
            return
        if num == 3:
            self.playerFrame3.config(bg=color)
            self.playerName3.config(bg=color)
            self.playerKill3.config(bg=color)
            self.playerState3.config(bg=color)
            self.playerScore3.config(bg=color)
            self.playerBtn3.config(bg=color)
            return
        if num == 4:
            self.playerFrame4.config(bg=color)
            self.playerName4.config(bg=color)
            self.playerKill4.config(bg=color)
            self.playerState4.config(bg=color)
            self.playerScore4.config(bg=color)
            self.playerBtn4.config(bg=color)
            return

    def back(self):
        self.multiFrame.place(x=1000)
        self.singleFrame.place(x=1000)
        self.labelFrame1.place(x=606)
        self.root.title("贪吃蛇")



if __name__ == '__main__':
    x = Game_Win()


    def setS():
        c = ['green', 'lightgreen', 'blue', 'lightblue', 'lightskyblue', 'cyan', 'lightcyan', 'grey', 'purple', 'orange']
        x.setPFColor(random.randint(1, 4), c[random.randint(0, 9)])


    x.multiGStartBtnBind(setS)

    x.mainloop()
