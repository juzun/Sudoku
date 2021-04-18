import time


def print_grid(grid):
    for i in range(len(grid)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - ")
        
        for j in range(len(grid)):
            if j % 3 == 0 and j != 0:
                print(" | ", end = "")
            
            if j == 8:
                print(grid[i][j])
            else:
                print(str(grid[i][j]) + " ", end = "")


def possible (grid, x, y, n):  # může být n na pozici [x,y]?
    for i in range (9):
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


# ***************************************************************** Backtrack

def backtrack(grid, x0 = 0, y0 = 0):
    global backtracks
    x, y = nextEmptyCell(grid, x0, y0)
    if x == -1:
        return True
    for n in range(1, 10):
        if possible(grid, x, y, n):
            grid[x][y] = n
            if backtrack(grid, x, y):
                return True            
            backtracks += 1
            grid[x][y] = 0        
    return False

def nextEmptyCell(grid, x0, y0):
    for x in range(x0, 9):  # mírné zjednodušení - netřeba procházet všechny předchozí řádky, ušetříme čas
        for y in range(9):
            if grid[x][y] == 0:
                return x, y
    return -1, -1


# ***************************************************************** Reverzní backtrack

def backtrack_reverse(grid, x0 = 8, y0 = 8):
    global backtracks
    x, y = nextEmptyCell_reverse(grid, x0, y0)
    if x == -1:
        return True
    for n in range(1, 10):
        if possible(grid, x, y, n):
            grid[x][y] = n
            if backtrack_reverse(grid, x, y):
                return True            
            backtracks += 1
            grid[x][y] = 0        
    return False

def nextEmptyCell_reverse(grid, x0, y0):
    for x in range(x0,-1,-1):
        for y in range(8,-1,-1):
            if grid[x][y] == 0:
                return x, y
    return -1, -1


# ***************************************************************** Backtrack s implikacemi

def backtrack_impl(grid, x0 = 0, y0 = 0):
    global backtracks
    x, y = nextEmptyCell(grid, x0, y0)
    if x == -1:
        return True
    for n in range(1, 10):
        if possible(grid, x, y, n):
            grid[x][y] = n
            impl = makeImplication(grid, x, y, n)
            if backtrack_impl(grid, x, y):
                return True
            undoImplication(grid, impl)
            backtracks += 1
            grid[x][y] = 0        
    return False


sectors = [[0, 3, 0, 3], [3, 6, 0, 3], [6, 9, 0, 3], 
           [0, 3, 3, 6], [3, 6, 3, 6], [6, 9, 3, 6], 
           [0, 3, 6, 9], [3, 6, 6, 9], [6, 9, 6, 9]]

def makeImplication(grid, i, j, e):
    global sectors
    grid[i][j] = e
    impl = [(i, j, e)]
    for k in range(len(sectors)):
        sectinfo = []
        vset = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for x in range(sectors[k][0], sectors[k][1]):
            for y in range(sectors[k][2], sectors[k][3]):
                if grid[x][y] != 0:
                    vset.remove(grid[x][y])
        for x in range(sectors[k][0], sectors[k][1]):
            for y in range(sectors[k][2], sectors[k][3]):
                if grid[x][y] == 0:
                    sectinfo.append([x, y, vset.copy()])
            
        for m in range(len(sectinfo)):
            sin = sectinfo[m]
            rowv = set()
            for y in range(9):
                rowv.add(grid[sin[0]][y])
            left = sin[2].difference(rowv)
            colv = set()
            for x in range(9):
                colv.add(grid[x][sin[1]])
            left = left.difference(colv)
            if len(left) == 1:
                val = left.pop()
                if possible(grid, sin[0], sin[1], val):
                    grid[sin[0]][sin[1]] = val
                    impl.append((sin[0], sin[1], val))
    return impl


def undoImplication(grid, impl):  
    for i in range(len(impl)):
        grid[impl[i][0]][impl[i][1]] = 0





if __name__ == '__main__':

        grid1 = [[5,3,0,0,7,0,0,0,0],
                 [6,0,0,1,9,5,0,0,0],
                 [0,9,8,0,0,0,0,6,0],
                 [8,0,0,0,6,0,0,0,3],
                 [4,0,0,8,0,3,0,0,1],
                 [7,0,0,0,2,0,0,0,6],
                 [0,6,0,0,0,0,2,8,0],
                 [0,0,0,4,1,9,0,0,5],
                 [0,0,0,0,8,0,0,7,9]]
        
        grid2 = [[5,1,7,6,0,0,0,3,4],
                 [2,8,9,0,0,4,0,0,0],
                 [3,4,6,2,0,5,0,9,0],
                 [6,0,2,0,0,0,0,1,0],
                 [0,3,8,0,0,6,0,4,7],
                 [0,0,0,0,0,0,0,0,0],
                 [0,9,0,0,0,0,0,7,8],
                 [7,0,3,4,0,0,5,6,0],
                 [0,0,0,0,0,0,0,0,0]]

        grid3 = [[5,1,7,6,0,0,0,3,4],
                 [0,8,9,0,0,4,0,0,0],
                 [3,0,6,2,0,5,0,9,0],
                 [6,0,0,0,0,0,0,1,0],
                 [0,3,0,0,0,6,0,4,7],
                 [0,0,0,0,0,0,0,0,0],
                 [0,9,0,0,0,0,0,7,8],
                 [7,0,3,4,0,0,5,6,0],
                 [0,0,0,0,0,0,0,0,0]]


        grid = grid2

        
        backtracks = 0
        start = time.time()
        backtrack(grid)
        end = time.time() 
                
        print_grid(grid)
        print("Number of backtracks: " + str(backtracks))
        print(end-start)










