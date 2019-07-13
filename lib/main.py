import sys
import time
import traceback
import cProfile
import logging
import threading

import logging
import tkinter
import datetime
import tkinter.scrolledtext as ScrolledText
from tkinter import ttk
import lib.drones
import lib.overview
from lib import docked, load_ship, navigation as nav, unload_ship, mining, \
    bookmarks, drones, overview
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

# recommended per https://docs.python.org/2/library/logging.html
logger = logging.getLogger(__name__)

# logging.basicConfig(format='(%(levelno)s) %(asctime)s - %(funcName)s -- %('
# 'message)s', level=logging.DEBUG)


# MAIN SCRIPTS ################################################################

def miner():
    ore1 = './img/overview/ore_types/plagioclase.bmp'
    ore2 = './img/overview/ore_types/pyroxeres.bmp'
    ore3 = './img/overview/ore_types/veldspar.bmp'
    ore4 = './img/overview/ore_types/scordite.bmp'
    ore5 = 0
    print('main, drones is', drones)
    global playerfound
    global site
    global runs
    timer_var = 0
    logging.info('beginning run' + (str(runs)))
    while docked.docked_check() == 0:
        if lib.drones.detect_drones_launched() == 1:
            lib.overview.focus_client()
            lib.drones.recall_drones_loop(drones)
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
            if lib.overview.focus_overview_tab('general') == 1:
                if lib.overview.detect_npcs(detect_npcs, npc_frig_dest,
                                            npc_cruiser_bc) == 1:
                    miner()
            if lib.overview.detect_pcs(detect_pcs, pc_indy, pc_barge,
                                       pc_frig_dest, pc_cruiser_bc, pc_bs,
                                       pc_capindy_freighter, pc_rookie,
                                       pc_pod) == 1:
                playerfound += 1
                miner()

            lib.overview.focus_overview_tab('mining')
            target = lib.overview.detect_overview_target(ore1, ore2, ore3,
                                                         ore4,
                                                         ore5)
            while lib.overview.detect_overview_target(ore1, ore2, ore3, ore4,
                                                      ore5
                                                      ) is not None:
                lib.drones.launch_drones_loop(drones)
                if lib.overview.target_overview_target(target) == 0:
                    miner()
                mining.activate_miner()
                # If ship inventory isn't full, continue to mine ore and wait
                # for popups or errors.
                # Switch back to the general tab for easier ship detection
                lib.overview.focus_overview_tab('general')
                while mining.inv_full_popup() == 0:
                    if mining.asteroid_depleted_popup() == 1:
                        target = lib.overview.detect_overview_target(ore1,
                                                                     ore2,
                                                                     ore3,
                                                                     ore4,
                                                                     ore5)
                        if lib.overview.detect_overview_target(ore1, ore2,
                                                               ore3, ore4, ore5
                                                               ) == 0:
                            #nav.blacklist_local_bookmark()
                            miner()

                        elif lib.overview.detect_overview_target(ore1, ore2,
                                                                 ore3, ore4,
                                                                 ore5
                                                                 ) is not None:
                            if lib.overview.target_overview_target(target) \
                                    == 0:
                                miner()
                            mining.activate_miner()
                            mining.inv_full_popup()
                            continue
                    if lib.overview.detect_npcs(detect_npcs, npc_frig_dest,
                                                npc_cruiser_bc) == 1 or \
                            lib.overview.detect_pcs(detect_pcs, pc_indy,
                                                    pc_barge,
                                                    pc_frig_dest,
                                                    pc_cruiser_bc, pc_bs,
                                                    pc_capindy_freighter,
                                                    pc_rookie,
                                                    pc_pod) == 1 or \
                            lib.overview.detect_jam() == 1 or \
                            mining.timer(timer_var) == 1:
                        lib.drones.recall_drones_loop(drones)
                        miner()
                    timer_var += 1
                    time.sleep(1)

                if mining.inv_full_popup() == 1:
                    # Once inventory is full, dock at home station and unload.
                    lib.drones.recall_drones_loop(drones)
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

                if lib.overview.detect_overview_target(ore1, ore2, ore3, ore4,
                                                       ore5
                                                       ) == 0:
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

# GUI #########################################################################

# def mainthread():
#    print('called mainthread')
#    threading.Thread(target=miner(), args=[])
#    return

gui = tkinter.Tk()

detect_npcs_gui = tkinter.IntVar()

npc_frig_dest_gui = tkinter.IntVar()
npc_cruiser_bc_gui = tkinter.IntVar()
npc_bs_gui = tkinter.IntVar()

detect_pcs_gui = tkinter.IntVar()
detect_pcs_gui.set(1)

pc_indy_gui = tkinter.IntVar()
pc_indy_gui.set(1)

pc_barge_gui = tkinter.IntVar()
pc_barge_gui.set(1)

pc_frig_dest_gui = tkinter.IntVar()
pc_frig_dest_gui.set(1)

pc_capindy_freighter_gui = tkinter.IntVar()
pc_capindy_freighter_gui.set(1)

pc_cruiser_bc_gui = tkinter.IntVar()
pc_cruiser_bc_gui.set(1)

pc_bs_gui = tkinter.IntVar()
pc_bs_gui.set(1)

pc_rookie_gui = tkinter.IntVar()
pc_pod_gui = tkinter.IntVar()

t = tkinter.Label(text="")
t.grid(column=0, row=0, columnspan=2, sticky='W', padx=0,
       pady=0)

t = tkinter.Label(text="")
t.grid(column=0, row=3, columnspan=2, sticky='W', padx=0,
       pady=0)

combo_modules = ttk.Combobox(values=[1, 2, 3, 4])
combo_modules.current(1)
combo_modules.grid(column=1, row=4, columnspan=1, sticky='W')
combo_modules.config(width='4', height='10')
m = tkinter.Label(text="mining lasers")
m.grid(column=0, row=4, columnspan=1, sticky='W', padx=5)

combo_drones = ttk.Combobox(values=[0, 1, 2, 3, 4, 5])
combo_drones.current(2)
combo_drones.grid(column=1, row=5, columnspan=1, sticky='W')
combo_drones.config(width='4', height='10')
label_drones = tkinter.Label(text="drones")
label_drones.grid(column=0, row=5, columnspan=1, sticky='W',
                  padx=5, pady=5)

detect_pcs = tkinter.Checkbutton(text='pc check',
                                 variable=detect_pcs_gui)
detect_pcs.grid(column=0, row=6, columnspan=1, sticky='W')

pc_indy = tkinter.Checkbutton(text='pc indy check',
                              variable=pc_indy_gui)
pc_indy.grid(column=1, row=6, columnspan=1, sticky='W')

pc_barge = tkinter.Checkbutton(text='pc barge check',
                               variable=pc_barge_gui)
pc_barge.grid(column=0, row=7, columnspan=1, sticky='W')

pc_frig_dest = tkinter.Checkbutton(text='pc frig/dest '
                                        'check',
                                   variable=pc_frig_dest_gui)
pc_frig_dest.grid(column=1, row=7, columnspan=1, sticky='W')

pc_capindy_freighter = tkinter.Checkbutton(text='pc '
                                                'cap '
                                                'indy/freighter check',
                                           variable=pc_capindy_freighter_gui)
pc_capindy_freighter.grid(column=0, row=8, columnspan=1,
                          sticky='W')

pc_cruiser_bc = tkinter.Checkbutton(text='pc cruiser/bc '
                                         'check',
                                    variable=pc_cruiser_bc_gui)
pc_cruiser_bc.grid(column=1, row=8, columnspan=1, sticky='W')

pc_bs = tkinter.Checkbutton(text='pc bs check',
                            variable=pc_bs_gui)
pc_bs.grid(column=0, row=9, columnspan=1, sticky='W')

pc_rookie = tkinter.Checkbutton(text='pc rookie check',
                                variable=pc_rookie_gui)
pc_rookie.grid(column=1, row=9, columnspan=1, sticky='W')

pc_pod = tkinter.Checkbutton(text='pc pod check',
                             variable=pc_pod_gui)
pc_pod.grid(column=0, row=10, columnspan=1, sticky='W')

detect_npcs = tkinter.Checkbutton(text='npcs check',
                                  variable=detect_npcs_gui)
detect_npcs.grid(column=1, row=10, columnspan=1, sticky='W')

npc_frig_dest = tkinter.Checkbutton(text='npc frig/dest '
                                         'check',
                                    variable=npc_frig_dest_gui)
npc_frig_dest.grid(column=0, row=11, columnspan=1, sticky='W')

npc_cruiser_bc = tkinter.Checkbutton(text='npc bs check',
                                     variable=npc_cruiser_bc_gui)
npc_cruiser_bc.grid(column=1, row=11, columnspan=1, sticky='W')

t = tkinter.Label(text="")
t.grid(column=0, row=12, columnspan=2, sticky='W', padx=0,
       pady=0)


# self.npc_bs = tkinter.Checkbutton(self, text='npc bs check',
#                                    variable=npc_bs_gui)
# self.npc_bs.grid(column=1, row=10, columnspan=1, sticky='W')

# self.detect_jam = tkinter.Checkbutton(self, text='jam check',
# variable=detect_jam)
# self.check_pc.grid(column=0, row=10, columnspan=1, sticky='W')

# self.mytext = ScrolledText.ScrolledText(self, state="disabled")
# self.mytext.grid(column=0, row=99, columnspan=99)
# self.mytext.grid_columnconfigure(0, weight=1)
# self.mytext.grid_rowconfigure(0, weight=1)
# self.mytext.config(width='30', height='15')


def start(event):
    global drones, modules

    global detect_pcs, pc_indy, pc_barge, pc_frig_dest, \
        pc_capindy_freighter, pc_cruiser_bc, pc_bs, pc_rookie, pc_pod

    global detect_npcs, npc_frig_dest, npc_cruiser_bc, npc_bs

    modules = (int(combo_modules.get()))
    drones = (int(combo_drones.get()))
    logger.debug((str(modules)) + ' modules')
    logger.debug((str(drones)) + ' drones')

    detect_pcs = (int(detect_pcs_gui.get()))
    logger.debug('detect pcs is ' + (str(detect_pcs)))

    pc_indy = (int(pc_indy_gui.get()))
    logger.debug('detect pc indy is ' + (str(pc_indy)))

    pc_barge = (int(pc_barge_gui.get()))
    logger.debug('detect pc barge is ' + (str(pc_barge)))

    pc_frig_dest = (int(pc_frig_dest_gui.get()))
    logger.debug('detect pc frig/dest is ' + (str(pc_frig_dest)))

    pc_capindy_freighter = (int(pc_capindy_freighter_gui.get()))
    logger.debug('detect pc capital indy/freighter is ' + (str(
        pc_capindy_freighter)))

    pc_cruiser_bc = (int(pc_cruiser_bc_gui.get()))
    logger.debug('detect pc cruiser/bc is ' + (str(
        pc_cruiser_bc)))

    pc_bs = (int(pc_bs_gui.get()))
    logger.debug('detect pc bs is ' + (str(pc_bs)))

    pc_rookie = (int(pc_rookie_gui.get()))
    logger.debug('detect pc rookie is ' + (str(pc_rookie)))

    pc_pod = (int(pc_pod_gui.get()))
    logger.debug('detect pc pod is ' + (str(pc_pod)))

    detect_npcs = (int(detect_npcs_gui.get()))
    logger.debug('detect npcs is ' + (str(detect_npcs)))

    npc_frig_dest = (int(npc_frig_dest_gui.get()))
    logger.debug('detect npc frig/dest is ' + (str(npc_frig_dest)))

    npc_cruiser_bc = (int(npc_cruiser_bc_gui.get()))
    logger.debug('detect npc cruiser/bc is ' + (str(npc_cruiser_bc)))

    npc_bs = (int(npc_bs_gui.get()))
    logger.debug('detect npc bs is ' + (str(npc_bs)))
    # gui.update()
    # t2 = threading.Thread(target=miner, args=[])
    # t2.start()
    miner()
    return


startbutton = tkinter.Button(text="start")
startbutton.grid(column=0, row=1, columnspan=3, sticky='N')
startbutton.bind("<ButtonRelease-1>", start)
startbutton.config(width='20', height='1', padx=25, pady=0)
'''
termbutton = tkinter.Button(text="stopper", command=stopper)
termbutton.grid(column=0, row=2, sticky='W')
termbutton.config(width='13', height='1')

stopbutton = tkinter.Button(text="runner", command=runner)
stopbutton.grid(column=1, row=1, columnspan=1, sticky='W')
stopbutton.config(width='13', height='1')

endrunbutton = tkinter.Button(text="checker", command=checker)
endrunbutton.grid(column=1, row=2, columnspan=1, sticky='W')
endrunbutton.config(width='13', height='1')
'''
'''
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
'''
'''
if __name__ == "__main__":
    # create Tk object instance
    app = simpleapp_tk(None)
    app.title('NEOMINER v0.1')
'''
    # setup logging handlers using the Tk instance created above
    # the pattern below can be used in other threads...
    # ...to allow other thread to send msgs to the gui
    # in this example, we set up two handlers just for demonstration (you could add a fileHandler, etc)
    # stderrHandler = logging.StreamHandler()  # no arguments => stderr
    # logger.addHandler(stderrHandler)
    # guiHandler = MyHandlerText(app.mytext)
    # logger.addHandler(guiHandler)
    #logger.setLevel(logging.DEBUG)

    # start Tk

# miner()
gui.title('NEOMINER v0.1')
gui.mainloop()
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

