from tkinter import *
import time

def create_board(row, col, color, w):
    
    for i in range(row):
        id_array.append([])
        for j in range(col):
            id_array[i].append(canvas.create_rectangle(j*w,
                                    i*w,
                                    (j+1)*w,
                                    w*(i+1),
                                    fill = color))
            time.sleep(0.001)
            tk.update()
    return id_array

def l_click(event, id_array, w):
    if len(coords) >= 4:
        cleaning(id_array, data_x, data_y, coords, 20, 20)
    x_start = event.x // w
    y_start = event.y // w
    
    canvas.itemconfig(id_array[y_start][x_start], fill = 'green')
    coords.append(x_start)
    coords.append(y_start)
    if len(coords) == 4:
        bresenham(coords[0], coords[2], coords[1], coords[3])
        
def line(data_x, data_y, id_array):
    for i in range(len(data_x)):
        canvas.itemconfig(id_array[data_y[i]][data_x[i]], fill = 'green')

def cleaning(id_array, data_x, data_y, coords, row, col):
    for i in range(row):
        for j in range(col):
            canvas.itemconfig(id_array[i][j], fill = 'grey')
    data_x.clear()
    data_y.clear() 
    coords.clear()
    
def bresenham(x0, x1, y0, y1):
    print(coords)

    dE = (y1 - y0)/(x1 - x0)
    E = 0
    
    data_x = []
    data_y = []
    print(coords)
    if dE <= 1 and dE >= -1:
        if x1 < x0:
            y1, y0 = y0, y1
            x1, x0 = x0, x1
        y = y0
        for i in range(x0, x1 + 1, 1):
            data_x.append(i)
            if E >= 0.5:
                y += 1
                E -= 1
                data_y.append(y)
            elif E <= -0.5:
                y -= 1
                E += 1
                data_y.append(y)
            else:
                data_y.append(y)
            E += dE
        
    else:
        if y1 < y0:
            y1, y0 = y0, y1
            x1, x0 = x0, x1
        dE = (x1 - x0)/(y1 - y0)
        
        data_x = []
        data_y = []

        x = x0

        for i in range(y0, y1 + 1, 1):
            data_y.append(i)
            if E >= 0.5:
                x += 1
                E -= 1
                data_x.append(x)
                
            elif E <= -0.5:
                x -= 1
                E += 1
                data_x.append(x)
               
            else:
                data_x.append(x)
               
            E += dE
    print(dE)
    line(data_x, data_y, id_array)
    

    
tk = Tk()
tk.title('///')
tk.resizable(0,0)
canvas = Canvas(tk, width = 400, height = 400, bg = 'white')
canvas.pack()
id_array = []
data_x = []
data_y = []
w = 20
create_board(20,20,'grey',20)
coords = []
tk.bind('<Button-1>', lambda event: l_click(event, id_array,20))
tk.mainloop()