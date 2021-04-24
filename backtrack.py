import time
import random

backtracks = 0
sectors = [[0, 3, 0, 3], [3, 6, 0, 3], [6, 9, 0, 3], 
           [0, 3, 3, 6], [3, 6, 3, 6], [6, 9, 3, 6], 
           [0, 3, 6, 9], [3, 6, 6, 9], [6, 9, 6, 9]]


def solve(grid, method):
    '''
    Metoda zavolá příslušnou řešící metodu, která je určena vstupem.
    '''
    if method == "1":
        backtrack(grid)
    elif method == "2":
        backtrack_reverse(grid)
    elif method == "3":
        backtrack_impl(grid)
    elif method == "4":
        backtrack_forward_checking(grid)
    return backtracks


# ***************************************************************** Backtrack

def backtrack(grid, x0 = 0, y0 = 0):
    '''
    Základní metoda backtrack. Na principu brute force vyplňuje buňky, dokud 
    nenarazí na kolizi. V takovém případě se vrátí o krok zpátky a napíše do 
    buňky jiné číslo (o jedna vyšší).
    '''
    global backtracks
    x, y = nextEmptyCell(grid, x0) # souřadnice následující prázdné buňky
    if x == -1:        # pokud nebyla nalezena prázdná buňka, končíme
        return True
    for n in range(1, 10):  # do prázdné buňky se pokoušíme postupně zapsat čísla od 1 do 9
        if possible(grid, x, y, n):  # ověříme, jestli lze hodnotu n do buňky zapsat (na základě hodnot zapsaných v mřížce)
            grid[x][y] = n       # můžeme-li zapsat, zapíšeme
            if backtrack(grid, x, y):   # a metodu opakujeme - rekurze
                return True            
            grid[x][y] = 0  # pokud některá backtrack metoda vrátí false, vymažeme poslední přiřazenou hodnotu na [x,y]
            backtracks += 1  # počítadlo backtracků         
    return False


# ***************************************************************** Reverzní backtrack

def backtrack_reverse(grid, x0 = 8, y0 = 8):
    '''
    Drobná variace původní backtrack. Buňky nevyplňuje od počátku, nýbrž od konce.
    Vyplatí se, když je v druhé polovině mřížky více hodnot než v první.
    '''
    global backtracks
    x, y = nextEmptyCell_reverse(grid, x0) # zde je rozdíl oproti obyčejnému bactracku
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
    '''
    Metoda backtrack, kde při každém vyplnění buňky zkontrolujeme, jestli se nám 
    tímto přiřazením nezredukovaly možnosti v nějaké jiné buňce na pouze jednu 
    možnost. V takovém případě tuto možnost také zapíšeme. Kontrola těchto možností
    probíhá na řádku, sloupci a v sektoru, kde došlo k vyplnění původní hodnoty.
    '''
    global backtracks
    x, y = nextEmptyCell(grid, x0)
    if x == -1:
        return True
    for n in range(1, 10):
        if possible(grid, x, y, n):            
            impl = implicate(grid, x, y, n) # načteme všechny možné implikace
            if backtrack_impl(grid, x, y):
                return True
            unimplicate(grid, impl)  # pokud vracíme, smažeme všechny implikace, ne jen [x,y] = n
            backtracks += 1  
    return False


# ***************************************************************** Backtrack s dopřednou kontrolou a MRV (minimal remaining values)

def backtrack_forward_checking(grid):
    '''
    Metoda backtrack, kde před vyplněním buňky kontrolujeme i to, jestli nekoliduje
    s nějakým potenciálním vyplněním buňky v budoucnu. Tuto kontrolu provádí metoda 
    forward_check() - zkontroluje, jestli v listu zbývajících možností buněk, které 
    na stejném řádku, sloupci nebo v sektoru, není některá možnost jen jedna - to by
    znamenalo kolizi v budoucnu a rovnou tuto možnost zamítneme.
    Dále zde nejdeme postupně od první buňky, nýbrž jdeme vždy do té buňky, kde je 
    nejméně možností (MRV). Ideální je stav, kdy najdeme vždy takovou buňku, kde je
    jen jedna možnost - v takovém případě bude počet vrácení (backtracků) nulový.
    '''
    global backtracks
           
    remaining_values = get_remaining_values(grid) # list listů možností pro každou buňku v mřížce

    if remaining_values.count([0]) == len(remaining_values):  # pokud již žádné možnosti nejsou, končíme
        return True

    x, y, values = get_MRV(remaining_values)   # souřadnice buňky, kde je nejméně zbylých možností, values - zbylé možnosti 
    
    for n in values:   # projdeme všechny možnosti v buňce [x,y]
        if forward_check(x, y, n, remaining_values):  # kontrola forward_check()
            grid[x][y] = n
            if backtrack_forward_checking(grid):
                return True
            grid[x][y] = 0
            backtracks += 1
    return False



# ***************************************************************** Základní pomocné metody

def nextEmptyCell(grid, x0):
    '''
    Vrátí souřadnice další prázdné buňky od rádku x0.
    '''
    for x in range(x0, 9):
        for y in range(9):
            if grid[x][y] == 0:
                return x, y
    return -1, -1

def nextEmptyCell_reverse(grid, x0):
    '''
    Vrátí souřadnice předchozí prázdné buňky od konce (od řádku x0).
    '''
    for x in range(x0,-1,-1):
        for y in range(8,-1,-1):
            if grid[x][y] == 0:
                return x, y
    return -1, -1

def possible (grid, x, y, n):
    '''
    Zjistí, zda může být n na pozici [x,y].
    '''
    for i in range (9):
        if grid[x][i] == n:
            return False
    for i in range (9):
        if grid[i][y] == n:
            return False
    
    x0 = (x//3)*3 # nastavení počáteční souřadnice sektoru, ve kterém je [x,y]
    y0 = (y//3)*3
    for i in range (3):
        for j in range (3):
            if grid[x0+i][y0+j] == n:
                return False
    return True        


# ***************************************************************** Pomocné metody pro implikaci

def implicate(grid, x, y, n):
    '''
    Vloží do mřížky všechny implikovatelné hodnoty a vrátí list provedených implikací.
    '''
    global sectors
    grid[x][y] = n
    impl = [(x, y, n)]  # list implikací
                        # krom samotného dosazení [x,y] = n bude obsahovat i další možná dosazení v každém sektoru
                        # zjistíme následujícím algoritmem
    
    for s in sectors:
        empty_cells = []                 # list prázdných buněk v daném sektoru
        sector_opt = {1, 2, 3, 4, 5, 6, 7, 8, 9}   # set chybějících čísel v daném sektoru - možnosti sektoru
        
        for i in range(s[0], s[1]):     # pro všechny prvky sektoru
            for j in range(s[2], s[3]):
                if grid[i][j] != 0:
                    sector_opt.remove(grid[i][j])  # souřadnice nenulové hodnoty vymaž ze setu možností
                else:
                    empty_cells.append([i, j])   # souřadnice nulové hodnoty přidej do listu prázdných buněk
            
        for c in empty_cells:
            x0, y0 = c                  # vytáhněme souřadnice prázdné buňky c
            row, col = set(), set()       # set čísel obsažených v řádku c a sloupci c
            
            for i in range(9):         # projdi čísla na daném řádku/sloupci c a každé číslo vlož do setu
                row.add(grid[x0][i])    # jsou to sety, tedy se tam žádná hodnota nebude opakovat
                col.add(grid[i][y0])
                        
            rest = (sector_opt.difference(row)).difference(col)    # zbytek možností = možnosti sektoru - čísla obsažená v řádku a sloupci      

            if len(rest) == 1:           # pokud nám zbyde jen jedna možnost
                n0 = rest.pop()
                if possible(grid, x0, y0, n0):  # pokud lze tuto možnost dosadit do mřížky
                    grid[x0][y0] = n0           # vložme ji
                    impl.append((x0, y0, n0))   # a přidejme do listu implikací
    return impl

def unimplicate(grid, impl):  
    '''
    Vrátí všechny implikace - vloží nulu tam, kde byly dosazeny nějaké hodnoty v posledním kroku.
    '''
    for i in range(len(impl)):
        grid[impl[i][0]][impl[i][1]] = 0


# ***************************************************************** Pomocné metody pro Forward checking a MRV

def get_remaining_values(grid):
    '''
    Vrátí list možností pro každou z 81 buněk.
    '''
    remaining_values = []    # seznam možností - pořadí v listu určuje souřadnice, list na této pozici jsou možnosti v buňce
    [remaining_values.append([*range(1,10)]) for i in range(81)]        
    for x in range(len(grid)):
        for y in range(len(grid)):
            if grid[x][y] != 0:                
                remaining_values = remove_values(x, y, grid[x][y], remaining_values)  # vymaž tuto hodnotu z příslušných možností
    return remaining_values

def remove_values(x, y, n, remaining_values):
    '''
    Vymaže z listu zbylých možností hodnoty, které již nejsou možnostmi (kvůli nové hodnotě n).
    '''        
    remaining_values[y+x*9] = [0]  # na pozici [x,y] již je n - proto tam nemůže být nic jiného
    
    # následující 3 cykly vymažou hodnotu n z možností na řádku x, sloupci y a v sektoru, kde se nachází [x,y]
    for i in remaining_values[x*9 : x*9 + 9]:  # projde všechny sloupce řádku x        
        if n in i:
            i.remove(n)            
    
    for i in range(9):        # projde všechny řádky sloupce y
        if n in remaining_values[y+9*i]:
            remaining_values[y+9*i].remove(n)        
    
    x0 = (x//3)*3
    y0 = (y//3)*3
    for i in range(3):       # projde všechny prvky v daném sektoru
        for j in range(3):
            if n in remaining_values[(x0 + i)*9 + y0 + j]:
                remaining_values[(x0 + i)*9 + y0 + j].remove(n)

    return remaining_values

def get_MRV(remaining_values):
    '''
    Najde buňku, kde je nejméně zbylých možností a vrátí souřadnice této buňky a v ní zbylé možnosti.
    '''
    non_zero = []
    for i in remaining_values:
        if i != [0]:
            if len(i) == 1:  # pokud najdeme buňku, kde je jen jedna možnost, rovnou ji vracíme
                return [remaining_values.index(i) //9, remaining_values.index(i) %9, i]
            non_zero.append(i)
    mrv = min(non_zero, key=len)  # pokud nenajdeme buňku, kde je jen jedna možnost, vrátíme tu, kde je možností nejméně
    return [remaining_values.index(mrv) //9, remaining_values.index(mrv) %9, mrv]

def forward_check(x, y, n, remaining_values):    
    '''
    Zkontroluje, jestli vložená hodnota n na [x,y] nekoliduje s nějakou jinou, ještě nevloženou 
    hodnotou - tak, že projde všechny zbývající možnosti na řádku, sloupci a v sektoru a zkontroluje, 
    zda někde nezbývá jen jedna možnost, která by byla právě n. V takovém případě vrací False.
    '''
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
    for i in range(3):    # projde všechny prvky v sektoru, kde je [x,y]
        for j in range(3):            
            if [x0+i, y0+j] == [x, y]:
                continue            
            r = remaining_values[(x0 + i)*9 + y0 + j]
            if len(r) == 1 and r[0] == n:
                return False
    return True