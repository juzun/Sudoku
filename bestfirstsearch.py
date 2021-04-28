from copy import deepcopy

def solve(grid):
    '''
    Metoda spustí řešič a vrátí výslednou mřížku.
    '''
    solve_sudoku(grid)
    return promenna


def solve_sudoku(grid):
    '''
    Řešič funguje na principu best-first search, kdy nejlepší volbou v každé iteraci 
    je najít a vyplnit buňku s nejméně možnostmi. Metoda getCandidates() vrací list mřížek, 
    kde každá se liší zvolenou přípustnou možností ve vybrané buňce. 
    Metoda pak zkontroluje každou možnost v listu, dokud nenarazí na řešení.
    '''
    if isSolved(grid):
        global promenna  # zde uchováváme výsledek
        promenna = grid
        return True
        
    candidates = getCandidates(grid)

    for k in range(0,len(candidates)):
        if solve_sudoku(candidates[k]):
            return True
    
    return False


def isSolved(grid):  
    '''
    Řešič se ukončí, pokud v mřížce nezbývá žádná volná buňka.  
    '''
    for r in range(0,9):
        for c in range(0,9):
            if grid[r][c] == 0:
                return False
    return True


def getCandidates(grid):
    '''
    Metoda nalezne buňku (empty_cell) s nejvíce omezeními (nejméně možnostmi na doplnění)
    pomocí metody getMostConstrainedCell() a dále hodnoty, které je možné doplnit pomocí 
    metody getPossibilitiesForCell(). Nakonec vrátí všechny nově vygenerované mřížky.
    '''
    choices = list()  # list mřížek
    empty_cell = getMostConstrainedCell(grid) 
    possible_values = getPossibilitiesForCell(grid, empty_cell[0], empty_cell[1])

    for k in range(0,len(possible_values)):
        setGrid(grid, empty_cell, possible_values[k]) 
        grid2 = deepcopy(grid)
        choices.append(grid2)
    return choices


def getMostConstrainedCell(grid):
    '''
    Nejdříve se nalezne první prázdná buňka, dále pak hledáme další prázdné buňky 
    a porovnáme počet přípustných možností těchto buněk s počtem přípustných možností té první vybrané buňky.
    Pokud jsme našli buňku s menším počtem možností, uložíme její souřadnice.
    ''' 
    number_possibilities = [[0]*9]*9  # mřížka nul
    min_r = -1  # souřadnice prázdné buňky
    min_c = -1

    for r in range(0,9):
        for c in range(0,9):
            if grid[r][c] == 0:
                min_r=r
                min_c=c
                for r in range(0,9):
                    for c in range(0,9):
                        if (grid[r][c] != 0):
                            continue
                        else:
                            number_possibilities[r][c] = getNumberPossibilitiesForCell(grid,r,c)
                            if (number_possibilities[r][c] == 1):
                                return r,c
                            if (number_possibilities[r][c] < number_possibilities[min_r][min_c]):
                                min_r = r
                                min_c = c
    return min_r, min_c # vracím souřadnice buňky s nejmenším počtem přípustných možností


def getNumberPossibilitiesForCell(grid,r,c): 
    '''
    Metoda zjišťuje, která čísla se již nachází v řádku, sloupci a bloku odpovídajícím buňce [r,c].
    Podle toho pak odpočítává počet možných doplnění pro tuto buňku (počet hodnot False ve vektoru used).
    Tento počet možností pak vrátí.
    '''
    used = [False] * 9 
    # False na dané číselné pozici znamená, že toto číslo nemohu zapast na pozici [r,c] v mžížce 
    r_t = 0
    c_t = 0

    for k in range(0,9):
        if grid[r][k] != 0:  # kontrola řádku
            used[grid[r][k]-1] = True  
        if grid[k][c] != 0:  # kontrola sloupců
            used[grid[k][c]-1] = True

        r_t = int((r - r%3) + k/3)  
        c_t = int((c - c%3) + k%3)
       
        if (grid[r_t][c_t] != 0):  # kontrola bloků
            used[grid[r_t][c_t]-1] = True
    
    number = 9
    for k in range(0,9):
        if used[k]:
            number = number - 1
    
    return number 

def getPossibilitiesForCell(grid, r, c): 
    '''
    Metoda je velmi podobná metodě getNumberPossibilitiesForCell(), nevrací však počet možností, 
    ale přímo vektor možností. Ač jsou metody podobné, bylo vhodnější je nechat odděleně.
    '''
    possibilities = [] # vektor možností
    if grid[r][c] != 0:
        return possibilities 

    used = [False] * 9
    r_t = 0
    c_t = 0

    for k in range(0,9):
        if grid[r][k] != 0:
            used[grid[r][k]-1] = True
        if grid[k][c] != 0:
            used[grid[k][c]-1] = True

        r_t = int((r - r%3) + k/3)
        c_t = int((c - c%3) + k%3)

        if (grid[r_t][c_t] != 0):
            used[grid[r_t][c_t]-1] = True

    for k in range(0,9):
        if used[k]!=True:
            possibilities.append(k+1)
    return possibilities


def setGrid(grid, empty_cell, new_value): 
    '''
    Aktualizace mřížky novou možností (new_value) pro zvolenou prázdnou buňku (empty_cell).  
    '''
    grid[empty_cell[0]][empty_cell[1]] = new_value


    
