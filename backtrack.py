import time

def flatten(input):
    new_list = []
    for i in input:
        for j in i:
            new_list.append(j)
    return new_list


def print_grid(grid):  # vykresli mřížku
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


def nextEmptyCell(grid, x0, y0):   # najde další prázdnou buňku
    for x in range(x0, 9):  # optimalizace - netřeba procházet všechny předchozí řádky, ušetříme čas
        for y in range(9):
            if grid[x][y] == 0:
                return x, y
    return -1, -1


def nextEmptyCell_reverse(grid, x0, y0):
    for x in range(x0,-1,-1):
        for y in range(8,-1,-1):
            if grid[x][y] == 0:
                return x, y
    return -1, -1


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


# ***************************************************************** Backtrack s implikacemi

def backtrack_impl(grid, x0 = 0, y0 = 0):
    global backtracks
    x, y = nextEmptyCell(grid, x0, y0)
    if x == -1:
        return True
    for n in range(1, 10):
        if possible(grid, x, y, n):            
            impl = implicate(grid, x, y, n)
            if backtrack_impl(grid, x, y):
                return True
            unimplicate(grid, impl)  # pokud se musíme vrátit, musíme smazat všechny implikace, ne jen [x,y] = n, proto posíláme impl na vstup a výstup
            backtracks += 1  
    return False


sectors = [[0, 3, 0, 3], [3, 6, 0, 3], [6, 9, 0, 3], 
           [0, 3, 3, 6], [3, 6, 3, 6], [6, 9, 3, 6], 
           [0, 3, 6, 9], [3, 6, 6, 9], [6, 9, 6, 9]]


def implicate(grid, x, y, n):
    global sectors
    grid[x][y] = n
    impl = [(x, y, n)]  # seznam implikací - krom samotného dosazení [x,y] = n bude obsahovat i další možná dosazení v každém sektoru za použití následujícího algoritmu
    
    for s in range(len(sectors)):
        empty_cells = []                 # seznam prázdných buněk v daném sektoru
        sector_opt = {1, 2, 3, 4, 5, 6, 7, 8, 9}   # seznam chybějících čísel v daném sektoru - možnosti sektoru
        
        for i in range(sectors[s][0], sectors[s][1]):     # pro všechny prvky sektoru
            for j in range(sectors[s][2], sectors[s][3]):
                if grid[i][j] != 0:
                    sector_opt.remove(grid[i][j])  # souřadnice nenulové hodnoty vymaž ze seznamu možností
                else:
                    empty_cells.append([i, j])   # souřadnice nulové hodnoty přidej do seznamu prázdných buněk
            
        for c in range(len(empty_cells)):
            empty_cell = empty_cells[c]                     # prázdná buňka c
            x_o, y_o = empty_cell[0], empty_cell[1]   # vytáhněme souřadnice prázdné buňky c
            row, col = set(), set()             # set čísel obsažených v řádku c a sloupci c
            
            for i in range(9):         # projdi čísla na daném řádku/sloupci c a každé číslo vlož do setu (právě jednou)
                row.add(grid[x_o][i])   
                col.add(grid[i][y_o])
                        
            rest = (sector_opt.difference(row)).difference(col)    # zbytek možností = možnosti sektoru - čísla obsažená v řádku a sloupci  
                                                                   # proto je to set()... jednoduchá metoda difference()          

            if len(rest) == 1:           # pokud nám zbyde jen jedna možnost
                n_o = rest.pop()
                if possible(grid, x_o, y_o, n_o):  # pokud lze tuto možnost dosadit do tabulky
                    grid[x_o][y_o] = n_o           # vložme ji
                    impl.append((x_o, y_o, n_o))   # a přidejme do seznamu implikací
    return impl


def unimplicate(grid, impl):  
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

        grid1_sol = [[5, 3, 4, 6, 7, 8, 9, 1, 2], [6, 7, 2, 1, 9, 5, 3, 4, 8], [1, 9, 8, 3, 4, 2, 5, 6, 7], [8, 5, 9, 7, 6, 1, 4, 2, 3], [4, 2, 6, 8, 5, 3, 7, 9, 1], [7, 1, 3, 9, 2, 4, 8, 5, 6], [9, 6, 1, 5, 3, 7, 2, 8, 4], [2, 8, 7, 4, 1, 9, 6, 3, 5], [3, 4, 5, 2, 8, 6, 1, 7, 9]]

        grid2 = [[5,1,7,6,0,0,0,3,4],
                 [2,8,9,0,0,4,0,0,0],
                 [3,4,6,2,0,5,0,9,0],
                 [6,0,2,0,0,0,0,1,0],
                 [0,3,8,0,0,6,0,4,7],
                 [0,0,0,0,0,0,0,0,0],
                 [0,9,0,0,0,0,0,7,8],
                 [7,0,3,4,0,0,5,6,0],
                 [0,0,0,0,0,0,0,0,0]]

        grid2_sol = [[5, 1, 7, 6, 9, 8, 2, 3, 4], [2, 8, 9, 1, 3, 4, 7, 5, 6], [3, 4, 6, 2, 7, 5, 8, 9, 1], [6, 7, 2, 8, 4, 9, 3, 1, 5], [1, 3, 8, 5, 2, 6, 9, 4, 7], [9, 5, 4, 7, 1, 3, 6, 8, 2], [4, 9, 5, 3, 6, 2, 1, 7, 8], [7, 2, 3, 4, 8, 1, 5, 6, 9], [8, 6, 1, 9, 5, 7, 4, 2, 3]]

        grid3 = [[5,1,7,6,0,0,0,3,4],
                 [0,8,9,0,0,4,0,0,0],
                 [3,0,6,2,0,5,0,9,0],
                 [6,0,0,0,0,0,0,1,0],
                 [0,3,0,0,0,6,0,4,7],
                 [0,0,0,0,0,0,0,0,0],
                 [0,9,0,0,0,0,0,7,8],
                 [7,0,3,4,0,0,5,6,0],
                 [0,0,0,0,0,0,0,0,0]]

        grid3_sol = [[5, 1, 7, 6, 9, 8, 2, 3, 4], [2, 8, 9, 1, 3, 4, 7, 5, 6], [3, 4, 6, 2, 7, 5, 8, 9, 1], [6, 7, 2, 8, 4, 9, 3, 1, 5], [1, 3, 8, 5, 2, 6, 9, 4, 7], [9, 5, 4, 7, 1, 3, 6, 8, 2], [4, 9, 5, 3, 6, 2, 1, 7, 8], [7, 2, 3, 4, 8, 1, 5, 6, 9], [8, 6, 1, 9, 5, 7, 4, 2, 3]]

        grid = grid2
        grid_sol = grid2_sol
        
        backtracks = 0
        start = time.time()
        backtrack_impl(grid)
        end = time.time() 
                

        print_grid(grid)
        print("Number of backtracks: " + str(backtracks))
        print(end-start)

        print(grid_sol == grid)










