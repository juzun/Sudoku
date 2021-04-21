from itertools import product
import numpy as np

def exact_cover(X, Y):
    X = {j: set() for j in X}
    for i, row in Y.items():
        for j in row:
            X[j].add(i)
    return X, Y

def solve(X,Y,solution=[]):  
    if not X:   # je-li zadaný slovník prázdný, "máme" hned řešení
        yield list(solution) 
    else:
        c = min(X, key=lambda c: len(X[c])) # najdi sloupec s minimálním počtem jedniček
        
        for r in list(X[c]):  # iteruju přes všechna písmena ve slovníku X na řádku c
            solution.append(r) # r-tý řádek přídaný do řešení 
            cols = select(X, Y, r) # potřebuju najít jedničkové sloupce z tohoto řádku
            for s in solve(X, Y, solution): # rekurze
                yield s
            # deselect(X, Y, r, cols)   # pro případ více řešení (smaže aktuální, hledá další) 
            # solution.pop()

def select(X, Y, r):
    
    cols = [] # záloha vymazaných možností z X
    for j in Y[r]: # j jsou čísla v řádku(písmenu) r  (1,4,7) 
        for i in X[j]: # přes všechna písmena i v řádku (čísle) j (pro j=1 je to A,B)
            for k in Y[i]: # opět 1,4,7
                if k != j:
                    X[k].remove(i) # odstranuju A,B,C,E,F 
        cols.append(X.pop(j))  
    return cols


def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)



def solve_sudoku(size, grid):
    R, C = size
    N = R * C  # počet pmožných čísel
    X = ([("rc", rc) for rc in product(range(N), range(N))] +   # čísla n až od 1, sloupce a řádky od 0
         [("rn", rn) for rn in product(range(N), range(1, N + 1))] +
         [("cn", cn) for cn in product(range(N), range(1, N + 1))] +
         [("bn", bn) for bn in product(range(N), range(1, N + 1))])
    # X prostě vektor 
    
    Y = dict()
    for r, c, n in product(range(N), range(N), range(1, N + 1)):  # všechny řádky v tabulce - také jen hlavičky R1C1#1 apod.
        b = (r // R) * R + (c // C) # Box number
        Y[(r, c, n)] = [
            ("rc", (r, c)),
            ("rn", (r, n)),
            ("cn", (c, n)),
            ("bn", (b, n))]
    
    
    X, Y = exact_cover(X, Y) # nX se předělá na dictionary
   
    for i, row in enumerate(grid):
        for j, n in enumerate(row):
            if n: # if n>0 ??
                select(X, Y, (i, j, n)) # pouze promazáváme možnosti v X 
    

    for solution in solve(X, Y, []):  # hlavní řešič ... solutions může být vice
        
        for (r, c, n) in solution:  # vypsání výsledného sudoku
            grid[r][c] = n
        yield grid


if __name__ == "__main__":
    grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0], 
        [6, 0, 0, 1, 9, 5, 0, 0, 0], 
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3], 
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]]
    grid_mala = [
        [0,3,4,0],
        [4,0,0,2],
        [1,0,0,3],
        [0,2,1,0]]
    

    for solution in solve_sudoku((3, 3), grid):
        print(*solution, sep='\n')
    

   