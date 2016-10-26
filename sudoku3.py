import os
import sys
import tty
import termios
import random

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
        k = inkey()
        if k != '':
            break
    if k == 'w':
        if cursor[1] > 0:
            cursor[1] -= 1
            draw(tomb2)
    elif k == 's':
        if cursor[1] < 8:
            cursor[1] += 1
            draw(tomb2)
    elif k == 'd':
        if cursor[0] < 8:
            cursor[0] += 1
            draw(tomb2)
    elif k == 'a':
        if cursor[0] > 0:
            cursor[0] -= 1
            draw(tomb2)
    elif k == 'n':
        copyfield(solved)
        sudokusolvere(solved)
        draw(solved)
        print('Too easy')
        exit()
    elif k.isdigit():
        changevalue(tomb2, cursor[1], cursor[0], int(k))
        draw(tomb2)
        game()
    elif k == '\x1b':
        exit()
    else:
        draw(tomb2)
        print("Not valid input")


def fieldinit():
    for i in range(9):
        field.append([])
        for j in range(9):
            field[i].append(0)

def fieldgenerator(level=5):
    count=0
    while count<level:
        x=random.randint(0,8)
        y=random.randint(0,8)
        if field[x][y]!=0:
            field[x][y]=0
            count +=1


def countzero(array):
    zeros = 0
    for i in range(9):
        for j in range(9):
                    if array[i][j] == 0:
                        zeros += 1
    return zeros


def countinline(array):
    valid = 0
    for numb in range(1, 10):
        for i in range(9):
            number = 0
            for j in range(9):
                if array[i][j] == numb:
                        number += 1
            if number > 1:
                valid = 1
    return valid


def countincolumn(array):
    valid = 0
    for numb in range(1, 10):
        for i in range(9):
            number = 0
            for j in range(9):
                if array[j][i] == numb:
                    number += 1
            if number > 1:
                valid = 1
    return valid

def validmini(array):
    valid=0
    for numb in range(1,10):
        for i in range(3):
            for j in range(3):
                number=0
                for k in range(3):
                    for l in range(3):
                        if array[i*3+k][j*3+l]==numb:
                            number +=1
                if number>1:
                    valid=1
    return valid


def validsolution(array):
    valid = 0
    if countincolumn(array) > 0:
        valid = 1
    elif countinline(array) > 0:
        valid = 1
    elif validmini(array) > 0:
        valid = 1
    return valid

def copyfield(array):
    del array[:]
    for i in range(9):
        array.append([])
        for j in range(9):
            array[i].append(field[i][j])


def changevalue(array, x, y, value):
    if array[x][y] == 0 or field[x][y] == 0:
        array[x][y] = value


def spacealign(position):
    for space in range(position):
        print(" ", end="")


def drawminussign(x):
    for minussign in range(25):
        print("-", end="")


def draw(array):
    os.system('clear')
    spacealign(40)
    drawminussign(25)
    print()
    for i in range(9):
        spacealign(40)
        for j in range(3):
                print("| ", end="")
                for f in range(3):
                    if array[i][j*3+f] == 0:
                        if i == cursor[1] and j*3+f == cursor[0]:
                            print('\x1b[0;37;47m%d\x1b[0m' % array[i][j*3+f], " ", sep="", end="")
                        else:
                            print('\x1b[0;35;8m%d\x1b[0m' % (array[i][j*3+f]), " ", sep="", end="")
                    elif array[i][j*3+f] == field[i][j*3+f]:
                        if i == cursor[1] and j*3+f == cursor[0]:
                            print('\x1b[1;32;47m%d\x1b[0m' % array[i][j*3+f], " ", sep="", end="")
                        else:
                            print('\x1b[1;33m%d\x1b[0m' % array[i][j*3+f], " ", sep="", end="")
                    else:
                        if i == cursor[1] and j*3+f == cursor[0]:
                            print('\x1b[1;34;47m%d\x1b[0m' % array[i][j*3+f], " ", sep="", end="")
                        else:
                            print('\x1b[1;34m%d\x1b[0m' % array[i][j*3+f], " ", sep="", end="")
        print('|')
        if (i+1)%3 == 0:
            spacealign(40)
            drawminussign(25)
            print("")


def game():
    if validsolution(tomb2) > 0:
        column, line, minitree = False, False, False
        if countincolumn(tomb2) > 0:
            column = True
        elif countinline(tomb2) > 0:
            line = True
        elif validmini(tomb2) > 0:
            minitree = True
        changevalue(tomb2, cursor[1], cursor[0], 0)
        draw(tomb2)
        if column:
            print("Not valid number,in the column there is already one.")
        elif line:
            print("Not valid number,in the line there is already one.")
        elif minitree:
            print("Not valid number,in the mini square there is already one.")
    else:
        draw(tomb2)


def sudoku(level):
    sudokusolver(field)
    fieldgenerator(level)
    copyfield(tomb2)
    draw(tomb2)
    numberzero=countzero(tomb2)
    while numberzero > 0:
        get()
        numberzero = countzero(tomb2)
    print("Well done Smartass!")

def nextemptyspace(array):
    if countzero(array)>76:
            while True:
                x=random.randrange(0,9)
                y=random.randrange(0,9)
                if array[x][y]==0:
                    return x,y
    else:
        for i in range(9):
            for j in range(9):
                if array[i][j]==0:
                    return i,j
        return -1,-1

def sudokusolver(array):
    x,y = nextemptyspace(array)
    if x<0:
        return True
    for numb in range(1,10):
        array[x][y]=numb
        if validsolution(array)==0:
            if sudokusolver(array):
                return True
        else:
            array[x][y]=0
    return False

def sudokusolvere(array):
    x,y = nextemptyspace(array)
    if x<0:
        return True
    for numb in range(1,10):
        array[x][y]=numb
        draw(array)
        if validsolution(array)==0:
            if sudokusolver(array):
                return True
        else:
            array[x][y]=0
    return False

def main():
    while True:
        os.system('clear')
        print("Type one of the following words:game,help,exit")
        choose = input()
        if choose == "game":
            while True:
                level=input("Choose level:1,2,3 \n")
                if level=='1':
                        sudoku(10)
                        exit()
                elif level=='2':
                        sudoku(25)
                        exit()
                elif level=='3':
                        sudoku(50)
                        exit()
                else:
                        print("Wrong input Dumbass")
        elif choose == "exit":
            exit()    
        elif choose == "help":
            print("Press WASD to move cursor")
            print("Press a number if a cursor is in a right position")
            print("Press escape or arrowkeys to quit")
            print("start the game or exit tutorial (type start or exit to terminal)")
            choose2 = input()
            if choose2 == "start":
                sudoku()
                exit()
            elif choose2 == "exit":
                exit()
            else:
                print("Not valid input")
        else:
            print("not valid input")


size = 9
field = []
tomb2 = []
solved= []
cursor = [0, 0]
fieldinit()
numberzero=81

main()




