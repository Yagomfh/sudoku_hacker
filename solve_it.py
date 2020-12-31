#!/usr/bin/python3
import sys
from pynput.mouse import Controller as ctr
from pynput.mouse import Button
from pynput.keyboard import Key, Controller
import time

def get_todo_list(grid):
    res = []
    for x in range(0, 9):
        for y in range(0, 9):
            if grid[x][y] == 0:
                res.append({'x' : x, 'y' : y})
    return res

def display_grid(grid):
    for x in range(0, 9):
        if x == 3 or x == 6:
            print("------+-------+------")
        for y in range(0, 9):
            if y == 3 or y == 6:
                print("| ", end="")
            print(grid[x][y], end=" ")
        print("")

def line_to_grid(line):
    grid = []
    for x in range(0, 9):
        new_line = list(line[9 * x: 9 * x + 9])
        new_line = list(map(int, new_line))
        grid.append(new_line)
    return grid

def check_line(grid, nb, position):
    if nb in grid[position['x']]:
        return False
    return True

def check_column(grid, nb, position):
    for x in range(0, 9):
        if grid[x][position['y']] == nb:
            return False
    return True

def check_square(grid, nb, position):
    x = position['x'] // 3
    y = position['y'] // 3
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[x * 3 + i][y * 3 + j] == nb:
                return False
    return True

def solve(grid, todo_list, index):
    for nb in range(1, 10):
        if check_line(grid, nb, todo_list[index]) and check_column(grid, nb, todo_list[index]) and check_square(grid, nb, todo_list[index]):
            grid[todo_list[index]['x']][todo_list[index]['y']] = nb
            if index + 1 < len(todo_list):
                if solve(grid, todo_list, index + 1):
                    return grid
            else:
                return grid
        grid[todo_list[index]['x']][todo_list[index]['y']] = 0
    return False

def auto_solve(grid):
    mouse = ctr()
    keyboard = Controller()
    mouse.position = (48, 248)
    y_axis = [248, 303, 358, 410, 470, 521, 577, 629, 686]
    x_axis = [48, 105, 161, 216, 272, 326, 378, 435, 492]
    for i in range(0, 3):
        mouse.press(Button.left)
        mouse.release(Button.left)
    i = 0
    for y in y_axis:
        j = 0
        for x in x_axis:
            mouse.position = (x, y)
            time.sleep(0.1)
            mouse.click(Button.left, 2)
            keyboard.type(str(grid[i][j]))
            j += 1
        i += 1


def main():
    if len(sys.argv) != 2:
        print("Usage: ./solve_it [YOUR SUDOKU]\nYOUR SUDOKU format example: 000000018057000400000100000000300062700009105000060070002000030801007000009600020")
        return
    if len(sys.argv[1]) != 81:
        print("Your Sudoku is not 81 characters long...")
        return
    sudoku = sys.argv[1]
    grid = line_to_grid(sudoku)
    print("ok")
    display_grid(grid)
    todo_list = get_todo_list(grid)
    solve(grid, todo_list, 0)
    print("---------------------\n------SOLUTION:------\n---------------------")
    display_grid(grid)
    auto_solve(grid)

if __name__ == '__main__':
    main()
