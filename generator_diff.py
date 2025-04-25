import sys
import random

def generate_valid_move():
    # 生成一个有效的落子位置，行列在 1 到 19 之间
    x = random.randint(1, 19)
    y = random.randint(1, 19)
    return f"{x} {y}"

def generate_special_moves():
    # 生成特殊位置，包括棋盘的角落和边缘
    special_moves = [
        "1 1", "19 1", "1 19", "19 19",  # 四个角落
        "1 10", "19 10", "10 1", "10 19",  # 四条边缘
        "10 10", "5 5", "15 15",  # 中心和其他有意义的点
        "2 2", "18 18", "9 9"  # 特殊的边界
    ]
    return random.choice(special_moves)

def generator(t):
    num_moves = int(t)  # 从命令行参数获取生成的落子数量
    moves = []

    # 增加围困局面来测试提子逻辑
    # 这里的棋子会形成一个完全围困的局面，需要提子
    moves.extend([
        "3 3", "3 4", "3 5", "4 4", "5 4",  # 围住 4,4 位置的棋子，测试提子
        "15 15", "15 16", "15 17", "16 16", "17 16",  # 另一组围困棋子，测试提子
    ])
    
    # 增加更多的围困和提子局面
    moves.extend([
        "7 7", "7 8", "8 7", "8 8",  # 一个小的围困局面
        "12 12", "12 13", "13 12", "13 13",  # 另一小围困局面
    ])

    # 增加随机生成的多样化位置，确保触发模拟器的不同逻辑
    for _ in range(num_moves - 10):
        move = generate_valid_move()
        moves.append(move)

    # 返回生成的所有落子位置，每行一个位置
    return "\n".join(moves)

if __name__ == '__main__':
    # 获取命令行参数
    t = sys.argv[1]  # 落子数量
    outname = sys.argv[2]  # 输出文件名
    
    # 写入输出文件
    with open(outname, "w") as fout:
        fout.write(generator(t))
