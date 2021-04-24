import time
import random


def backtrack_forward_checking(grid):
    #global backtracks
           
    remaining_values = get_remaining_values(grid) # list listů možností pro každou buňku

    if remaining_values.count([0]) == len(remaining_values):
        print_grid(grid)
        return True

    x, y, values = get_least(remaining_values)   # souřadnice buňky, kde je nejméně zbylých možností, values - zbylé možnosti 
    
    for n in values:
        if forward_check(x, y, n, remaining_values):
            grid[x][y] = n
            if backtrack_forward_checking(grid):
                return True
            grid[x][y] = 0
            #backtracks += 1
    return False


# vrátí souřadnice buňky a v ní zbylé možnosti, kde je zbylých možností nejméně
def get_least(remaining_values):
    non_zero = []
    for i in remaining_values:
        if i != [0]:
            if len(i) == 1:
                return [remaining_values.index(i) //9, remaining_values.index(i) %9, i]
            non_zero.append(i)
    rem = min(non_zero, key=len)
    return [remaining_values.index(rem) //9, remaining_values.index(rem) %9, rem]


# vrátí list možností pro každou z 81 buněk
def get_remaining_values(grid):
    remaining_values = []    # seznam možností -  pořadí v listu určuje souřadnice, list na této pozici jsou možnosti v buňce
    [remaining_values.append([*range(1,10)]) for i in range(81)]    
    for x in range(len(grid)):
        for y in range(len(grid[1])):
            if grid[x][y] != 0:
                n = grid[x][y]  
                remaining_values = remove_values(x, y, n, remaining_values)                
    return remaining_values  

# vymaže z listu zbylých možností hodnoty, které již nejsou možnostmi (kvůli nové hodnotě n)
def remove_values(x, y, n, remaining_values):
        
    remaining_values[y+x*9] = [0]  # na pozici [x,y] již je n - proto tam nemůže být nic jiného
    
    # následující 3 cykly vymažou hodnotu n z možností na řádku x, sloupci y a v bloku, kde se nachází [x,y]
    for i in remaining_values[x*9 : x*9 + 9]:  # projde všechny sloupce řádku x        
        if n in i:
            i.remove(n)
            
    for i in range(9):        # projde všechny řádky sloupce y
        if n in remaining_values[y+9*i]:
            remaining_values[y+9*i].remove(n)
        
    x0 = (x//3)*3
    y0 = (y//3)*3
    for i in range(3):       # projde všechny prvky v daném bloku
        for j in range(3):
            if n in remaining_values[(x0 + i)*9 + y0 + j]:
                remaining_values[(x0 + i)*9 + y0 + j].remove(n)

    return remaining_values


# Zkontroluje, jestli vložená hodnota n na [x,y] nekoliduje s nějakou jinou, ještě nevloženou hodnotou
# Tak, že projde všechny zbývající možnosti na řádku, sloupci a v bloku a zkontroluje, 
# zda někde nezbývá jen jedna možnost, která by byla právě n. V takovém případě vrací False.
def forward_check(x, y, n, remaining_values):    

    for i in range(9):      # projde všechny sloupce v řádku x
        if i == y:
            continue            
        r = remaining_values[x*9+i]  # zbylé možnosti pro buňku [x,i]                
        if len(r) == 1 and r[0] == n:  # pokud obsahuje r jen jeden prvek a tento prvek je n
            return False
     
    for i in range(9):       # projde všechny řádky ve sloupci y
        if i == x:
            continue            
        r = remaining_values[9*i+y]   # zbylé možnosti pro buňku [i,y]
        if len(r) == 1 and r[0] == n:
            return False

    x0 = (x//3)*3
    y0 = (y//3)*3  
    for i in range(3):
        for j in range(3):            
            if [x0+i, y0+j] == [x, y]:
                continue            
            r = remaining_values[(x0 + i)*9 + y0 + j]
            if len(r) == 1 and r[0] == n:
                return False
    return True



# ***************************************************************** Backtrack

def backtrack(grid, x0 = 0, y0 = 0):
    #global backtracks
    x, y = nextEmptyCell(grid, x0, y0)
    if x == -1:   # pokud nebyla nalezena prázdná buňka
        return True
    for n in range(1, 10):
        if possible(grid, x, y, n):
            grid[x][y] = n
            if backtrack(grid, x, y):
                return True            
            #backtracks += 1
            grid[x][y] = 0    
    return False


# ***************************************************************** Reverzní backtrack

def backtrack_reverse(grid, x0 = 8, y0 = 8):
    #global backtracks
    x, y = nextEmptyCell_reverse(grid, x0, y0)
    if x == -1:
        return True
    for n in range(1, 10):
        if possible(grid, x, y, n):
            grid[x][y] = n
            if backtrack_reverse(grid, x, y):
                return True            
            #backtracks += 1
            grid[x][y] = 0        
    return False


# ***************************************************************** Backtrack s implikacemi

def backtrack_impl(grid, x0 = 0, y0 = 0):
    #global backtracks
    x, y = nextEmptyCell(grid, x0, y0)
    if x == -1:
        return True
    for n in range(1, 10):
        if possible(grid, x, y, n):            
            impl = implicate(grid, x, y, n)
            if backtrack_impl(grid, x, y):
                return True
            unimplicate(grid, impl)  # pokud se musíme vrátit, musíme smazat všechny implikace, ne jen [x,y] = n, proto posíláme impl na vstup a výstup
            #backtracks += 1  
    return False





# ***************************************************************** Pomocné metody


def print_grid(grid):  # vykreslení mřížky
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


def possible (grid, x, y, n):  # zjistí, zda může být n na pozici [x,y]
    for i in range (9):
        if grid[x][i] == n:
            return False
    for i in range (9):
        if grid[i][y] == n:
            return False
    
    x0 = (x//3)*3 # nastavíme počáteční souřadnice sektoru, ve kterém je [x,y]
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



sectors = [[0, 3, 0, 3], [3, 6, 0, 3], [6, 9, 0, 3], 
           [0, 3, 3, 6], [3, 6, 3, 6], [6, 9, 3, 6], 
           [0, 3, 6, 9], [3, 6, 6, 9], [6, 9, 6, 9]]

def implicate(grid, x, y, n):
    global sectors
    grid[x][y] = n
    impl = [(x, y, n)]  # list implikací - krom samotného dosazení [x,y] = n bude obsahovat i další možná dosazení v každém sektoru za použití následujícího algoritmu
    
    for s in range(len(sectors)):
        empty_cells = []                 # list prázdných buněk v daném sektoru
        sector_opt = {1, 2, 3, 4, 5, 6, 7, 8, 9}   # set chybějících čísel v daném sektoru - možnosti sektoru
        
        for i in range(sectors[s][0], sectors[s][1]):     # pro všechny prvky sektoru
            for j in range(sectors[s][2], sectors[s][3]):
                if grid[i][j] != 0:
                    sector_opt.remove(grid[i][j])  # souřadnice nenulové hodnoty vymaž ze setu možností
                else:
                    empty_cells.append([i, j])   # souřadnice nulové hodnoty přidej do listu prázdných buněk
            
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
                    impl.append((x_o, y_o, n_o))   # a přidejme do listu implikací
    return impl


def unimplicate(grid, impl):  
    for i in range(len(impl)):
        grid[impl[i][0]][impl[i][1]] = 0





if __name__ == '__main__':

        grid1 = [[5,3,1,0,7,0,0,0,0],
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




        grid = grid3
        grid_sol = grid3_sol
        
        backtracks = 0

        start = time.time()
        backtrack_forward_checking(grid)
        end = time.time() 
                

        print_grid(grid)
        print("Number of backtracks: " + str(backtracks))
        print(end-start)

        print(grid_sol == grid)

