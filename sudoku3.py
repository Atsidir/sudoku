import os,sys,tty,termios


class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

def get():
        inkey = _Getch()
        while(1):
                k=inkey()
                if k!='':break
        if k == 'w':
                 if cursor[1]>0 :
                    cursor[1] -= 1
                    print(cursor[0],cursor[1])
                    draw(tomb2)
        elif k == 's':
                if cursor[1]<8:
                    cursor[1] += 1
                    print(cursor[0],cursor[1])
                    draw(tomb2)
        elif k == 'd':
                if cursor[0]<8:
                    cursor[0] += 1
                    print(cursor[0],cursor[1])
                    draw(tomb2)
        elif k == 'a':
                if cursor[0]>0:
                    cursor[0] -= 1
                    print(cursor[0],cursor[1])
                    draw(tomb2)
        elif k.isdigit()==True:
            changevalue(tomb2,cursor[1],cursor[0],int(k))
            game()
        elif k == '\x1b':
            exit()
        else:
            draw(tomb2)
            print("Not valid input")

def fieldinit():   
    
    f=open("sudoku.txt","r")
    sor=0
    for line in f:
        field.append([])
        for word in line.split():
              field[sor].append(int(word))
        sor = sor+1


def countzero(array):
    zeros=0
    for i in range(3):
        for j in range(3):
            for k in range(3):         
                for f in range(3):
                    if array[i][k][j][f] == 0:
                        zeros += 1
    return zeros

def countinline(array):
    valid=0
    for numb in range(1,10):
        for i in range(3):   
            for j in range(3):
                number=0
                for k in range(3):         
                    for f in range(3):
                        if array[i][k][j][f] == numb:
                            number += 1
                if number>1:
                    valid=1
    return valid

  

def countincolumn(array):
    valid=0
    for numb in range(1,10):
        for i in range(3):
            for j in range(3):
                number=0
                for k in range(3):   
                    for f in range(3):
                        if array[k][j][f][i] == numb:
                            number += 1
                if number>1:
                    valid=1
    return valid


def validsolution(array):
    valid=0
    if countincolumn(array) > 0:
        valid=1
    elif countinline(array)> 0:
        valid=1
    elif validwhole(array) > 0:
        valid=1
    return valid

def split(sor,oszlop):
    array=[]
    for i in range(3):
        array.append([])
        for j in range(3):
            array[i].append(field[i+sor][j+oszlop])
    return array

def splitminithrees(array):
    del array[:]
    line=0
    for i in range(0,9,3):
        array.append([])
        for j in range(0,9,3):
            array[line].append(split(i,j))
        line += 1

def changevalue(array,x,y,value):
    if array[(x)//3][(y)//3][(x%3)][(y%3)] == 0 or field[x][y]==0:
        array[(x)//3][(y)//3][(x%3)][(y%3)]=value

def spacealign(position):
    for space in range(position):
            print(" ",end="")
def drawminussign(x):
    for minussign in range(25):
            print("-",end="")

def draw(array):
    os.system('clear')
    for i in range(3):
        spacealign(40)
        drawminussign(25)
        print()
        for j in range(3):
            spacealign(40)
            for k in range(3):          
                print("| ",end="")
                for f in range(3):
                    if array[i][k][j][f] == 0:
                        if i==(cursor[1]//3) and k==(cursor[0]//3) and j==(cursor[1]%3) and f==(cursor[0]%3):
                            print('\x1b[0;37;47m%d\x1b[0m' %array[i][k][j][f]," ",sep="",end="")
                        else:
                            print('\x1b[0;35;8m%d\x1b[0m' %(array[i][k][j][f])," ",sep="",end="")
                    elif array[i][k][j][f] == field[i*3+j][k*3+f]:
                        if i==(cursor[1]//3) and k==(cursor[0]//3) and j==(cursor[1]%3) and f==(cursor[0]%3):
                            print('\x1b[1;32;47m%d\x1b[0m' %array[i][k][j][f]," ",sep="",end="")
                        else:
                            print('\x1b[1;33m%d\x1b[0m' %array[i][k][j][f]," ",sep="",end="")
                    else:
                        if i==(cursor[1]//3) and k==(cursor[0]//3) and j==(cursor[1]%3) and f==(cursor[0]%3):
                            print('\x1b[1;34;47m%d\x1b[0m' %array[i][k][j][f]," ",sep="",end="")
                        else:
                            print('\x1b[1;34m%d\x1b[0m' %array[i][k][j][f]," ",sep="",end="")
            print("|")
    spacealign(40)
    drawminussign(25)
    print()
    
        
def validminitree(array):
    valid=0
    for number in range(1,10):
        countnumber=0
        for i in range(3):
            for j in range(3):
                if array[i][j] == number:
                    countnumber+=1
        if countnumber>1:
            valid=1
    return valid


def validwhole(array):
    valid=0
    for i in range(3):
        for j in range(3):
            if validminitree(tomb2[i][j])>0:
                valid=1
    return valid

def game():
    if validsolution(tomb2) > 0:
        column,line,minitree=False,False,False
        if countincolumn(tomb2) > 0:
            column=True
        elif countinline(tomb2)> 0:
            line=True
        elif validwhole(tomb2) > 0:
            minitree=True
        changevalue(tomb2,cursor[1],cursor[0],0)
        draw(tomb2) 
        if column==True:
            print("Not valid number,in the column there is already one.")
        elif line==True:
            print("Not valid number,in the line there is already one.")
        elif minitree==True:
            print("Not valid number,in the mini square there is already one.")
    else:
        draw(tomb2)

def sudoku():
    global numberzero
    draw(tomb2)
    while numberzero>0:
        get()
        numberzero=countzero(tomb2)
    print("Well done Smartass!")

def main():
    while True:
        os.system('clear')
        print("Type one of the following words:game,help,exit")
        choose=input()
        if choose=="game":
            sudoku()
            exit()
        elif choose=="exit":
            exit()
        elif choose=="help":
            print("Press WASD to move cursor")
            print("Press a number if a cursor is in a right position")
            print("Press escape or arrowkeys to quit")
            print("start the game or exit tutorial (type start or exit to terminal)")
            choose2=input()
            if choose2=="start":

                sudoku()
                exit()
            elif choose2=="exit":
                exit()
            else:
                print("Not valid input")

        else:
            print("not valid input")
size = 9
field = []
tomb2= []
fieldinit()
cursor=[0,0]
splitminithrees(tomb2)
numberzero=countzero(tomb2)

main()
