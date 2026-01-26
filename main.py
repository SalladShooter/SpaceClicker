import curses
from curses import wrapper
import time

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    stdscr.nodelay(True)

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
    resources = [
        ['CREDITS', money],
        ['ENERGY', energy],
    ]
    tick = 0
    location = "Earth"
    last_key = None

    def display_center_text(text,y,style=curses.A_NORMAL):
        h, w = stdscr.getmaxyx()
        if h <= 0 or w <= 0:
            return

        if y < 0 or y >= h:
            return

        visible = text[:max(0, w)]
        x = max(0, (w - len(visible)) // 2)

        try:
            stdscr.addstr(y, x, visible, style)
        except curses.error:
            pass

    def build():
        pass

    def display_resources(width):
        resource_win.erase()
        resource_win.border()
        try:
            resource_win.addstr(0, width//2-len(' RESOURCES ')//2, ' RESOURCES ', STANDOUT)
        except curses.error:
            pass

        for resource in range(len(resources)):
            try:
                resource_win.addstr(resource+1, 1, f'{resources[resource][0]} - {resources[resource][1]}')
            except curses.error:
                pass

        resource_win.refresh()

    def display_cur_building(width):
        cur_building_win.erase()
        cur_building_win.border()
        try:
            cur_building_win.addstr(0, width//2-len(' BUILDINGS ')//2, ' BUILDINGS ', STANDOUT)
        except curses.error:
            pass
        cur_building_win.refresh()

    def display_log(width):
        log_win.erase()
        log_win.border()
        try:
            log_win.addstr(0, width//2-len(' CONSOLE ')//2, ' CONSOLE ', STANDOUT)
        except curses.error:
            pass
        log_win.refresh()

    h, w = stdscr.getmaxyx()
    last_h, last_w = h, w

    resource_win = curses.newwin(h-4,w//3-2,2,2)
    cur_building_win = curses.newwin(h-4,w//3-2,2,w//3+2)
    log_win = curses.newwin(h-4,w//3-4,2,w//3*2+2)

    stdscr.erase()
    stdscr.border()
    stdscr.refresh()

    while True:
        h, w = stdscr.getmaxyx()
        top_bar_text = f' SpaceClicker - TIME {tick} - LOCATION {location} '
        bottom_bar_text = f' (c) GAIN CREDITS - (b) BUILD - (q) QUIT '
        if h < 6 + len(resources) or w < len(top_bar_text)+1+4:
            stdscr.clear()
            try:
                stdscr.addstr(0, 0, "Terminal too small. Enlarge window.")
            except curses.error:
                pass
            stdscr.refresh()
            time.sleep(0.1)
            stdscr.clear()
            stdscr.border()
            stdscr.refresh()
            continue

        if (h, w) != (last_h, last_w):
            last_h, last_w = h, w

            resource_win = curses.newwin(h-4,w//3-2,2,2)
            cur_building_win = curses.newwin(h-4,w//3-2,2,w//3+2)
            log_win = curses.newwin(h-4,w//3-4,2,w//3*2+2)

            stdscr.clear()
            stdscr.border()
            stdscr.refresh()

        display_resources(w//3-2)
        display_cur_building(w//3-2)
        display_log(w//3-2)

        display_center_text(top_bar_text, 0, DIM)
        display_center_text(bottom_bar_text, h-1, DIM)

        last_key = curses.ERR
        key = stdscr.getch()
        while key != curses.ERR:
            last_key = key
            key = stdscr.getch()

        if last_key == ord('c'):
            money += 1
            resources[0][1] = money
        elif last_key == ord('b'):
            build()
        elif last_key == ord('q'):
            break

        tick += 1
        stdscr.refresh()
        time.sleep(0.1)

wrapper(main)
