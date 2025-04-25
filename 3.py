import sys

class GoBoard:
    def __init__(self, size=19):
        self.size = size
        self.board = [['.' for _ in range(size)] for _ in range(size)]

    def place_stone(self, line, color):
        try:
            x, y = line.split()
            x = int(x) - 1
            y = int(y) - 1
            if x < 0 or x > 18 or y < 0 or y > 18:
                return
            self.board[x][y] = color
            self.check_captures()
        except:
            pass
    
    def check_captures(self):
        index = 0
        vis = [[-1 for _ in range(self.size)] for _ in range(self.size)]

        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] != '.' and vis[r][c] == -1:
                    self.get_group(r, c, index, self.board[r][c], vis)
                    index = index + 1
    
        liberties = [0 for _ in range(index)]

        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == '.':
                    continue
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size:
                        if self.board[nr][nc] == '.':
                            liberties[vis[r][c]] = 1
                            
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == '.':
                    continue
                if liberties[vis[r][c]] == 0:
                    self.board[r][c] = '.'

    
    def get_group(self, r, c, index, color, vis):

        vis[r][c] = index
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    if vis[nr][nc] == - 1 and self.board[nr][nc] == color:
                        self.get_group(nr, nc, index, color, vis)
    
    def display(self, outfile):
        for row in self.board:
            output = ' '.join(row) + '\n'
            outfile.write(output)

    def simulate(self, inname, outname):
        infile = open(inname, 'r')
        outfile = open(outname, 'w')
        sequence = infile.readlines()
        infile.close()
        if(len(sequence) > 1000):
            outfile.write("")
            outfile.close()
            return
        color = 0
        for line in sequence:
            self.place_stone(line, 'B' if color == 0 else 'W')
            color = color ^ 1
        self.display(outfile)
        outfile.close()

if __name__ == '__main__':
    inname = sys.argv[1]
    outname = sys.argv[2]
    Go = GoBoard()
    Go.simulate(inname, outname)
    