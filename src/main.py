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
# import drones

# import src.docked
# import src.drones
from src import docked as doc, drones, navigation as nav, mining as mng, \
    bookmarks as bkmk, overview as o
from src.vars import system_mining, originx, originy, windowx, windowy

sys.setrecursionlimit(9999999)
playerfound = 0

# TERMINOLOGY ##################################################################

# A 'warning' is a persistent dialogue window that appears in the center of
# the screen and dims the rest of the screen. Warnings can only be dismissed
# with an explicit keystroke or button click from the user.

# A 'popup' is a partially transparent block of text that appears in the
# main play area for about five seconds.

# A 'site' is just shorthand for a user-set numbered bookmark that the ship can
# warp to, usually an asteroid belt.

################################################################################

# These variables are for the mining script only -------------------------------
# Total number of saved bookmark locations. This variable is set by the user.
total_sites = 10
# ------------------------------------------------------------------------------

# recommended per https://docs.python.org/2/library/logging.html
logger = logging.getLogger(__name__)


# logging.basicConfig(format='(%(levelno)s) %(asctime)s - %(funcName)s -- %('
# 'message)s', level=logging.DEBUG)


# MAIN SCRIPTS #################################################################

def miner():
    # Ores to mine, in order of priority.
    o1 = './img/overview/ore_types/plagioclase.bmp'
    o2 = './img/overview/ore_types/pyroxeres.bmp'
    o3 = './img/overview/ore_types/veldspar.bmp'
    o4 = './img/overview/ore_types/scordite.bmp'
    o5 = 0

    global playerfound
    global site
    # Number of 'runs' completed by the mining script. This will always start
    # as 1
    runs_var = 1
    timer_var = 0
    global npc_list, pc_list
    # Build the lists of ship icons to check for based on the user-specified
    # checkboxes in the GUI.
    (npc_list, pc_list) = o.build_ship_list(detect_npcs, npc_frig_dest,
                                            npc_cruiser_bc, detect_pcs, pc_indy,
                                            pc_barge, pc_frig_dest,
                                            pc_cruiser_bc, pc_bs,
                                            pc_capindy_freighter, pc_rookie,
                                            pc_pod)
    logging.info('beginning run ' + (str(runs_var)))
    while doc.is_docked() == 0:
        if drones.are_drones_launched() == 1:
            o.focus_client()
            drones.recall_drones(drone_num)
            site = 1
        if bkmk.iterate_through_bookmarks_rand(total_sites) == 1:
            # Once arrived at site, check for hostile npcs and human players.
            # If either exist, warp to another site.
            # If no hostiles npcs or players are present, check for asteroids.
            # If no asteroids exist,  warp to another site.
            if o.select_overview_tab('general') == 1:
                if o.look_for_ship(npc_list, pc_list) == 1:
                    miner()
            o.select_overview_tab('mining')
            target = o.look_for_targets(o1, o2, o3, o4, o5)
            while target != 0:
                drones.launch_drones(drone_num)
                if o.initiate_target_lock(target) == 0:
                    miner()
                mng.activate_miner(module_num)
                # If ship inventory isn't full, continue to mine ore and wait
                # for popups or errors.
                # Switch back to the general tab for easier ship detection
                o.select_overview_tab('general')
                while mng.ship_full_popup() == 0:
                    if mng.asteroid_depleted_popup() == 1:
                        o.select_overview_tab('mining')
                        target = o.look_for_targets(o1, o2, o3, o4, o5)
                        if target == 0:
                            miner()
                        elif target != 0:
                            if o.initiate_target_lock(target) == 0:
                                miner()
                            mng.activate_miner(module_num)
                            mng.ship_full_popup()
                            continue
                    if o.look_for_ship(npc_list, pc_list) == 1 or \
                            o.is_jammed(jam_var) == 1 or mng.time_at_site(
                        timer_var) == 1:
                        drones.recall_drones(drone_num)
                        miner()
                    timer_var += 1
                    time.sleep(1)

                if mng.ship_full_popup() == 1:
                    # Once inventory is full, dock at home station and unload.
                    drones.recall_drones(drone_num)
                    logging.info('finishing run ' + (str(runs_var)))
                    if system_mining == 0:
                        if bkmk.set_home() == 1:
                            if navigator() == 1:
                                doc.unload_ship()
                                doc.wait_for_undock()
                                playerfound = 0
                                time.sleep(3)
                                runs_var += 1
                                miner()
                    # If ship is mining in the same system it will dock in,
                    # a different set of functions is required.
                    elif system_mining == 1:
                        bkmk.dock_at_local_bookmark()
                        doc.unload_ship()
                        doc.wait_for_undock()
                        playerfound = 0
                        time.sleep(3)
                        runs_var += 1
                        miner()
                if target == 0:
                    logging.debug('no targets, restarting')
                    miner()
                    # bkmk.blacklist_local_bookmark()
        elif bkmk.iterate_through_bookmarks_rand(total_sites) == 0:
            nav.emergency_terminate()
            sys.exit(0)
    if doc.is_docked() == 1:
        # If docked when script starts, undock_loop.
        o.focus_client()
        doc.wait_for_undock()
        miner()


def navigator():
    """A standard warp-to-zero autopilot script. Warp to the destination, then
    terminate."""
    logging.debug('running navigator')
    nav.has_route()
    dockedcheck = doc.is_docked()

    while dockedcheck == 0:
        o.focus_overview()
        selectwaypoint = nav.warp_to_waypoint()
        while selectwaypoint == 1:  # Value of 1 indicates stargate waypoint.
            time.sleep(5)  # Wait for jump to begin.
            detectjump = nav.wait_for_jump()
            if detectjump == 1:
                selectwaypoint = nav.warp_to_waypoint()
            else:
                logging.critical('error detecting jump')
                nav.emergency_terminate()
                traceback.print_exc()
                traceback.print_stack()
                sys.exit()

        while selectwaypoint == 2:  # Value of 2 indicates a station waypoint.
            time.sleep(5)
            detectdock = nav.wait_for_dock()
            if detectdock == 1:
                logging.info('arrived at destination')
                return 1
        else:
            logging.warning('likely at destination')
            return 1

    while dockedcheck == 1:
        doc.wait_for_undock()
        time.sleep(5)
        navigator()


def collector():
    """Haul all items from a predetermined list of stations to a single 'home'
    station, as specified by the user. The home station is identified by a
    station bookmark beginning with '000', while the remote stations are any
    station bookmark beginning with the numbers 1-9. This means up to 10
    remote stations are supported."""
    logging.debug('running collector')
    dockedcheck = doc.is_docked()
    while dockedcheck == 0:
        selectwaypoint = nav.warp_to_waypoint()

        while selectwaypoint == 1:
            time.sleep(3)  # Wait for warp to start.
            detectjump = nav.wait_for_jump()
            if detectjump == 1:
                selectwaypoint = nav.warp_to_waypoint()
        while selectwaypoint == 2:
            time.sleep(3)
            detectdock = nav.wait_for_dock()
            if detectdock == 1:
                collector()
        else:
            logging.critical('error with at_dest_check_var and '
                             'at_home_check_var')
            traceback.print_exc()
            traceback.print_stack()
            sys.exit()

    while dockedcheck == 1:
        athomecheck = bkmk.is_home()
        # If docked at home station, set a destination waypoint to a remote
        # station and unload cargo from ship into home station inventory.
        if athomecheck == 1:
            doc.unload_ship()
            bkmk.set_dest()
            doc.wait_for_undock()
            collector()
        elif athomecheck == 0:
            logging.debug('not at home')
            loadship = doc.load_ship()
            logging.debug('loadship is ' + (str(loadship)))

            if loadship == 2 or loadship == 0 or loadship is None:
                atdestnum = bkmk.detect_bookmark_location()
                if atdestnum == -1:
                    doc.wait_for_undock()
                    collector()
                else:
                    bkmk.set_dest()
                    bkmk.blacklist_station()
                    doc.wait_for_undock()
                    collector()
            elif loadship == 1:  # Value of 1 indicates ship is full.
                bkmk.set_home()
                doc.wait_for_undock()
                collector()

        else:
            logging.critical('error with detect_at_home and at_dest_check')
            traceback.print_exc()
            traceback.print_stack()
            sys.exit()
    if dockedcheck is None:
        collector()


print("originx =", originx)
print("originy =", originy)
print("windowx =", windowx)
print("windowy =", windowy)


# GUI #########################################################################


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

detect_jam_gui = tkinter.IntVar()
detect_jam_gui.set(1)

t = tkinter.Label(text="")
t.grid(column=0, row=0, columnspan=2, sticky='W', padx=0, pady=0)

t = tkinter.Label(text="")
t.grid(column=0, row=3, columnspan=2, sticky='W', padx=0, pady=0)

combo_modules = ttk.Combobox(values=[1, 2, 3, 4])
combo_modules.current(1)
combo_modules.grid(column=1, row=4, columnspan=1, sticky='W')
combo_modules.config(width='4', height='10')
label_mininglasers = tkinter.Label(text="mining lasers")
label_mininglasers.grid(column=0, row=4, columnspan=1, sticky='W', padx=20)

combo_drones = ttk.Combobox(values=[0, 1, 2, 3, 4, 5])
combo_drones.current(2)
combo_drones.grid(column=1, row=5, columnspan=1, sticky='W')
combo_drones.config(width='4', height='10')
label_drones = tkinter.Label(text="drones")
label_drones.grid(column=0, row=5, columnspan=1, sticky='W', padx=20, pady=5)

detect_pcs = tkinter.Checkbutton(text='pc check', variable=detect_pcs_gui)
detect_pcs.grid(column=0, row=6, columnspan=1, sticky='W')

pc_indy = tkinter.Checkbutton(text='pc indy check', variable=pc_indy_gui)
pc_indy.grid(column=1, row=6, columnspan=1, sticky='W')

pc_barge = tkinter.Checkbutton(text='pc barge check', variable=pc_barge_gui)
pc_barge.grid(column=0, row=7, columnspan=1, sticky='W')

pc_frig_dest = tkinter.Checkbutton(text='pc frig/dest check',
                                   variable=pc_frig_dest_gui)
pc_frig_dest.grid(column=1, row=7, columnspan=1, sticky='W')

pc_capindy_freighter = tkinter.Checkbutton(text='pc capindy/freighter check',
                                           variable=pc_capindy_freighter_gui)
pc_capindy_freighter.grid(column=0, row=8, columnspan=1, sticky='W')

pc_cruiser_bc = tkinter.Checkbutton(text='pc cruiser/bc check',
                                    variable=pc_cruiser_bc_gui)
pc_cruiser_bc.grid(column=1, row=8, columnspan=1, sticky='W')

pc_bs = tkinter.Checkbutton(text='pc bs check', variable=pc_bs_gui)
pc_bs.grid(column=0, row=9, columnspan=1, sticky='W')

pc_rookie = tkinter.Checkbutton(text='pc rookie check', variable=pc_rookie_gui)
pc_rookie.grid(column=1, row=9, columnspan=1, sticky='W')

pc_pod = tkinter.Checkbutton(text='pc pod check', variable=pc_pod_gui)
pc_pod.grid(column=0, row=10, columnspan=1, sticky='W')

t = tkinter.Label(text="")
t.grid(column=0, row=11, columnspan=2, sticky='W', padx=0, pady=0)

detect_npcs = tkinter.Checkbutton(text='npc check', variable=detect_npcs_gui)
detect_npcs.grid(column=0, row=12, columnspan=1, sticky='W')

npc_frig_dest = tkinter.Checkbutton(text='npc frig/dest check',
                                    variable=npc_frig_dest_gui)
npc_frig_dest.grid(column=1, row=12, columnspan=1, sticky='W')

npc_cruiser_bc = tkinter.Checkbutton(text='npc bs check',
                                     variable=npc_cruiser_bc_gui)
npc_cruiser_bc.grid(column=0, row=13, columnspan=1, sticky='W')


# self.npc_bs = tkinter.Checkbutton(self, text='npc bs check',
#                                    variable=npc_bs_gui)
# self.npc_bs.grid(column=1, row=10, columnspan=1, sticky='W')

t = tkinter.Label(text="")
t.grid(column=0, row=14, columnspan=2, sticky='W', padx=0, pady=0)

detect_jam = tkinter.Checkbutton(text='ecm jamming check',
                                 variable=detect_jam_gui)
detect_jam.grid(column=0, row=15, columnspan=1, sticky='W')

t = tkinter.Label(text="")
t.grid(column=0, row=16, columnspan=2, sticky='W', padx=0, pady=0)


def start(event):
    global drone_num, module_num, jam_var

    global detect_pcs, pc_indy, pc_barge, pc_frig_dest, \
        pc_capindy_freighter, pc_cruiser_bc, pc_bs, pc_rookie, pc_pod

    global detect_npcs, npc_frig_dest, npc_cruiser_bc, npc_bs

    module_num = (int(combo_modules.get()))
    drone_num = (int(combo_drones.get()))
    logger.debug((str(module_num)) + ' modules')
    logger.debug((str(drone_num)) + ' drones')

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
    logger.debug('detect pc cruiser/bc is ' + (str(pc_cruiser_bc)))

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

    jam_var = (int(detect_jam_gui.get()))
    logger.debug('detect ecm jamming is ' + (str(detect_jam)))

    miner()
    return


startbutton = tkinter.Button(text="start")
startbutton.grid(column=0, row=1, columnspan=2)
startbutton.bind("<ButtonRelease-1>", start)
startbutton.config(width='10', height='1', padx=5, pady=0)
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
