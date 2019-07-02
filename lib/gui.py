from tkinter import *
from tkinter.ttk import *
import tkinter.scrolledtext as ScrolledText
import tkinter as tk
import logging

window = Tk()
window.title("NEOBOT")
miner_modules = IntVar()

# Set number of miner modules (miner script only)
rad1 = Radiobutton(window, text='1', value=1, variable=miner_modules)
rad2 = Radiobutton(window, text='2', value=2, variable=miner_modules)
rad3 = Radiobutton(window, text='3', value=3, variable=miner_modules)
rad4 = Radiobutton(window, text='4', value=4, variable=miner_modules)
rad1.grid(column=1, row=1)
rad2.grid(column=2, row=1)
rad3.grid(column=3, row=1)
rad4.grid(column=4, row=1)

# Script selection
script = Combobox(window)
script['values'] = ("Miner", "Autopilot", "Collector")
script.current(0)  # set the default selected item
script.grid(column=0, row=0)


class TextHandler(logging.Handler):
    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tk.END)

        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)


class myGUI(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.build_gui()

    def build_gui(self):
        # Build GUI
        self.root.title('TEST')
        self.root.option_add('*tearOff', 'FALSE')
        self.grid(column=0, row=0, sticky='ew')
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_columnconfigure(1, weight=1, uniform='a')
        self.grid_columnconfigure(2, weight=1, uniform='a')
        self.grid_columnconfigure(3, weight=1, uniform='a')

        # Add text widget to display logging info
        st = ScrolledText.ScrolledText(self, state='disabled')
        st.configure(font='TkFixedFont')
        st.grid(column=0, row=1, sticky='w', columnspan=3)

        # Create textLogger
        text_handler = TextHandler(st)

        # Logging configuration
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        # Add the handler to logger
        logger = logging.getLogger()
        logger.addHandler(text_handler)


def start():
    if script.get() == "Miner":
        logging.info('selected ' + script.get())

        logging.info((str(miner_modules.get())) + ' mining module(s)')
        script_var = script.get()
        modules_var = miner_modules.get()

    elif script.get() == "Autopilot":
        logging.info('selected ' + script.get())
        script_var = script.get()

    elif script.get() == "Collector":
        logging.info('selected ' + script.get())
        script_var = script.get()


def main():
    root = tk.Tk()
    myGUI(root)

    btn = Button(window, text="Start", command=start)
    btn.grid(column=2, row=3)

    root.mainloop()


main()

"""
OLD GUI BASED ON PYGUBU

import traceback
import sys
import os
import threading

import tkinter as tk  # for python 3
import pygubu

from lib import main


class Application:
    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('gui.ui')
        self.mainwindow = builder.get_object('main_window', master)
        builder.connect_callbacks(self)

    def start_button_click(self):
        threading.Thread(main.collector())

    def stop_button_click(self):
        raise SystemExit

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
"""
