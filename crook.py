from copy import deepcopy
import time

def create_possibles(grid, possibles):
    for i in range(9):
        for j in range(9):
            possibles[i,j]=[p for p in possibles[i,j] if p not in grid[i]]
            possibles[i,j]=[p for p in possibles[i,j] if p not in [s[j] for s in grid]]

    for a in [0,3,6]:
        for b in [0,3,6]:
            square=[r[b:b+3] for r in grid[a:a+3]]
            square=[item for sublist in square for item in sublist] # sjednoceni listu ve square
            for i in range(3):
                for j in range(3):
                    possibles[a+i, b+j]=[p for p in possibles[a+i, b+j] if p not in square]

def update_possibles(grid, possibles, x,y):
    """
    vymaže hodnotu grid[x][y] z přípustnách hodnot 
    v řádku x, 
    v sloupci y,
    ve čtverci, ve kterém je x,y

    vymaže všechny přípustné hodoty v x,y
    """

    # kontrola řádků a sloupců
    for i in range(9):
        possibles[x,i]=[ p for p in  possibles[x,i] if p!=grid[x][y] ]
        possibles[i,y]=[ p for p in possibles[i,y] if p!=grid[x][y] ]
    
    # kontrola boxu
    x0 = (x//3)*3
    y0 = (y//3)*3
    for i in range(3):
        for j in range(3):
            possibles[x0+i,y0+j]=[p for p in possibles[x0+i,y0+j] if p!=grid[x][y]]

    # vynulování přípistnách donot v x,y
    possibles[x,y]=list()

def fill_only_one_possible(grid, possibles):
    """
    Dosadí hodnotu do políček, do kterých jde dosadit jen jedno číslo
    """
    
    while(True):
        last=deepcopy(grid)
        ones={key: val for key, val in possibles.items() if len(val)==1}
        for key, val in ones.items():
            grid[key[0]][key[1]]=val[0]
            update_possibles(grid, possibles, key[0],key[1])
        if last==grid:
            break

def check_row(grid, possibles):
    """
    Zkontroluje, jestli v některém řádku není číslo, 
    které může být jen v jednom políčku daného řádku.
    Pokud takové číslo je, dosadí ho
    """
    for i in range(9):
        row_possibles=[value for key, value in possibles.items() if key[0] == i and len(value) > 0]
        pe = [x for y in row_possibles for x in y] 

        row_uniques=[x for x in pe if pe.count(x)==1]
        if len(row_uniques)>0:
            for element in row_uniques:
                keys=[key for key, value in possibles.items() if key[0]==i and element in value]
                grid[keys[0][0]][keys[0][1]]=element
                update_possibles(grid, possibles, keys[0][0],keys[0][1])

def check_col(grid, possibles):
    """
    Zkontroluje, jestli v některém sloupci není číslo, 
    které může být jen v jednom políčku daného sloupce.
    Pokud takové číslo je, dosadí ho
    """
    for i in range(9):
        col_possibles=[value for key, value in possibles.items() if key[1] == i and len(value) > 0]
        pe = [x for y in col_possibles for x in y] 
        
        col_uniques=[x for x in pe if pe.count(x)==1]
        if len(col_uniques)>0:
            for element in col_uniques:
                keys=[key for key, value in possibles.items() if key[1]==i and element in value]
                grid[keys[0][0]][keys[0][1]]=element
                update_possibles(grid, possibles, keys[0][0],keys[0][1])

    
def check_box(grid, possibles):
    """
    Zkontroluje, jestli v některém boxu není číslo, 
    které může být jen v jednom políčku daného boxu.
    Pokud takové číslo je, dosadí ho
    """
    for i in range(3):
        for j in range(3):
            I=list(range(3*i,3*i+3))
            J=list(range(3*j,3*j+3))
            box_possibles=[value for key, value in possibles.items()
                     if key[0] in I and key[1] in J and len(value) > 0]
            pe = [x for b in box_possibles for x in b]

            box_uniques=[x for x in pe if pe.count(x)==1]
            if len(box_uniques)>0:
                for element in box_uniques:
                    keys=[key for key, value in possibles.items() 
                            if key[0] in I and key[1] in J and element in value]
                    grid[keys[0][0]][keys[0][1]]=element
                    update_possibles(grid, possibles, keys[0][0],keys[0][1])

def outside_box(grid, possibles):
    """
    Pokud je v některém boxu nějaké číslo přípustné jen v jednom řádku,
    nebo jen v jednom sloupci, pak nemůže být v tomto řádku nebo sloupci
    mimo daný box. V takovém případě je odebráno z přípustných čísel
    """
    for i in range(3):
        for j in range(3):
            I=list(range(3*i,3*i+3))
            J=list(range(3*j,3*j+3))
            box_possibles=[value for key, value in possibles.items()
                    if key[0] in I and key[1] in J and len(value) > 0]
            pe = set([x for b in box_possibles for x in b])
            
            for n in pe:
                x=[key[0] for key, value in possibles.items() 
                            if key[0] in I and key[1] in J and n in value]
                y=[key[1] for key, value in possibles.items() 
                            if key[0] in I and key[1] in J and n in value]
                
                if len(set(x))==1:
                    for k in range(9):
                        if n in possibles[x[0],k] and k not in J:
                            possibles[x[0],k].remove(n)

                if len(set(y))==1:
                    for k in range(9):
                        if n in possibles[k,y[0]] and k not in I:
                            possibles[k,y[0]].remove(n)
    
def crook_solve(grid, possibles):
    crook_row(grid, possibles)
    crook_col(grid, possibles)
    crook_box(grid, possibles)

def crook_row(grid, possibles):
    for i in range(9):
        segment={key: value for key, value in possibles.items() if key[0]==i and len(value)>0}
        crook(grid, possibles, segment)

def crook_col(grid, possibles):
    for i in range(9):
        segment={key: value for key, value in possibles.items() if key[1]==i and len(value)>0}
        crook(grid, possibles, segment)

def crook_box(grid, possibles):
    for i in range(3):
        for j in range(3):
            I=list(range(3*i,3*i+3))
            J=list(range(3*j,3*j+3))
            segment={key: value for key, value in possibles.items() if key[0] in I and key[1] in J and len(value)>0}
            crook(grid, possibles, segment)

def crook(grid, possibles, segment):
    lengths=[(len(v)) for _, v in segment.items()]
    if lengths:
        min_segment, max_segment = min(lengths), max(lengths)
    else:
        return
    
    for i in range(max_segment, max(min_segment-1,1), -1):
        for _, value in {key: value for key, value in segment.items() 
                                if len(value) == i}.items():
            cnt=0
            pe=list()
            for k2, v2 in segment.items():
                if len(v2)<=i:
                    if set(value).issubset(set(v2)):
                        cnt+=1
                        pe.append(k2)
            if cnt==i:
                for k, _ in segment.items():
                    if k not in pe:
                        possibles[k]=[p for p in possibles[k] if p not in value]


def basic(grid, possibles):
    fill_only_one_possible(grid, possibles)
    check_col(grid, possibles)
    check_row(grid, possibles)
    check_box(grid, possibles)
    outside_box(grid, possibles)
    fill_only_one_possible(grid, possibles)


def prt(table):
    for i in range(9):
        if i==0:
            print("┌───────┬───────┬───────┐")
        if i==3 or i==6:
            print("├───────┼───────┼───────┤")
        print("│ {} {} {} │ {} {} {} │ {} {} {} │".format(*table[i]))
        if i==8:
            print("└───────┴───────┴───────┘")
            
def loop(grid, possibles):
    while(True):
        last=deepcopy(grid)
        basic(grid, possibles)
        crook_solve(grid, possibles)
        if grid==last:
            for x in range(9):
                for y in range(9):
                    if grid[x][y]==0:
                        for n in range(1,10):
                            if n in possibles[x,y]:
                                # vytvoreni bodu navratu, abuchom se meli kam 
                                # vratit, kdyby n nepatrilo na pozici x,y
                                poss=deepcopy(possibles)
                                gr=deepcopy(grid)
                                # zkusime dosadit n do x,y a upravime possibles
                                grid[x][y]=n
                                update_possibles(grid, possibles, x,y)
                                # budeme dal resit pomoci funkce loop, prvne 
                                # klasickymi postupy, pripadne zase backtrackem
                                loop(grid, possibles)
                                # pokud se z backtracku vratime, meli jsme 
                                # spatny predpoklad, ze na pozici x,y je n, 
                                # takze se vratime k bodu navratu a zkousime dal
                                possibles=deepcopy(poss)
                                grid=deepcopy(gr)
                        return
            if grid==last:
                break

def solve(grid):
    possibles=dict()
    for i in range(9):
        for j in range(9):
            possibles[i,j]=range(1,10)
            if grid[i][j]!=0:
                possibles[i,j]=[]
    create_possibles(grid, possibles)
    loop(grid, possibles)

if __name__=="__main__":
    grid1 =[[5,3,0,0,7,0,0,0,0],
            [6,0,0,1,9,5,0,0,0],
            [0,9,8,0,0,0,0,6,0],
            [8,0,0,0,6,0,0,0,3],
            [4,0,0,8,0,3,0,0,1],
            [7,0,0,0,2,0,0,0,6],
            [0,6,0,0,0,0,2,8,0],
            [0,0,0,4,1,9,0,0,5],
            [0,0,0,0,8,0,0,7,9]]

    grid2 =[[5,1,7,6,0,0,0,3,4],
            [2,8,9,0,0,4,0,0,0],
            [3,4,6,2,0,5,0,9,0],
            [6,0,2,0,0,0,0,1,0],
            [0,3,8,0,0,6,0,4,7],
            [0,0,0,0,0,0,0,0,0],
            [0,9,0,0,0,0,0,7,8],
            [7,0,3,4,0,0,5,6,0],
            [0,0,0,0,0,0,0,0,0]]

    grid3 =[[5,1,7,6,0,0,0,3,4],
            [0,8,9,0,0,4,0,0,0],
            [3,0,6,2,0,5,0,9,0],
            [6,0,0,0,0,0,0,1,0],
            [0,3,0,0,0,6,0,4,7],
            [0,0,0,0,0,0,0,0,0],
            [0,9,0,0,0,0,0,7,8],
            [7,0,3,4,0,0,5,6,0],
            [0,0,0,0,0,0,0,0,0]]

    zapeklite=[[8,0,4,2,0,0,3,0,0],
                [0,2,3,0,0,0,8,0,7],
                [0,0,0,0,9,0,0,1,0],
                [7,0,0,0,0,0,0,6,8],
                [0,0,8,0,0,0,9,0,0],
                [9,6,0,0,0,0,0,0,5],
                [0,1,0,0,7,0,0,0,0],
                [5,0,7,0,0,0,6,8,0],
                [0,0,6,0,0,5,2,0,1]]

    s107 = [[2,0,0,1,5,4,0,8,0],
            [5,0,6,0,0,8,0,0,0],
            [0,0,0,6,0,3,0,0,0],
            [0,9,0,5,0,0,0,0,0],
            [0,0,7,0,0,0,4,0,0],
            [0,0,0,0,0,6,0,0,1],
            [8,0,5,2,3,0,1,0,6],
            [0,0,0,0,8,0,0,0,9],
            [0,0,0,0,0,0,0,0,3]]

    s59  = [[0,0,0,0,0,0,0,7,1],
            [0,1,0,0,0,2,9,4,0],
            [0,0,0,0,7,0,0,0,6],
            [0,5,0,0,0,6,0,0,0],
            [0,9,0,0,0,0,7,0,0],
            [2,3,6,0,1,4,0,5,0],
            [0,0,0,0,0,0,0,0,0],
            [0,2,4,6,0,0,3,8,0],
            [3,0,0,0,4,5,6,1,7]]

    

    grid=deepcopy(zapeklite)

    t1=time.time()
    solve(grid)
    t2=time.time()

    prt(grid)
    print("time: ",t2-t1, "s")