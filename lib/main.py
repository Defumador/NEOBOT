import sys
import time
import traceback
import cProfile
import logging

import logging
import tkinter
import datetime
import tkinter.scrolledtext as ScrolledText
from tkinter import ttk

import lib.bookmarks
import lib.drones
import lib.navigation
import lib.overview
from lib import docked, load_ship, navigation as nav, unload_ship, mining
from lib.vars import system_mining, originx, originy, windowx, windowy

sys.setrecursionlimit(9999999)
playerfound = 0



# TERMINOLOGY #################################################################

# A 'warning' is a persistent dialogue window that appears in the center of
# the screen and dims the rest of the screen. Warnings can only be dismissed
# with an explicit keystroke or button click from the user.

# A 'popup' is a partially transparent block of text that appears in the
# main play area for about five seconds.

# A function with the word 'loop' in its name will not return until a certain
# condition has been met or it times out.

###############################################################################

# These variables are for the mining script only ------------------------------
# Script begins at location 0, assumed to be your home station.
site = 7
# Total number of saved bookmark locations. This variable is set by the user.
total_sites = 10
# Number of 'runs' completed for mining script
runs = 1
# -----------------------------------------------------------------------------
modules = 0
drones = 0

detect_npcs_var = 1

detect_npc_frigate_and_destroyer = 0
detect_npc_cruiser_and_battlecruiser = 1
detect_npc_battleship = 1

detect_pcs = 1

detect_pc_industrial = 1
detect_pc_mining_barge = 1
detect_pc_frigate_and_destroyer = 1
detect_pc_capital_industrial_and_freighter = 1
detect_pc_cruiser_and_battlecruiser = 1
detect_pc_battleship = 1
detect_pc_rookie_ship = 1
detect_pc_capsule = 1

# recommended per https://docs.python.org/2/library/logging.html
logger = logging.getLogger(__name__)


# logging.basicConfig(format='(%(levelno)s) %(asctime)s - %(funcName)s -- %('
# 'message)s', level=logging.DEBUG)


# MAIN SCRIPTS ################################################################
def miner():
    print('main, drones is ', drones)
    print('detect pc', detect_pcs)
    return
    global playerfound
    global site
    global runs
    timer_var = 0
    logging.info('beginning run' + (str(runs)))
    while docked.docked_check() == 0:
        if lib.drones.detect_drones_launched() == 1:
            lib.overview.focus_client()
            lib.drones.recall_drones_loop()
        # Increment desired mining site by one as this is the next location
        # ship will warp to.
        site += 1
        # If there aren't any more sites left, loop back around to site 1.
        if site > total_sites:
            site = 1
        if lib.bookmarks.travel_to_bookmark(site) == 1:
            # Once arrived at site, check for hostile npcs and human players.
            # If either exist, warp to the next site.
            # If no hostiles npcs or players are present, check for asteroids.
            # If no asteroids, blacklist site and warp to next site.
            if lib.overview.detect_npcs_var == 1:
                if lib.overview.focus_overview_tab('general') == 1:
                    if lib.overview.detect_npcs() == 1:
                        miner()
            if lib.overview.detect_pcs_var == 1:
                if lib.overview.detect_pcs() == 1:
                    playerfound += 1
                    miner()

            lib.overview.focus_overview_tab('mining')
            while mining.detect_ore() == 1:
                lib.drones.launch_drones_loop()
                if mining.target_ore() == 0:
                    miner()
                mining.activate_miner()
                # If ship inventory isn't full, continue to mine ore and wait
                # for popups or errors.
                # Switch back to the general tab for easier ship detection
                lib.overview.focus_overview_tab('general')
                while mining.inv_full_popup() == 0:
                    if mining.asteroid_depleted_popup() == 1:
                        if mining.detect_ore() == 0:
                            #nav.blacklist_local_bookmark()
                            miner()
                        elif mining.detect_ore() == 1:
                            if mining.target_ore() == 0:
                                miner()
                            mining.activate_miner()
                            mining.inv_full_popup()
                            continue
                    if lib.overview.detect_npcs() == 1 or \
                            lib.overview.detect_pcs() == 1 or \
                            lib.overview.detect_jam() == 1 or \
                            mining.timer(timer_var) == 1:
                        lib.drones.recall_drones_loop()
                        miner()
                    timer_var += 1
                    time.sleep(1)

                if mining.inv_full_popup() == 1:
                    # Once inventory is full, dock at home station and unload.
                    lib.drones.recall_drones_loop()
                    logging.info('finishing run' + (str(runs)))
                    if system_mining == 0:
                        if lib.bookmarks.set_home() == 1:
                            if navigator() == 1:
                                unload_ship.unload_ship()
                                docked.undock_loop()
                                playerfound = 0
                                time.sleep(3)
                                runs += 1
                                miner()
                    # If ship is mining in the same system it will dock in,
                    # a different set of functions is required.
                    elif system_mining == 1:
                        lib.bookmarks.dock_at_local_bookmark()
                        unload_ship.unload_ship()
                        docked.undock_loop()
                        playerfound = 0
                        time.sleep(3)
                        runs += 1
                        miner()

                if mining.detect_ore() == 0:
                    lib.bookmarks.blacklist_local_bookmark()
        elif lib.bookmarks.travel_to_bookmark(site) == 0:
            nav.emergency_terminate()
            sys.exit(0)
    if docked.docked_check() == 1:
        # If docked when script starts, undock_loop.
        lib.overview.focus_client()
        docked.undock_loop()
        miner()



def navigator():
    # A standard warp-to-zero autopilot script. Warp to the destination, then
    # terminate.
    print('navigator -- running navigator')
    nav.detect_route()
    dockedcheck = docked.docked_check()

    while dockedcheck == 0:
        lib.overview.focus_client()
        selectwaypoint = nav.warp_to_waypoint()
        while selectwaypoint == 1:  # Value of 1 indicates stargate waypoint.
            time.sleep(5)  # Wait for jump to begin.
            detectjump = nav.detect_jump_loop()
            if detectjump == 1:
                lib.overview.focus_client()
                selectwaypoint = nav.warp_to_waypoint()
            else:
                nav.emergency_terminate()
                traceback.print_exc()
                traceback.print_stack()
                sys.exit('navigator -- error detecting jump')

        while selectwaypoint == 2:  # Value of 2 indicates a station waypoint.
            time.sleep(5)
            detectdock = nav.detect_dock_loop()
            if detectdock == 1:
                print('navigator -- arrived at destination')
                return 1
        else:
            print('navigator -- likely at destination')
            return 1

    while dockedcheck == 1:
        docked.undock_loop()
        time.sleep(5)
        navigator()


def collector():
    # Haul all items from a predetermined list of stations to a single 'home'
    # station, as specified by the user. The home station is identified by a
    # station bookmark beginning with '000', while the remote stations are any
    # station bookmark beginning with the numbers 1-9. This means up to 10
    # remote stations are supported.
    print('collector -- running collector')
    dockedcheck = docked.docked_check()
    while dockedcheck == 0:
        lib.overview.focus_client()
        selectwaypoint = nav.warp_to_waypoint()

        while selectwaypoint == 1:
            time.sleep(3)  # Wait for warp to start.
            detectjump = nav.detect_jump_loop()
            if detectjump == 1:
                lib.overview.focus_client()
                selectwaypoint = nav.warp_to_waypoint()
        while selectwaypoint == 2:
            time.sleep(3)
            detectdock = nav.detect_dock_loop()
            if detectdock == 1:
                collector()
        else:
            print(
                'collector -- error with at_dest_check_var and '
                'at_home_check_var')
            traceback.print_exc()
            traceback.print_stack()
            sys.exit()

    while dockedcheck == 1:
        athomecheck = lib.bookmarks.detect_at_home()
        # If docked at home station, set a destination waypoint to a remote
        # station and unload cargo from ship into home station inventory.
        if athomecheck == 1:
            unload_ship.unload_ship()
            lib.bookmarks.set_dest()
            docked.undock_loop()
            collector()
        elif athomecheck == 0:
            print('collector -- not at home')
            loadship = load_ship.load_ship_full()
            print('collector -- loadship is', loadship)

            if loadship == 2 or loadship == 0 or loadship is None:
                atdestnum = lib.bookmarks.detect_bookmark_location()
                if atdestnum == -1:
                    docked.undock_loop()
                    collector()
                else:
                    lib.bookmarks.set_dest()
                    lib.bookmarks.blacklist_station()
                    docked.undock_loop()
                    collector()
            elif loadship == 1:  # Value of 1 indicates ship is full.
                lib.bookmarks.set_home()
                docked.undock_loop()
                collector()

        else:
            print('collector -- error with detect_at_home and at_dest_check')
            traceback.print_exc()
            traceback.print_stack()
            sys.exit()
    if dockedcheck is None:
        collector()


print("originx =", originx)
print("originy =", originy)
print("windowx =", windowx)
print("windowy =", windowy)

#miner()

# cProfile.run('lib.overview.detect_jam()')
# Method for determining which script to run, as yet to be implemented by gui.
# selectscript = 2
#
# if selectscript == 1:
#	navigator()
# elif selectscript == 2:
#	nav.detect_route()
#	collector()

'''
# unit tests
while mining.inv_full_popup() == 0:
    if mining.asteroid_depleted_popup() == 1:
        if mining.detect_asteroids() == 0:
            # nav.blacklist_local_bookmark()
            miner()
        elif mining.detect_asteroids() == 1:
            mining.target_asteroid()
            mining.activate_miner()
            mining.inv_full_popup()
            continue
    if threading.Thread(target=mining.detect_pcs()).start() == 1:
        mining.recall_drones_loop()
        miner()
    if threading.Thread(target=mining.detect_pcs()).start() == 1:
        mining.recall_drones_loop()
        miner()
    time.sleep(2)
'''

'''
sample threading implementation

import threading
import time

stop = 0
lock = threading.Lock()

def shield_check():
    global stop
    for i in range(1, 15):
        time.sleep(1)
        print('shield_check', i)
        if stop == 1:
            print('shield check stopping!')
            break
        elif i >= 4:
            print('shield check warping out!')
            stop = 1
            warpout()

def npc_check():
    global stop
    for i in range(1, 21):
        time.sleep(2)
        print('npc_check', i)
        if stop == 1:
            print('npc_check stopping!')
            break
        elif i >= 2:
            print('npc_check warping out!')
            stop = 1
            warpout()

def warpout():
    lock.acquire()
    for i in range(1, 5):
        time.sleep(3)
        print('warping out!', i)
    lock.release()
'''


# GUI #########################################################################


class simpleapp_tk(tkinter.Tk):
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent

        self.grid()

        global detect_npcs_var, detect_npc_frigate_and_destroyer, \
            detect_npc_cruiser_and_battlecruiser, detect_npc_battleship

        global detect_pcs_var, detect_pc_industrial, detect_pc_mining_barge, \
            detect_pc_frigate_and_destroyer, \
            detect_pc_capital_industrial_and_freighter, \
            detect_pc_cruiser_and_battlecruiser, detect_pc_battleship, \
            detect_pc_rookie_ship, detect_pc_capsule

        detect_npcs_var = tkinter.IntVar()

        detect_npc_frigate_and_destroyer = tkinter.IntVar()
        detect_npc_cruiser_and_battlecruiser = tkinter.IntVar()
        detect_npc_battleship = tkinter.IntVar()

        detect_pcs_var = tkinter.IntVar()

        detect_pc_industrial = tkinter.IntVar()
        detect_pc_mining_barge = tkinter.IntVar()
        detect_pc_frigate_and_destroyer = tkinter.IntVar()
        detect_pc_capital_industrial_and_freighter = tkinter.IntVar()
        detect_pc_cruiser_and_battlecruiser = tkinter.IntVar()
        detect_pc_battleship = tkinter.IntVar()
        detect_pc_rookie_ship = tkinter.IntVar()
        detect_pc_capsule = tkinter.IntVar()

        def start():
            global drones, modules, detect_pcs
            modules = (int(self.combo_modules.get()))
            drones = (int(self.combo_drones.get()))
            logger.debug((str(modules)) + ' modules')
            logger.debug((str(drones)) + ' drones')

            detect_pcs = (int(detect_pcs_var.get()))
            logger.debug('detect pcs is ' + (str(detect_pcs)))
            miner()

        self.t = tkinter.Label(self, text="")
        self.t.grid(column=0, row=0, columnspan=2, sticky='W', padx=0,
                    pady=0)

        self.start = tkinter.Button(self, text="Start", command=start)
        self.start.grid(column=0, row=1, sticky='W')
        self.start.config(width='13', height='1')

        self.stop = tkinter.Button(self, text="Stop")
        self.stop.grid(column=1, row=1, columnspan=1, sticky='W')
        self.stop.config(width='13', height='1')

        self.end = tkinter.Button(self, text="End Run")
        self.end.grid(column=1, row=2, columnspan=1, sticky='W')
        self.end.config(width='13', height='1')

        self.t = tkinter.Label(self, text="")
        self.t.grid(column=0, row=3, columnspan=2, sticky='W', padx=0,
                    pady=0)

        self.combo_modules = ttk.Combobox(self, values=[1, 2, 3, 4])
        self.combo_modules.current(2)
        self.combo_modules.grid(column=1, row=4, columnspan=1, sticky='W')
        self.combo_modules.config(width='4', height='10')
        self.m = tkinter.Label(self, text="mc")
        self.m.grid(column=0, row=4, columnspan=1, sticky='W', padx=5)

        self.combo_drones = ttk.Combobox(self, values=[0, 1, 2, 3, 4, 5])
        self.combo_drones.current(0)
        self.combo_drones.grid(column=1, row=5, columnspan=1, sticky='W')
        self.combo_drones.config(width='4', height='10')
        self.label_drones = tkinter.Label(self, text="drones")
        self.label_drones.grid(column=0, row=5, columnspan=1, sticky='W',
                               padx=5)

        self.check_pc = tkinter.Checkbutton(self, text='pc check',
                                            variable=detect_pcs_var)
        self.check_pc.grid(column=0, row=6, columnspan=1, sticky='W')
        # self.check_pc = tkinter.Checkbutton(self, text='pc frig/des check',
        # variable=pcfd)
        # self.check_pc.grid(column=1, row=5, columnspan=1, sticky='W')
        # self.check_pc = tkinter.Checkbutton(self, text='pc cru/bc check',
        ## variable=pcbc)
        # self.check_pc.grid(column=0, row=6, columnspan=1, sticky='W')
        # self.check_pc = tkinter.Checkbutton(self, text='pc bs check',
        ## variable=pcbs)
        # self.check_pc.grid(column=1, row=6, columnspan=1, sticky='W')
        # self.check_pc = tkinter.Checkbutton(self, text='pc min frig check',
        ## variable=pcmf)
        # self.check_pc.grid(column=0, row=7, columnspan=1, sticky='W')
        # self.check_pc = tkinter.Checkbutton(self, text='pc indy check',
        ## variable=pci)
        # self.check_pc.grid(column=1, row=7, columnspan=1, sticky='W')

        # self.check_pc = tkinter.Checkbutton(self, text='npc check',
        ## variable=npc)
        # self.check_pc.grid(column=0, row=8, columnspan=1, sticky='W')
        # self.check_pc = tkinter.Checkbutton(self, text='npc frig/des
        ## check', variable=npcfd)
        # self.check_pc.grid(column=1, row=8, columnspan=1, sticky='W')
        # self.check_pc = tkinter.Checkbutton(self, text='npc cru/bc check',
        ## variable=npcbc)
        # self.check_pc.grid(column=0, row=9, columnspan=1, sticky='W')
        # self.check_pc = tkinter.Checkbutton(self, text='npc bs check',
        ## variable=npcbs)
        # self.check_pc.grid(column=1, row=9, columnspan=1, sticky='W')

        # self.check_pc = tkinter.Checkbutton(self, text='ecm check',
        # variable=ecm)
        # self.check_pc.grid(column=0, row=10, columnspan=1, sticky='W')

        self.mytext = ScrolledText.ScrolledText(self, state="disabled")
        self.mytext.grid(column=0, row=99, columnspan=99)
        self.mytext.grid_columnconfigure(0, weight=1)
        self.mytext.grid_rowconfigure(0, weight=1)
        self.mytext.config(width='30', height='15')

        self.mybutton = tkinter.Button(self, text="ClickMe")
        self.mybutton.grid(column=0, row=2, sticky='W')
        self.mybutton.bind("<ButtonRelease-1>", self.button_callback)
        self.mybutton.config(width='13', height='1')

    def button_callback(self, event):
        now = datetime.datetime.now()
        logger.info(now)


class MyHandlerText(logging.StreamHandler):
    def __init__(self, textctrl):
        logging.StreamHandler.__init__(self)  # initialize parent
        self.textctrl = textctrl

    def emit(self, record):
        msg = self.format(record)
        self.textctrl.config(state="normal")
        self.textctrl.insert(tkinter.END, msg + "\n")
        self.flush()
        self.textctrl.config(state="disabled")
        self.textctrl.yview(tkinter.END)


if __name__ == "__main__":
    # create Tk object instance
    app = simpleapp_tk(None)
    app.title('NEOMINER v0.1')

    # setup logging handlers using the Tk instance created above
    # the pattern below can be used in other threads...
    # ...to allow other thread to send msgs to the gui
    # in this example, we set up two handlers just for demonstration (you could add a fileHandler, etc)
    stderrHandler = logging.StreamHandler()  # no arguments => stderr
    # logger.addHandler(stderrHandler)
    guiHandler = MyHandlerText(app.mytext)
    logger.addHandler(guiHandler)
    logger.setLevel(logging.DEBUG)
    logger.info("from main")

    # start Tk
    app.mainloop()
