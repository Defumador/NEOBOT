from tkinter import ttk
import time
import threading
import logging
try:
    import tkinter as tk # Python 3.x
    import tkinter.scrolledtext as ScrolledText
except ImportError:
    import Tkinter as tk # Python 2.x
    import ScrolledText




'''
class TextHandler(logging.Handler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

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
'''

class myGUI(tk.Frame):

    # This class defines the graphical user interface 

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        #self.build_gui()
        self.mainWidgets()
    
    def mainWidgets(self):
        #global dynamiclabel
        #dynamiclabel = tk.StringVar()
        #dynamiclabel.set("this label updates upon change")
        global lab
        lab = tk.Label(text='test1')
        lab.grid(column=1, row=7, columnspan=1, sticky='W', padx=20)
        
        #self.label1 = tk.Label(self, text="Main window label", bg="green")
        #self.label1.grid(row=3, column=0)

        #self.label2 = tk.Label(self, text="Main window label", bg="yellow")
        #self.label2.grid(row=4, column=0)

        startbutton = tk.Button(text="start", command=start)
        startbutton.grid(column=0, row=1, columnspan=2)
        #startbutton.bind("<ButtonRelease-1>", start)
        startbutton.config(width='10', height='1', padx=5, pady=0)

        combo_modules = ttk.Combobox(values=[1, 2, 3, 4])
        combo_modules.current(1)
        combo_modules.grid(column=1, row=4, columnspan=1, sticky='W')
        combo_modules.config(width='4', height='10')
        label_mininglasers = tk.Label(text="mining lasers")
        label_mininglasers.grid(column=0, row=4, columnspan=1, sticky='W', padx=20)

        combo_drones = ttk.Combobox(values=[0, 1, 2, 3, 4, 5])
        combo_drones.current(2)
        combo_drones.grid(column=1, row=5, columnspan=1, sticky='W')
        combo_drones.config(width='4', height='10')
        label_drones = tk.Label(text="drones")
        label_drones.grid(column=0, row=5, columnspan=1, sticky='W', padx=20, pady=5)

        detect_pcs = tk.Checkbutton(text='pc check')
        detect_pcs.grid(column=0, row=6, columnspan=1, sticky='W')

        pc_indy = tk.Checkbutton(text='pc indy check')
        pc_indy.grid(column=1, row=6, columnspan=1, sticky='W')

        pc_barge = tk.Checkbutton(text='pc barge check')
        pc_barge.grid(column=0, row=7, columnspan=1, sticky='W')

        #pc_frig_dest = tk.Checkbutton(text='pc frig/dest check')
        #pc_frig_dest.grid(column=1, row=7, columnspan=1, sticky='W')
        #self.window = mainWidgets(self)
        #self.window.grid(row=5, column=10, rowspan=2)
                       
        # Build GUI
        self.root.title('TEST')
        '''
        self.root.option_add('*tearOff', 'FALSE')
        self.grid(column=0, row=0, sticky='ew', padx=10, pady=5, columnspan=100)
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_columnconfigure(1, weight=1, uniform='a')
        self.grid_columnconfigure(2, weight=1, uniform='a')
        self.grid_columnconfigure(3, weight=1, uniform='a')

        # Add text widget to display logging info
        st = ScrolledText.ScrolledText(self, state='normal')
        st.configure(font='TkFixedFont')
        st.grid(column=0, row=2, sticky='ew', columnspan=100)
        st.config(width='60', height='10')

        # Create textLogger
        text_handler = TextHandler(st)

        # Logging configuration
        logging.basicConfig(filename='test.log',
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s - %(message)s')        

        # Add the handler to logger
        logger = logging.getLogger()        
        logger.addHandler(text_handler)
     '''


def start():
  global lab
  lab.configure(text="star123ted")
  lab.update()

  time.sleep(1)

  #logging.info('hellooo121212')
  #root1 = tk.Tk()
  #root1.update()

  time.sleep(1)

  lab.configure(text="star12323ted")
  lab.update()

  time.sleep(1)

  lab.configure(text="star12334343323ted")
  lab.update()
  return

def main():

  root = tk.Tk()
  myGUI(root)
    #Frame1(root)

   # t1 = threading.Thread(target=worker, args=[])
   # t1.start()

  root.mainloop()
   # t1.join()

main()

