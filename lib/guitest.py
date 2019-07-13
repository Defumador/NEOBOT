'''
from tkinter import *
import logging
import time
from threading import Thread


def test():
    logger = logging.getLogger(
        'print_stuff')  # will inherit "root" logger settings
    logger.info('This will now show')
    print('test132')


class IODirector(object):
    def __init__(self, text_area):
        self.text_area = text_area


class StdoutDirector(IODirector):
    def write(self, msg):
        self.text_area.insert(END, msg)

    def flush(self):
        pass


class App(Frame):
    def __init__(self, master):
        self.master = master
        Frame.__init__(self, master, relief=SUNKEN, bd=2)
        self.start()

    def start(self):
        self.master.title("Test")
        self.submit = Button(self.master, text='Run', command=self.do_run,
                             fg="red")
        self.submit.grid(row=1, column=2)
        self.text_area = Text(self.master, height=2.5, width=30,
                              bg='light cyan')
        self.text_area.grid(row=1, column=1)

    def do_run(self):
        t = Thread(target=print_stuff)
        sys.stdout = StdoutDirector(self.text_area)
        # configure the nameless "root" logger to also write           # added
        # to the redirected sys.stdout                                 # added
        logger = logging.getLogger()  # added
        console = logging.StreamHandler(stream=sys.stdout)  # added
        logger.addHandler(console)  # added
        t.start()


def print_stuff():
    logger = logging.getLogger(
        'print_stuff')  # will inherit "root" logger settings
    logger.info('This will now show')  # changed
    print('This will show')
    time.sleep(3)
    test()


def print_some_other_stuff():
    logger = logging.getLogger(
        'print_some_other_stuff')  # will inherit "root" logger settings
    logger.info('This will also now show')  # changed
    print('This will also show')


def main():
    logging.basicConfig(level=logging.INFO)  # enable logging           # added
    root = Tk()
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
'''
