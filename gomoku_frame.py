from tkinter import *
from tkinter.messagebox import *
from gomoku_model import *

class Chess(object):
	'''五子棋棋盘界面'''
	def __init__(self, model, row=15, col=15, mesh=25, ratio=0.9):
		## param ##
		self.borad_bg = '#CDBA96'
		self.row = row
		self.col = col
		self.ratio = ratio
		self.mesh = mesh
		self.step = self.mesh/2
		self.model = model
		self.chess = self.step * self.ratio
		self.point = self.step * 0.2
		self.is_start = False
		self.is_black = True
		self.last_point = None
		self.historical_point = []
		self.btn_font = ('黑体', 12, 'bold')
		self.lab_font = ('楷体', 18, 'bold')
		self.lab_fg	 = 'white'
		self.frame_bg = '#CDC0B0'

		## GUI ##
		self.root = Tk()
		self.title = '五子棋'
		self.root.title(self.title)
		self.root.resizable(width=False, height=False)
										 
		self.frame_head = Frame(self.root, highlightthickness=0, bg=self.frame_bg)
		self.frame_head.pack(fill=BOTH, ipadx=10)

		self.btn_start = Button(self.frame_head, text='开始', command=self.start_game ,font=self.btn_font)
		self.btn_restart = Button(self.frame_head, text='重来', command=self.restart_game ,font=self.btn_font, state=DISABLED)
		self.lab_info = Label(self.frame_head, text='未开始', bg=self.frame_bg, font=self.lab_font, fg=self.lab_fg)
		self.btn_regret = Button(self.frame_head, text='悔棋', command=self.regret_game ,font=self.btn_font, state=DISABLED)
		self.btn_lose = Button(self.frame_head, text='认输', command=self.lose_game ,font=self.btn_font, state=DISABLED)

		self.btn_start.pack(side=LEFT, padx=20)
		self.btn_restart.pack(side=LEFT)
		self.lab_info.pack(side=LEFT, expand=YES, fill=BOTH, pady=10)
		self.btn_regret.pack(side=RIGHT, padx=20)
		self.btn_lose.pack(side=RIGHT)

		# self.root = master
		self.canvas = Canvas(self.root, bg=self.borad_bg, width=(self.col+1)*self.mesh, 
								height=(self.row+1)*self.mesh, highlightthickness=0)
		self.draw_board()
		self.canvas.bind("<Button-1>", self.canvas_clikc)
		self.canvas.pack()

		self.root.mainloop()
			

	def draw_board(self):
		'''画整个棋盘'''
		[[self.draw_mesh(r, c) for c in range(self.col)] for r in range(self.row)]
		self.canvas.bg = self.borad_bg
		self.canvas.pack()


	def draw_mesh(self, x, y):
		'''画棋盘网格'''
		# 一个倍率，由于tkinter操蛋的GUI，如果不加倍率，悔棋的时候会有一点痕迹，可以试试把这个改为1，就可以看到
		ratio = (1 - self.ratio) * 0.99 + 1
		center_x, center_y = self.mesh* (x + 1), self.mesh * (y + 1)
		#画背景颜色
		self.canvas.create_rectangle(center_y - self.step, center_x - self.step,
										center_y + self.step, center_x - self.step,
										fill=self.borad_bg, outline=self.borad_bg)
		#画网格线 x,y 中心画十字 长度step
		## 三元表达式中嵌套三元表达式
		a, b = [0, ratio] if y==0 else [-ratio, 0] if y==self.row-1 else [-ratio, ratio]
		c, d = [0, ratio] if x==0 else [-ratio, 0] if x==self.col-1 else [-ratio, ratio]
		# print('(%d,%d) ratio is %d,%d,%d,%d' %(x,y,a,b,c,d))
		self.canvas.create_line(center_y+a*self.step, center_x, center_y+b*self.step, center_x)
		self.canvas.create_line(center_y, center_x+c*self.step, center_y, center_x+d*self.step)

		if ((x==self.col/5 or x==self.col*4/5-1) and (y==self.row/5 or y==self.row*4/5-1)) or (x==int(self.col/2) and y==int(self.row/2)):
			self.canvas.create_oval(center_y - self.point, center_x - self.point, center_y + self.point, center_x + self.point, fill='black')


	def draw_chess(self, x, y, color, outline='black'):
		'''画棋子'''
		center_x, center_y = self.mesh * (x+1), self.mesh * (y+1)
		self.canvas.create_oval(center_y - self.chess, center_x - self.chess, 
								center_y + self.chess, center_x + self.chess,
								fill=color, outline=outline)


	def draw_all_chess(self):
		pass


	def center_show(self, text):
		'''设置中间文件显示'''
		width, height = int(self.canvas['width']), int(self.canvas['height'])
		self.canvas.create_text(int(width/2), int(height/2), text=text, font=self.lab_font, fill='red')


	def canvas_clikc(self, event):
		'''点击事件'''
		# 找点击的最近坐标
		x, y = int((event.y - self.step)/self.mesh), int((event.x - self.step)/self.mesh)
		# 坐标的中心位置
		center_x, center_y = self.mesh * (x+1), self.mesh * (y+1)
		# 点到中心的距离
		distance = ((center_x - event.y) ** 2) + ((center_y - event.x) ** 2) ** 0.5
		# 点击位置不在棋子范围内，改点也有棋子，游戏没开始则退出
		if not self.is_start or distance > self.step * 0.95 or self.model.getValue(x, y) != 0:
			return
		# 判断是下棋方
		color = self.ternary_operator('black', 'white')
		self.historical_point.append((color,x,y))
		# 画棋子
		self.draw_chess(x, y, color)
		# 设置数据
		tag = self.ternary_operator(1, -1)
		self.model.setValue(x, y, tag)
		self.last_point = [x, y]
		if self.is_win(x, y, tag):
			self.is_start = False
			self.set_btn_state('init')
			text = self.ternary_operator('黑方胜', '白方胜')
			self.center_show(text)
			print('历史棋子%s' %self.historical_point)
			return
		# 转化棋手
		self.transform_identify()

	def is_win(self, x, y, tag):
		'''判断是否满足'''
		print('count the values ...')
		max = self.model.countValue(x, y, tag)
		# print(self.model)
		if max == 5:
			return True
		return False

	def start_game(self):
		'''开始游戏'''
		print('being game...')
		# 初始化棋盘
		self.set_btn_state('start')
		self.is_start = True
		self.is_black = True
		self.model.init()
		self.lab_info.config(text='黑方下')
		self.canvas.delete('all')
		self.draw_board()

	def restart_game(self):
		'''重新游戏'''
		print('restart game....')
		self.start_game()

	def regret_game(self):
		'''悔棋，上一步'''
		print('regret game...')
		if not self.last_point:
			print('现在不能悔棋')
			showinfo('提示', '现在不能悔棋')
			return
		x, y = self.last_point
		#self.draw_mesh(x, y, self.borad_bg)
		self.draw_chess(x, y, self.borad_bg, outline=self.borad_bg)
		self.draw_mesh(x,y)		
		self.last_point = None
		# 悔棋有点击事件，悔棋后还是自己下
		self.model.setValue(x, y, 0)
		self.transform_identify()
		self.historical_point.pop()


	def lose_game(self):
		'''认输，结束游戏'''
		print('lose game....')
		self.set_btn_state('init')
		self.is_start = False
		text = self.ternary_operator('黑方认输', '白方认输')
		self.lab_info.config(text=text)
		self.center_show('输')


	def set_btn_state(self,state):
		'''设置按钮的状态'''
		state_list = [NORMAL, DISABLED, DISABLED, DISABLED] if state == 'init' else [DISABLED, NORMAL, NORMAL, NORMAL]
		self.btn_start.config(state=state_list[0])
		self.btn_restart.config(state=state_list[1])
		self.btn_lose.config(state=state_list[2])
		self.btn_regret.config(state=state_list[3])

	def ternary_operator(self, true, false):
		'''判断黑方的三元组'''
		return true if self.is_black else false

	def transform_identify(self):
		'''转化下棋'''
		self.is_black = not self.is_black
		text = self.ternary_operator('黑放下', '白方下')
		self.lab_info.config(text=text)

if __name__ == '__main__':
	row, col = 15, 15
	model = Model(row, col)
	chess = Chess(model, row, col)





