from tkinter import *
from tkinter import messagebox
import time


class Field:
    def __init__(self):
        self.tree = BinaryTree()
        self.x = 500
        self.y = 30
        self.w = 25
        self.allid = []
        self.data = []
        self.same = []
        self.color = '#00FFFF'
        self.tk = Tk()
        self.tk.title('Binary Tree')
        self.tk.resizable(0, 0)
        self.canvas = Canvas(self.tk, width=1024, height=900, bg='white')
        self.canvas.grid(row=0, column=0)
        self.tk.columnconfigure(0, weight=1)
        self.tk.columnconfigure(1, weight=1)

        self.create = Button(self.tk, text='Create', command=lambda: self.creation(), font='Calibri 24')
        self.create.grid(row=1, column=0, sticky='e')
        self.entry = Entry(self.tk, font='Calibri 24', validate="key")
        self.entry['validatecommand'] = (self.entry.register(testVal), '%P', '%d')
        self.entry.grid(row=1, column=1)

        self.findel = Button(self.tk, text='Find', font='Calibri 24', command=lambda: self.find())
        self.findel.grid(row=2, column=0, sticky='e')
        self.el = Entry(self.tk, font='Calibri 24', validate="key")
        self.el['validatecommand'] = (self.el.register(testVal), '%P', '%d')
        self.el.grid(row=2, column=1)

        self.delete_node = Button(self.tk, text='Del', font='Calibri 24', command=lambda: self.get_rid_of_node())
        self.delete_node.grid(row=3, column=0, sticky='e')
        self.d = Entry(self.tk, font='Calibri 24', validate="key")
        self.d['validatecommand'] = (self.d.register(testVal), '%P', '%d')
        self.d.grid(row=3, column=1)

    def creation(self):
        value = int(self.entry.get())
        self.entry.delete(0, 'end')
        if value in self.same:
            messagebox.showwarning("ЭЭЭэээээ", "Такой элемент уже есть!")
        else:
            self.same.append(value)
            pos = self.tree.insert(value)
            y = 75 * pos + self.y
            node = self.tree.binSearch(value)
            if node is not None:
                data = self.tree.check_pos(node)
                x = 512
                new = 256
                for i in data:
                    if i == 'r':
                        x += new
                    else:
                        x -= new
                    new //= 2

                ob = self.canvas.create_oval(x - self.w,
                                             y - self.w,
                                             x + self.w,
                                             y + self.w,
                                             fill='#00FFFF')

                node.cords = [x, y]
                node.id = ob
                self.allid.append(ob)
                self.data.append(ob)
                self.canvas.create_text(x, y, text=str(value), font=("Calibri", 18))
                self.allid.append(ob + 1)
                if value != self.tree.root.value:
                    x0, y0 = node.cords
                    x1, y1 = node.parent.cords
                    line = self.canvas.create_line(x0, y0, x1, y1, width=4)
                    self.allid.append(line)
                    if node.parent.right is not None:
                        if node.parent.right.value == node.value:
                            node.parent.lineright = line
                    if node.parent.left is not None:
                        if node.parent.left.value == node.value:
                            node.parent.lineleft = line

                    node.lineparent = line
                    self.canvas.lower(line)
                    self.canvas.lower(line)
                    self.tk.update()

    def find(self):
        sought = int(self.el.get())
        self.el.delete(0, 'end')
        if sought not in self.same:
            messagebox.showwarning("ЭЭЭэээээ", "Такого вообще нет!")
        else:
            node = self.tree.binSearch(sought)
            locid = node.id
            for i in range(3):
                self.canvas.itemconfig(locid, fill='#80FF80')
                self.tk.update()
                time.sleep(0.4)
                self.canvas.itemconfig(locid, fill=self.color)
                self.tk.update()
                time.sleep(0.5)
        self.tk.update()

    def get_rid_of_node(self):
        num = int(self.d.get())
        self.d.delete(0, 'end')
        if num not in self.same:
            messagebox.showwarning("ЭЭЭэээээ", "Такого вообще нет!")
        else:
            local = self.tree.binSearch(num)
            loc = local.id
            self.same = []
            for i in range(2):
                self.canvas.itemconfig(loc, fill='Red')
                self.tk.update()
                time.sleep(0.5)
                self.canvas.itemconfig(loc, fill=self.color)
                self.tk.update()
                time.sleep(0.4)
            data = self.tree.delete(num)
            for i in self.allid:
                self.canvas.delete(i)
            self.tree = BinaryTree()
            for value in data:
                self.same.append(value)
                pos = self.tree.insert(value)
                y = 75 * pos + self.y
                node = self.tree.binSearch(value)
                if node is not None:
                    data = self.tree.check_pos(node)
                    x = 512
                    new = 256
                    for i in data:
                        if i == 'r':
                            x += new
                        else:
                            x -= new
                        new //= 2

                    ob = self.canvas.create_oval(x - self.w,
                                                 y - self.w,
                                                 x + self.w,
                                                 y + self.w,
                                                 fill='#00FFFF')

                    node.cords = [x, y]
                    node.id = ob
                    self.allid.append(ob)
                    self.data.append(ob)
                    self.canvas.create_text(x, y, text=str(value), font=("Calibri", 18))
                    self.allid.append(ob + 1)

                    if value != self.tree.root.value:
                        x0, y0 = node.cords
                        x1, y1 = node.parent.cords
                        line = self.canvas.create_line(x0, y0, x1, y1, width=4)
                        self.allid.append(line)
                        if node.parent.right is not None:
                            if node.parent.right.value == node.value:
                                node.parent.lineright = line
                        if node.parent.left is not None:
                            if node.parent.left.value == node.value:
                                node.parent.lineleft = line
                        node.lineparent = line
                        self.canvas.lower(line)
                        self.canvas.lower(line)

            self.tk.update()


class Node:
    def __init__(self, value, left_child=None, right_child=None, parent=None):
        self.value = value
        self.left = left_child
        self.right = right_child
        self.parent = parent
        self.cords = [0, 0]
        self.id = 0
        self.lineleft = 0
        self.lineright = 0
        self.lineparent = 0


class BinaryTree:
    def __init__(self):
        self.root = None
        self.size = 0
        self.array = []

    def insert(self, value):
        node = Node(value)
        y = None
        x = self.root
        cnt = 0
        while x is not None:
            y = x
            cnt += 1
            if node.value < x.value:
                x = x.left
            else:
                x = x.right
        node.parent = y
        self.array.append(value)
        if y is None:
            self.root = node
        elif node.value < y.value:
            y.left = node
        else:
            y.right = node
        return cnt

    def delete(self, value):
        if value in self.array:
            self.array.remove(value)
            return self.array

    def binSearch(self, sought):
        if self.root is not None:
            return self._binSearch(self.root, sought)

    def _binSearch(self, cur_node, sought):
        if cur_node is not None:
            if cur_node.value == sought:
                return cur_node
            if cur_node.value > sought:
                return self._binSearch(cur_node.left, sought)
            else:
                return self._binSearch(cur_node.right, sought)
        else:
            return None

    def check_pos(self, cur_node):
        data = []
        if cur_node is not None:
            while cur_node.parent is not None:
                if cur_node.parent.left is not None:
                    if cur_node.value == cur_node.parent.left.value:
                        data.append('l')
                if cur_node.parent.right is not None:
                    if cur_node.value == cur_node.parent.right.value:
                        data.append('r')
                cur_node = cur_node.parent
            return data[::-1]


def testVal(inStr, acttyp):
    if acttyp == '1':
        if not inStr.isdigit():
            return False
    return True


test = Field()
test.tk.mainloop()
