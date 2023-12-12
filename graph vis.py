from tkinter import *


class Graph:
    def __init__(self):
        self.w = 40
        self.color = '#00FFFF'
        self.idGraph = []
        self.coords = []
        self.q = []
        self.idLine = []
        self.connect = []
        self.queue = []
        pass

    def createBoard(self):
        self.tk = Tk()
        self.tk.title('Graph')
        self.tk.resizable(0, 0)
        self.canvas = Canvas(self.tk, width=1000, height=1000, bg='white')
        self.canvas.pack()

        self.tk.bind('<ButtonRelease-3>', lambda event: self.click(event))
        self.tk.bind('<ButtonRelease-2>', lambda event: self.lines(event))
        self.tk.bind('<B1-Motion>', lambda event: self.dragNode(event))

    def back(self):
        if self.queue[-1] == 'node':
            self.canvas.delete(self.idGraph[-1])
            self.connect[-1] = []
        else:
            self.canvas.delete(self.idLine[-1])

    def click(self, event):
        x = event.x
        y = event.y

        a = self.canvas.create_oval(x - self.w, y - self.w,
                                    x + self.w, y + self.w,
                                    fill=self.color)
        self.idGraph.append(a)
        self.coords.append([x, y])
        self.canvas.create_text(x, y, text=len(self.idGraph) - 1,
                                fill='Black', font=("Calibri", 18))
        self.connect.append([])
        self.connect[-1].append(a)
        self.queue.append('node')

    def lines(self, event):
        x = event.x
        y = event.y
        if len(self.q) >= 2:
            self.q = []
        self.q.append((x, y))
        flag, pos = self.isNode(x, y)

        if flag:
            self.canvas.itemconfig(self.connect[pos][0], fill='#ADFF2F')

        if len(self.q) == 2:
            flag, pos = self.isNode(self.q[0][0], self.q[0][1])
            flag2, pos2 = self.isNode(self.q[1][0], self.q[1][1])
            if flag and flag2:
                if pos == pos2:
                    self.canvas.itemconfig(self.connect[pos][0], fill=self.color)
                else:
                    self.drawline(self.q, pos, pos2)

    def drawline(self, data, id1, id2):
        a = []
        for i in data:
            flag, pos = self.isNode(i[0], i[1])
            if flag:
                a.append(pos)

        if len(a) == 2:
            self.canvas.itemconfig(self.connect[id1][0], fill='#00FFFF')
            self.canvas.itemconfig(self.connect[id2][0], fill='#00FFFF')
            num = (self.canvas.create_line(self.coords[a[0]][0],
                                           self.coords[a[0]][1],
                                           self.coords[a[1]][0],
                                           self.coords[a[1]][1], width=5))
            self.idLine.append(num)
            self.connect[a[0]].append(num)
            self.connect[a[1]].append(num)
            self.canvas.lower(self.idLine[-1])
            self.queue.append('line')

            # print(self.connect)

    def dragNode(self, event):
        x = event.x
        y = event.y
        flag, pos = self.isNode(x, y)
        if flag:
            x = self.tk.winfo_pointerx()
            y = self.tk.winfo_pointery()
            abs_coord_x = x - self.tk.winfo_rootx()
            abs_coord_y = y - self.tk.winfo_rooty()

            self.canvas.move(self.connect[pos][0], abs_coord_x - self.coords[pos][0],
                             abs_coord_y - self.coords[pos][1])
            self.canvas.move(self.connect[pos][0] + 1, abs_coord_x - self.coords[pos][0],
                             abs_coord_y - self.coords[pos][1])

            self.coords[pos][0] = abs_coord_x
            self.coords[pos][1] = abs_coord_y

            data = self.connect[pos][1:]
            local = []
            for i in range(len(data)):
                for j in range(len(self.connect)):
                    if j != pos:
                        if data[i] in self.connect[j]:
                            local.append(self.connect[j][0])
            new = []
            for i in range(len(local)):
                for j in range(len(self.idGraph)):
                    if local[i] == self.idGraph[j]:
                        new.append(self.coords[j])
                        break

            for i in range(len(data)):
                self.canvas.coords(data[i], new[i][0], new[i][1], abs_coord_x, abs_coord_y)

    def isNode(self, x, y):
        pos = -1
        for dot, element in enumerate(self.coords):
            if element[0] - self.w < x < self.w + element[0]:
                if element[1] - self.w < y < self.w + element[1]:
                    pos = dot
        if pos == -1:
            return False, None
        return True, pos

    def printmatrix(self):
        n = len(self.idGraph)
        data = [[0] * n for i in range(n)]
        for i in range(len(self.connect)):
            loc = self.connect[i][1:]
            for line in range(len(loc)):
                for idNode in range(len(self.connect)):
                    if idNode != i:
                        if loc[line] in self.connect[idNode][1:]:
                            x = self.connect[idNode][0]
                            for num in range(len(self.idGraph)):
                                if self.idGraph[num] == x:
                                    data[i][num] = 1
                                    data[num][i] = 1

        return data

def matrix():
    data = graph.printmatrix()
    file = open('graph.txt', 'w+')
    for i in data:
        a = list(map(str, i))
        file.write(' '.join(a) + '\n')
    file.close()


graph = Graph()
graph.createBoard()

button = Button(graph.tk, command= lambda : matrix(), text='Print Matrix')
button.pack()

graph.tk.mainloop()
