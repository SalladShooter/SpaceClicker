import curses
from curses import wrapper
import time

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_BLACK, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_GREEN, -1)
    curses.init_pair(4, curses.COLOR_YELLOW, -1)
    curses.init_pair(5, curses.COLOR_BLUE, -1)
    curses.init_pair(6, curses.COLOR_MAGENTA, -1)
    curses.init_pair(7, curses.COLOR_CYAN, -1)
    curses.init_pair(8, curses.COLOR_WHITE, -1)

    BLACK = curses.color_pair(1)
    RED = curses.color_pair(2)
    GREEN = curses.color_pair(3)
    YELLOW = curses.color_pair(4)
    BLUE = curses.color_pair(5)
    MAGENTA = curses.color_pair(6)
    CYAN = curses.color_pair(7)
    WHITE = curses.color_pair(8)

    NORMAL = curses.A_NORMAL
    BOLD = curses.A_BOLD
    DIM = curses.A_DIM
    REVERSE = curses.A_REVERSE
    STANDOUT = curses.A_STANDOUT
    UNDERLINE = curses.A_UNDERLINE

    money = 0
    energy = 0

    def display_center_text(text,y,style=curses.A_NORMAL):
        h, w = stdscr.getmaxyx()
        x = max(0, (w - len(text)) // 2)
        stdscr.addstr(y, x, text[:max(0,w)], style)

    def build():
        pass

    while True:
        h, w = stdscr.getmaxyx()
        stdscr.clear()
        stdscr.border()
        stdscr.refresh()

        display_center_text(f' CREDITS {money} - ENERGY {energy} ', 0, STANDOUT)
        display_center_text(f' (c) GAIN CREDITS - (b) BUILD - (q) QUIT ', h-1, DIM)

        key = stdscr.getch()

        if key == ord('c'):
            money += 1
        elif key == ord('b'):
            build()
        elif key == ord('q'):
            break

wrapper(main)
