__version__ = "python3.6 0.0.1"
__mark__ = "参考 https://blog.csdn.net/qq_28969139/article/details/81008389"

from gomoku_frame import *



def main():
	row, col = 15, 15
	model = Model(row, col)
	chess = Chess(model, row, col)


if __name__ == "__main__":
	main()

