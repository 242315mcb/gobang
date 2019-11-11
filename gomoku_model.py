class Model(object):
	'''五子棋盘数据，二维数组'''
	def __init__(self, row=15, col=15):
		self.row = row
		self.col = col
		self.model = [[0 for c in range(col)] for r in range(row)]


	def init(self):
		self.model = [[0 for c in range(self.col)] for r in range(self.row)]

	def setValue(self, r, c, value):
		'''设置(r,c)位置的值为value'''
		if r >= self.row or r < 0 or c >= self.col or c < 0 :
			print('设置值-位置超出边界')
			return None
		self.model[r][c] = value


	def getValue(self, r, c):
		'''获取r,c)位置的值'''
		if r >= self.row or r < 0 or c >= self.col or c < 0 :
			print('获取值-位置超出边界')
			return None
		return self.model[r][c]


	def countValue(self, r, c, value):
		'''计算(r,c)位置最大个数'''
		if r >= self.row or r < 0 or c >= self.col or c < 0 :
			print('计算值-位置超出边界')
			return -1
		
		#-	横方向
		max = self.countHorizontal(r, c, value)
		#|	竖方向
		tmp = self.countVertical(r, c, value)
		max = max if max>tmp else tmp
		#/	左上到右下
		tmp = self.countOblique(r, c, value)
		max = max if max>tmp else tmp
		#\	右上到左下
		tmp = self.countBackslash(r, c, value)
		max = max if max>tmp else tmp
		return max


	def countHorizontal(self, r, c, value, style='Both'): 
		count = 0
		# print('(%d,%d) value is %d and the v is %d' %(r,c,self.model[r][c], value))
		if self.model[r][c] == value:
			count += 1
			# print('c-1 is %d,c+1 is %d'%(c-1,c+1))
			if c-1>=0 and style!='Down':
				count += self.countHorizontal(r, c-1, value, style='Up')
			if c+1<self.col and style!='Up':
				count += self.countHorizontal(r, c+1, value, style='Down')
		return count


	def countVertical(self, r, c, value, style='Both'):
		count = 0
		if self.model[r][c] == value:
			count += 1
			if r-1>=0 and style!='Down':
				count += self.countVertical(r-1, c, value, style='Up')
			if r+1<self.row and style!='Up':
				count += self.countVertical(r+1, c, value, style='Down')
		return count


	def countOblique(self, r, c, value, style='Both'):
		count = 0
		if self.model[r][c] == value:
			count += 1
			if r-1>=0 and c-1>=0 and style!='Down':
				count += self.countOblique(r-1, c-1, value, style='Up')
			if r+1<self.row and c+1<self.col and style!='Up':
				count += self.countOblique(r+1, c+1, value, style='Down')
		return count


	def countBackslash(self, r, c, value, style='Both'):
		count = 0
		if self.model[r][c] == value:
			count += 1
			if r-1>=0 and c+1<self.col and style!='Down':
				count += self.countBackslash(r-1, c+1, value, style='Up')
			if r+1<self.row and c-1>=0 and style!='Up':
				count += self.countBackslash(r+1, c-1, value, style='Down')
		return count

	def __str__(self):
		rs = ''
		for r in range(self.row):
			rs = rs + str(self.model[r]) + '\n'
		return rs
		


'''
设想找到目前为最适合位置，根据当前的已有的棋子，不好找
网上找一个评分的5元组的，没搞懂，还有博弈的，alaph-betal
'''
if __name__ == '__main__':
	#from random import *
	row, col = 15, 15
	m = Model(row, col)

	