import numpy as np



def possible (x,y,n):
    global grid
    for i in range (9): # od 0 do 8
        if grid[x][i] == n:
            return False
    for i in range (9):
        if grid[i][y] == n:
            return False
    
    x0 = (x//3)*3 # nastavíme počáteční souřadnice sub-pole, ve kterém je x, y
    y0 = (y//3)*3
    for i in range (3):
        for j in range (3):
            if grid[x0+i][y0+j] == n:
                return False
    return True        

def backtrack():
    global grid
    global backtracks
    for y in range(9):
        for x in range(9):
            if grid[x][y] == 0:
                for n in range(1,10):
                    if possible(x,y,n):
                        grid[x][y] = n
                        backtrack()         # rekurze
                        backtracks += 1
                        grid[x][y] = 0  # backtrack - pozici vynulujeme                            
                return    # vrátí se o jednu úroveň výš
    print(np.matrix(grid))
    print(backtracks)


def backtrack_reverse():
    global grid
    global backtracks    
    for y in range(8,-1,-1):
        for x in range(8,-1,-1):
            if grid[x][y] == 0:
                for n in range(1,10):
                    if possible(x,y,n):
                        grid[x][y] = n
                        backtrack_reverse()         # rekurze
                        backtracks += 1
                        grid[x][y] = 0  # backtrack - pozici vynulujeme                            
                return    # vrátí se o jednu úroveň výš
    print(np.matrix(grid))
    print(backtracks)


if __name__ == '__main__':

        grid = [[5,3,0,0,7,0,0,0,0],
                [6,0,0,1,9,5,0,0,0],
                [0,9,8,0,0,0,0,6,0],
                [8,0,0,0,6,0,0,0,3],
                [4,0,0,8,0,3,0,0,1],
                [7,0,0,0,2,0,0,0,6],
                [0,6,0,0,0,0,2,8,0],
                [0,0,0,4,1,9,0,0,5],
                [0,0,0,0,8,0,0,7,9]]
        
        backtracks = 0
        backtrack()
        
        backtracks = 0
        backtrack_reverse() # vhodné pro zadání, kdy je více známých hodnot na konci






