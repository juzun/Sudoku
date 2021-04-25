import time

class Node:  # každá nová mřížka reprezentuje stav - uzel staového prostoru
    def __init__(self, grid):
        self.grid = grid  # mřížka tohoto příslušného stavu

    def setGrid(self, empty_cell, new_val): # při inicializaci nové instance třídy upravím předchozí mřížku změnou jedné hodnoty
        self.grid[empty_cell[0]][empty_cell[1]] = new_val 

    def getCandidates(self):  # vrací nové mřížky po doplnění jednoho čísla do bunky
        ans = list() # bude to list objektů typu 
        empty_cell = self.getMostConstrainedCell() 
        possible_values = self.getPossibilitiesForCell(empty_cell[0], empty_cell[1])  # nalezené těchto možností

        for k in range(0,len(possible_values)):
            n = Node(self.grid)
            n.setGrid(empty_cell, possible_values[k])
            ans.append(n)
        return ans

    def isSolved(self):  # kontrola, zda již máme vyřešené sudoku
        for r in range(0,9):
            for c in range(0,9):
                if self.grid[r][c] == 0:
                    return False
        print("Sudoku vyřešeno")
        return True

    def getMostConstrainedCell(self):  # najdeme prázdnou buňku s nejméně možnostmi na doplnění
        number_possibilities = [[0]*9]*9
        min_r = -1
        min_c = -1

        for r in range(0,9):
            for c in range(0,9): 
                if self.grid[r][c] == 0:
                    min_r=r   # najdu první prazdnou bunku
                    min_c=c
                    for r in range(0,9):  # znova prohledávám celou mřížku a hledám jinou pázdnou bunku
                        for c in range(0,9):
                            if (self.grid[r][c] != 0): 
                                continue
                            else:  
                                number_possibilities[r][c] = self.getNumPossibilitiesForCell(r,c) # pro každou prázndou bunku najdu počet možností
                                if (number_possibilities[r][c] == 1): # pokud jsem narazil na nějakou s jedinou možností, tak pracuji s ní
                                    return r,c
                                if (number_possibilities[r][c] < number_possibilities[min_r][min_c]): # pokud jsem narazil na nějkou s menším počtem možností než tá původní vybraná, tak pracuj s touhle
                                    min_r = r
                                    min_c = c
                    return min_r, min_c  # vracím souřednice buňky, která ma nejmenší počet možných doplnění

    def getNumPossibilitiesForCell(self,r,c):   # vrátí počet možností pro bunku o souřadnicích r,c

        used = [False] * 9
        r_t = 0
        c_t = 0

        for k in range(0,9):
            if self.grid[r][k] != 0:
                used[self.grid[r][k]-1] = True
            if self.grid[k][c] != 0:
                used[self.grid[k][c]-1] = True

            r_t = int((r - r%3) + k/3)
            c_t = int((c - c%3) + k%3)
    
            if (self.grid[r_t][c_t] != 0):
                used[self.grid[r_t][c_t]-1] = True
    
        number = 9 # pocet možnosti
        for k in range(0,9):
            if used[k]:
                number = number - 1
    
        return number
    
    def getPossibilitiesForCell(self,r,c):  # vrátí už přímo konkrétní čísla, která je možno doplnit
        possibilities = []

        used = [False] * 9
        r_t = 0
        c_t = 0

        for k in range(0,9):
            if self.grid[r][k] != 0:
                used[self.grid[r][k]-1] = True
            if self.grid[k][c] != 0:
                used[self.grid[k][c]-1] = True

            r_t = int((r - r%3) + k/3)
            c_t = int((c - c%3) + k%3)

            if (self.grid[r_t][c_t] != 0):
                used[self.grid[r_t][c_t]-1] = True

        for k in range(0,9):
            if used[k]!=True:
                possibilities.append(k+1)
        return possibilities

    def printNode(self): # tisk
        for i in range(9):
            if i==0:
                print("┌───────┬───────┬───────┐")
            if i==3 or i==6:
                print("├───────┼───────┼───────┤")
            print("│ {} {} {} │ {} {} {} │ {} {} {} │".format(*self.grid[i]))
            if i==8:
                print("└───────┴───────┴───────┘")
    


def bestfirstsearch(grid):  
    n = Node(grid)  # inicializace třídy
    solve(n)   # solver

def solve(n): # rekurze
    if n.isSolved():  
        n.printNode()
        return True
        
    candidates = n.getCandidates() 

    for k in range(0,len(candidates)): # uvažuji všechny nové mřížky které vznikly změnou hodnoty jedné buňky
        if solve(candidates[k]): # rekurze
            return True
    
    return False

if __name__=="__main__":
    grid =[[5,3,0,0,7,0,0,0,0],
            [6,0,0,1,9,5,0,0,0],
            [0,9,8,0,0,0,0,6,0],
            [8,0,0,0,6,0,0,0,3],
            [4,0,0,8,0,3,0,0,1],
            [7,0,0,0,2,0,0,0,6],
            [0,6,0,0,0,0,2,8,0],
            [0,0,0,4,1,9,0,0,5],
            [0,0,0,0,8,0,0,7,9]]
    
    t1=time.time()
    bestfirstsearch(grid) # spousteci metoda
    t2=time.time()

    print("time: ",t2-t1, "s")
    