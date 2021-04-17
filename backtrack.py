import numpy as np

class Task:
    def __init__(self, grid):
        self.grid=grid

    def possible(self,x,y,n):
        for i in range (9):
            if self.grid[x][i] == n :
                return False
        for i in range (9):
            if self.grid[i][y] == n :
                return False
        
        x0 = (x//3)*3 # nastavíme počáteční souřadnice sub-pole, ve kterém je x, y
        y0 = (y//3)*3
        for i in range (3) :
            for j in range (3) :
                if self.grid[x0+i][y0+j] == n :
                    return False
        return True        

    def backtrack(self):
        for y in range(9):
            for x in range(9):
                if self.grid[x][y] == 0 :
                    for n in range(1,10):
                        if self.possible(x,y,n):
                            self.grid[x][y] = n
                            self.backtrack()         # rekurze
                            self.grid[x][y] = 0  # backtrack - pozici vynulujeme
                    return    # vrátí se o jednu úroveň výš
        print(np.matrix(self.grid))

    def backtrack_reverse(self):
        for y in range(8,-1,-1):
            for x in range(8,-1,-1):
                if self.grid[x][y] == 0 :
                    for n in range(1,10):
                        if self.possible(x,y,n):
                            self.grid[x][y] = n
                            self.backtrack_reverse()         # rekurze
                            self.grid[x][y] = 0  # backtrack - pozici vynulujeme
                    return    # vrátí se o jednu úroveň výš
        print(np.matrix(self.grid))