import tkinter as tk  # for python 3
import pygubu


class Application:
    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('gui.ui')
        self.mainwindow = builder.get_object('main_window', master)
        builder.connect_callbacks(self)

    def start_button_click(self):
        print('hello world')



if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
