import time
import threading
import logging
try:
    import tkinter as tk # Python 3.x
    import tkinter.scrolledtext as ScrolledText
except ImportError:
    import Tkinter as tk # Python 2.x
    import ScrolledText

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


class Frame1(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="red")
        self.parent = parent
        self.widgets()
        self.mainWidgets()

    def widgets(self):
        self.text = tk.Text(self)
        self.text.insert(tk.INSERT, "Hello World\t")
        self.text.insert(tk.END, "This is the first frame")
        self.text.grid(row=0, column=0, padx=20, pady=20) # margins

    def mainWidgets(self):

        self.label1 = tk.Label(self, text="Main window label", bg="green")
        self.label1.grid(row=3, column=0)

        self.label2 = tk.Label(self, text="Main window label", bg="yellow")
        self.label2.grid(row=4, column=0)

        self.window = tk.Frame1(self)
        self.window.grid(row=5, column=10, rowspan=2)

class myGUI(tk.Frame):

    # This class defines the graphical user interface 

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.build_gui()
        self.mainWidgets()
    
    def mainWidgets(self):

        self.label1 = tk.Label(self, text="Main window label", bg="green")
        self.label1.grid(row=3, column=0)

        self.label2 = tk.Label(self, text="Main window label", bg="yellow")
        self.label2.grid(row=4, column=0)

        #self.window = mainWidgets(self)
        #self.window.grid(row=5, column=10, rowspan=2)

    def build_gui(self):                    
        # Build GUI
        self.root.title('TEST')
        self.root.option_add('*tearOff', 'FALSE')
        self.grid(column=0, row=1, sticky='s', padx=10, pady=30)
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_columnconfigure(1, weight=1, uniform='a')
        self.grid_columnconfigure(2, weight=1, uniform='a')
        self.grid_columnconfigure(3, weight=1, uniform='a')

        # Add text widget to display logging info
        st = ScrolledText.ScrolledText(self, state='disabled')
        st.configure(font='TkFixedFont')
        st.grid(column=0, row=2, sticky='s', columnspan=4)

        # Create textLogger
        text_handler = TextHandler(st)

        # Logging configuration
        logging.basicConfig(filename='test.log',
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s - %(message)s')        

        # Add the handler to logger
        logger = logging.getLogger()        
        logger.addHandler(text_handler)

def worker():
    # Skeleton worker function, runs in separate thread (see below)   
    while True:
        # Report time / date at 2-second intervals
        time.sleep(2)
        timeStr = time.asctime()
        msg = 'Current time: ' + timeStr
        logging.info(msg) 

def main():

    root = tk.Tk()
    myGUI(root)
    #Frame1(root)

    t1 = threading.Thread(target=worker, args=[])
    t1.start()

    root.mainloop()
    t1.join()

main()
