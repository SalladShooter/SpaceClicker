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
    silver = 0
    titaniun = 0
    uranium = 0
    resources = [
        ['CREDITS', money],
        ['ENERGY', energy],
        ['SILVER', silver],
        ['TITANIUM', titanium],
        ['URANIUM', uranium],
    ]
    buildings = [
        # NAME       CC SC TC UC NUM DESC                            OVER  EN PER SIL TIT URA
        ['MINE',    100, 0, 0, 0, 1, "Increase CREDIT gain ability",   1,  0, 10,  0,  0,  0],
        ['SHIP',     50, 0, 0, 0, 0, "Increase SILVER gain ability",   0,  1,  0,  0,  0,  0],
        ['DOCK',    100, 0, 0, 0, 0, "Increase TITANIUM gain ability", 0,  3,  0,  0,  0,  0],
        ['SHUTTLE', 100, 0, 0, 0, 0, "Increase URANIUM gain ability", 10,  5,  0,  0,  0,  0],
    ]
    build_selection = 0
    credit_gain = 1
    location = "Earth"
    tick = 0

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

    def display_resources(width):
        resource_win.erase()
        resource_win.attrset(BLUE)
        resource_win.border()
        try:
            resource_win.addstr(0, width//2-len(' RESOURCES ')//2, ' RESOURCES ', BLUE | STANDOUT)
        except curses.error:
            pass
        for resource in range(len(resources)):
            try:
                resource_win.addstr(resource+1, 1, f'{resources[resource][0]} - {resources[resource][1]}', WHITE)
            except curses.error:
                pass
        resource_win.refresh()

    def display_overview(width):
        overview_win.erase()
        overview_win.attrset(GREEN)
        overview_win.border()
        try:
            overview_win.addstr(0, width//2-len(' OVERVIEW ')//2, ' OVERVIEW ', GREEN | STANDOUT)
        except curses.error:
            pass
        for building in range(len(buildings)):
            if not buildings[building][5] == 0 and not buildings[building][7] == 0:
                try:
                    total_energy = buildings[building][5] * buildings[building][9] -  buildings[building][5] * buildings[building][8]
                    if total_energy < 0:
                        energy_symbol = ''
                    else:
                        energy_symbol = '+'
                    overview_win.addstr(building+1, 1, f'{buildings[building][5]} : {buildings[building][0]} - +{buildings[building][5]*buildings[building][7]}C/s {energy_symbol}{total_energy}E/s', WHITE)
                except curses.error:
                    pass
        overview_win.refresh()

    def display_log(width):
        log_win.erase()
        log_win.attrset(MAGENTA)
        log_win.border()
        try:
            log_win.addstr(0, width//2-len(' CONSOLE ')//2, ' CONSOLE ', MAGENTA | STANDOUT)
        except curses.error:
            pass
        log_win.refresh()


    def display_build(width):
        build_win.erase()
        build_win.attrset(YELLOW)
        build_win.border()
        try:
            build_win.addstr(0, width//2-len(' BUILD ')//2, ' BUILD ', YELLOW | STANDOUT)
        except curses.error:
            pass
        for building in range(len(buildings)):
            try:
                build_style = NORMAL
                if build_selection == building:
                    build_style = STANDOUT
                build_win.addstr(building+1, 1, f'{buildings[building][5]} : {buildings[building][0]} - C{buildings[building][1]} - {buildings[building][7]}', WHITE | build_style)
            except curses.error:
                pass

        build_win.refresh()

    h, w = stdscr.getmaxyx()
    last_h, last_w = h, w
    last_key = None

    resource_win = curses.newwin(h-4, w//3, 2, 2)
    overview_win = curses.newwin(h-4, w//3-1, 2, w//3+2)
    log_win = curses.newwin(h-4, w//3-1, 2, w//3*2+1)
    build_win = curses.newwin(h-4, w//3*2-2, 2, w//3+2)

    build_menu = False

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

            resource_win = curses.newwin(h-4, w//3, 2, 2)
            overview_win = curses.newwin(h-4, w//3-1, 2, w//3+2)
            log_win = curses.newwin(h-4, w//3-1, 2, w//3*2+1)
            build_win = curses.newwin(h-4, w//3*2-2, 2, w//3+2)

            stdscr.clear()
            stdscr.border()
            stdscr.refresh()

        display_resources(w//3-2)
        if build_menu:
            display_build(w//3*2-2)
        else:
            display_overview(w//3-2)
            display_log(w//3-2)

        display_center_text(top_bar_text, 0, BOLD)
        display_center_text(bottom_bar_text, h-1, DIM)

        last_key = curses.ERR
        key = stdscr.getch()
        while key != curses.ERR:
            last_key = key
            key = stdscr.getch()

        if build_menu and last_key == curses.KEY_DOWN:
            if build_selection + 1 < len(buildings):
                build_selection += 1
        elif build_menu and last_key == curses.KEY_UP:
            if build_selection - 1 >= 0:
                build_selection -= 1

        if build_menu and last_key == ord('u'):
            if money >= buildings[build_selection][1]:
                money -= buildings[build_selection][1]
                buildings[build_selection][1] = round(buildings[build_selection][1] * 1.4)
                buildings[build_selection][2] += 1

        if last_key == ord('c'):
            money += credit_gain
            resources[0][1] = money
        elif last_key == ord('b'):
            build_menu = not build_menu
            stdscr.clear()
            stdscr.border()
            stdscr.refresh()
        elif last_key == ord('q'):
            break

        tick += 1
        for building in range(len(buildings)):
            if buildings[building][5] > 0 and not buildings[building][7] == 0 and tick % 10 == 0:
                if (buildings[building][8] > 0 and energy > 0) or buildings[building][8] == 0:
                    money += round(buildings[building][5] * buildings[building][7])
                energy -= buildings[building][5] * buildings[building][8]
                energy += buildings[building][5] * buildings[building][9]
                resources[0][1] = round(money)
                resources[1][1] = energy
        stdscr.refresh()
        time.sleep(0.1)

wrapper(main)
