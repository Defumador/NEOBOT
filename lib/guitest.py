import tkinter as tk

def cbc(id, tex):
    return lambda : callback(id, tex)

def callback(id, tex):
    s = 'At {} f is {}\n'.format(id, id**id/0.987)
    tex.insert(tk.END, s)
    tex.see(tk.END)             # Scroll if necessary

top = tk.Tk()
tex = tk.Text(master=top)
tex.pack(side=tk.RIGHT)
#bop = tk.Frame()
#bop.pack(side=tk.LEFT)
for k in range(1,10):
    tv = 'Say {}'.format(k)
    #b = tk.Button(bop, text=tv, command=cbc(k, tex))
    #b.pack()

#tk.Button(bop, text='Exit', command=top.destroy).pack()
top.mainloop()