import tkinter as tk
import functools

import zarf

class InputBar(tk.Entry):
    def __init__(self, root):
        self.root = root       
        sv = tk.StringVar()
        tk.Entry.__init__(self, root, textvariable=sv)
        self.sv = sv
        self.grid(row=0+root.gui_count+1, column=0, columnspan=3)

class Button(tk.Radiobutton):
    def __init__(self, root, text, var, col):
        tk.Radiobutton.__init__(self, root, text=text, variable=var, indicatoron=True, value=col)
        self.root = root
        self.grid(row=1+root.gui_count, column=col+3)
            
class Zarf(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.inputs = []
        self.buttons = []
        self.radios = []
        self.minusButtons = []
        #things that only happen once
        self.plusButton = tk.Button(self, text="+", command=self._init_gui)
        self.plusButton.grid(row=0, column=4)
        self.resultBox = tk.Text(self, font=("Courier", 12))
        self.resultBox.grid(row=2, column=1)
        self.resultBox.config(state=tk.DISABLED)
        self.gui_count = 0
        self._init_gui()
        self.bind("<Return>", lambda e: self.solve())

        
    def _init_gui(self):
        self.gui_count += 1
        self.inputs.append(InputBar(self))
        self.buttons.append([])
        self.radios.append(tk.IntVar())
        self.radios[-1].set(2) #starts at build
        for col, text in enumerate(['Pattern', 'Anagram', 'Build']):
            self.buttons[-1].append(Button(self, text, self.radios[-1], col))
        self.resultBox.grid(row=2+self.gui_count, column=1)
        
        minusButton = tk.Button(self, text="-", command=functools.partial(self._destroy_gui, self.gui_count))
        minusButton.grid(row=self.gui_count+1, column=6)
        self.minusButtons.append(minusButton)
        
    def _destroy_gui(self, num):
        for i in self.buttons[num-1]:
            i.grid_forget()
        self.radios[num-1].set(3) #illegal :)
        self.minusButtons[num-1].grid_forget()
        self.inputs[num-1].grid_forget()
        self.inputs[num-1].sv.set("")
        
    def resultSet(self, text):
        self.resultBox.config(state=tk.NORMAL)
        self.resultBox.delete(1.0, tk.END)
        self.resultBox.insert(tk.END, text)
        self.resultBox.config(state=tk.DISABLED)
        
    def solve(self):
        modes = list(filter(lambda i:i!= 'NA', [['p', 'a', 'b', 'NA'][radio.get()] for radio in self.radios]))
        racks = list(filter(lambda i: bool(i), [entry.get().upper() for entry in self.inputs]))
        self.resultSet(zarf.multisearch(modes, racks))

z = Zarf()
z.mainloop()
