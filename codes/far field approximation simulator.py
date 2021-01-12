
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from tkinter import *
import numpy as np
import math
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  NavigationToolbar2Tk) 
from PIL import Image, ImageTk

x_A, y_A = 520, 800
x_B, y_B = 700, 800
k = 0
dist3 = 100
draw = False
float_formatter = "{:.2f}".format
distance_vector = np.zeros(10)
angle_vector = np.zeros((10,10))
error_angle = np.zeros((10,10))
fig = plt.figure(figsize=(7, 7))


def plot_all():
    global x_A
    global y_A
    global x_B
    global y_B
    global dist3 
    global fig


    arg = (dist3,x_A,y_A,x_B,y_B)
    fig = plt.figure(figsize=(7, 7))
    fig.suptitle('Plots', fontsize=10, fontweight='bold')
    ax1 = fig.add_subplot(212)
    ax2 = fig.add_subplot(221)
    ax3 = fig.add_subplot(222)

    X = np.arange(-250, 250, 1)
    Y = np.arange(0, 500, 1)
    X, Y = np.meshgrid(X, Y)
    
    dist1 = np.sqrt((X+(arg[0]/2))**2 + Y**2)
    dist2 = np.sqrt((X-(arg[0]/2))**2 + Y**2)
    angle_incident = 180*np.arcsin(abs(dist1-dist2)/arg[0])/np.pi
    angle_incident_theo = abs(180*np.arcsin((dist1**2+arg[0]**2-dist2**2)/(2*dist1*arg[0]))/np.pi + 0.000001)
    error_angle = 100*abs(angle_incident_theo-angle_incident)/(angle_incident_theo+0.000001)
    error_angle[error_angle>(300)]=300
    contours = ax1.contour(X, Y, error_angle, [0, 10, 20, 30, 40, 50, 60, 100, 150, 200], colors='black', linestyles='dashed')
    ax1.clabel(contours, inline=True, fontsize=8)
    im=ax1.imshow(error_angle, extent=[-250, 250, 0, 500], origin='lower', cmap='viridis', alpha=0.5)
    fig.colorbar(im, ax=ax1)

    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_title('Error in Angle (%)', verticalalignment='top')

    

    contours2 = ax2.contour(X, Y, angle_incident_theo, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90], colors='black', linestyles='dashed')
    ax2.clabel(contours2, inline=True, fontsize=8)
    im2=ax2.imshow(angle_incident_theo, extent=[-250, 250, 0, 500], origin='lower', cmap='viridis', alpha=0.5)
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title('Theoretical Angle (Degree)')
    fig.colorbar(im2, ax=ax2);
    

    contours3 = ax3.contour(X, Y, angle_incident, [0, 2, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90], colors='black', linestyles='dashed')
    ax3.clabel(contours3, inline=True, fontsize=8)
    im3 = ax3.imshow(angle_incident, extent=[-250, 250, 0, 500], origin='lower', cmap='viridis', alpha=0.5)
    fig.colorbar(im3, ax=ax3);
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_title('Far Field Approximation Angle (Degree)')

    right_frame = Frame(my_window, width=500, height=500)
    right_frame.grid(row=0, column=1, padx=2, pady=2)
    right_frame.grid_forget()
    right_frame = Frame(my_window, width=500, height=500)
    right_frame.grid(row=0, column=1, padx=2, pady=2)
    
    
    
    plot_all.canvas = FigureCanvasTkAgg(fig, master = right_frame)   
    plot_all.canvas.draw() 
    plot_all.canvas.get_tk_widget().pack() 
    
    # creating the Matplotlib toolbar 
    plot_all.toolbar = NavigationToolbar2Tk(plot_all.canvas, right_frame) 
    plot_all.toolbar.update() 
  
    # placing the toolbar on the Tkinter window 
    plot_all.canvas.get_tk_widget().pack() 


    
def scan_point(event,arg):
    print('Scan is started.')
    global k
    #global m
    global distance_vector
    distance_vector[k] = arg[0]
    global angle_vector
    angle_vector[k,k] = arg[2]
    global error_angle
    error_angle[k,k] = 100*abs(arg[2]-arg[1])/arg[2]
    if k == 9:
      fig = plt.figure(figsize=(20, 16))
      ax = fig.add_subplot(111, projection='3d')
      m = 0
      for c, z in zip(['b', 'g', 'r', 'c', 'm', 'y', 'k', 'teal', 'indigo', 'tomato'], distance_vector):
        ax.bar(angle_vector[m,:], error_angle[m,:], zs=z, zdir='y', color=c, alpha=0.8)
        m = m + 1
      ax.set_xlabel('X, theoretical angle')
      ax.set_ylabel('Y, distance to the antenna')
      ax.set_zlabel('Z, error in angle (%)')
      plt.show()
    k = k + 1
    

def draw_lines(event):
    global dist3
    if hasattr(draw_lines, 'A_line'):
        my_canvas.delete(draw_lines.A_line)
        my_canvas.delete(draw_lines.B_line)
        my_canvas.delete(draw_lines.real_A)
        my_canvas.delete(draw_lines.textd1)
        my_canvas.delete(draw_lines.textd2)
        my_canvas.delete(draw_lines.nol)
        
        my_canvas.delete(draw_lines.ax)
    x, y = event.x, event.y
    point = np.array((x, y))
    dist1 = np.linalg.norm(point - point_A)
    dist2 = np.linalg.norm(point - point_B)
    dist3 = np.linalg.norm(point_A - point_B)
    middle_dist = np.linalg.norm(point - (point_A/2) - (point_B/2))
    prompt = Label(my_canvas, text='Length of median is = '+str(float_formatter(middle_dist))+'\n'+
                   'Distance to A = '+str(float_formatter(dist1))+'\n'+
                   'Distance to B = '+str(float_formatter(dist2))+'\n'+
                   'Distance between A & B = '+str(float_formatter(dist3)), bd=4, relief="solid", font="Times 10 bold", bg="white", fg="black")
    ant = x_B - x_A
    if dist1 > dist2: 
        h = y - y_B
        w = x - x_B
        p_x = (w / dist2)
        p_y = (h / dist2)
        draw_lines.A_line = my_canvas.create_line(x_A, y_A, x_A + dist2 * p_x/2, y_A + dist2 * p_y/2, width=3, fill='RoyalBlue1') # kucuk paralel
        draw_lines.textd1 = my_canvas.create_text( x_A + dist2 * p_x/2, y_A + dist2 * p_y/2,fill="RoyalBlue1",font="Times 18", text="d1")
        
        draw_lines.B_line = my_canvas.create_line(x_B, y_B, x, y, width=3, fill='VioletRed3') # kirmizi uzun
        draw_lines.real_A = my_canvas.create_line(x_A, y_A, x, y, width=3, dash=(3, 5), fill='blue2') # 
        draw_lines.textd2 = my_canvas.create_text(x, y,fill="blue2",font="Times 18", text="d2")
        
        draw_lines.ax = my_canvas.create_line(x_A+120, y_A-120*((x_B-x_A)/(y_B-y_A+0.001)), x_A-120, y_A+120*((x_B-x_A)/(y_B-y_A+0.001)), width=3, fill='black', dash=(2, 5))
        draw_lines.nol = my_canvas.create_text(x_B-120, y_B+120*((x_B-x_A)/(y_B-y_A+0.001)),fill="black",font="Times 18", text="N")
        
        angle_incident = 180*np.arcsin((dist1-dist2)/dist3)/np.pi
        angle_incident_theo = 180*np.arcsin((dist1**2+dist3**2-dist2**2)/(2*dist1*dist3))/np.pi
        # draw_lines.arc = my_canvas.create_arc(x_A+120, y_A-120*((x_B-x_A)/(y_B-y_A+0.001)), x_A + dist2 * p_x/2, y_A + dist2 * p_y/2, style=ARC, start=0, extent=angle)
        angle_label = Label(my_canvas, text='Angle incident to A, approx = '+str(float_formatter(angle_incident))+'\n'+'Angle incident to A, theo. = '+str(float_formatter(angle_incident_theo)), bd=4, relief="solid", font="Times 10 bold", bg="white", fg="black")
    else:
        h = y - y_A
        w = x - x_A
        p_x = (w / dist1)
        p_y = (h / dist1)
        draw_lines.B_line = my_canvas.create_line(x_B, y_B, x_B + dist1 * p_x/2, y_B + dist1 * p_y/2, width=3, fill='RoyalBlue1')
        draw_lines.textd1 = my_canvas.create_text(x_B + dist1 * p_x/2, y_B + dist1 * p_y/2,fill="RoyalBlue1",font="Times 18", text='d1')
        
        draw_lines.A_line = my_canvas.create_line(x_A, y_A, x, y, width=3, fill='VioletRed3')
        
        draw_lines.real_A = my_canvas.create_line(x_B, y_B, x, y, width=3, dash=(3, 5), fill='blue2')
        draw_lines.textd2 = my_canvas.create_text(x, y,fill="blue2",font="Times 18", text='d2')
        
        draw_lines.ax = my_canvas.create_line(x_B+120, y_B-120*((x_B-x_A)/(y_B-y_A+0.001)), x_B-120, y_B+120*((x_B-x_A)/(y_B-y_A+0.001)), width=3, fill='black', dash=(2, 5))
        draw_lines.nol = my_canvas.create_text(x_B-120, y_B+120*((x_B-x_A)/(y_B-y_A+0.001)),fill="black",font="Times 14", text='N')
        
        angle_incident = 180 * np.arcsin((dist2-dist1)/dist3) / np.pi
        angle_incident_theo = 180*np.arcsin((dist2**2+dist3**2-dist1**2)/(2*dist2*dist3))/np.pi
        # draw_lines.arc = my_canvas.create_arc(x_B+120, y_B-120*((x_B-x_A)/(y_B-y_A+0.001)), x_B + dist1 * p_x/3, y_B + dist1 * p_y/3, style=ARC, start=0, extent=angle) 
        angle_label = Label(my_canvas, text='Angle incident to B, approx = '+str(float_formatter(angle_incident))+'\n'+'Angle incident to B, theo. = '+str(float_formatter(angle_incident_theo)), bd=4, relief="solid", font="Times 10 bold", bg="white", fg="black")
    angle_label.place(x=303,y=0)
    prompt.place(x=0,y=0)
    my_canvas.focus_set()
    #my_canvas.bind("<Key>", lambda event, arg=(middle_dist,angle_incident,angle_incident_theo): scan_point(event,arg))
    #my_canvas.bind("<Key>", lambda event, arg=(dist3,x_A,y_A,x_B,y_B): plot_all(event,arg))
    
    return (dist3,x_A,y_A,x_B,y_B)
def create_grid(window):
    width = 500
    height = 500
    


    for line in range(0, width, 20): # range(start, stop, step)
        window.create_line([(line, 0), (line, height)], fill='black', tags='grid_line_w', width=0.5, dash=(3, 5))

    for line in range(0, height, 20):
        window.create_line([(0, line), (width, line)], fill='black', tags='grid_line_h', width=0.5, dash=(3, 5))

    window.grid(row=0, column=0)


def on_click():
    global x_A
    global y_A
    global point_A
    global x_B
    global y_B
    global point_B

    if hasattr(on_click, 'ovalA'):
        my_canvas.delete(on_click.ovalB)
        my_canvas.delete(on_click.textB)
        my_canvas.delete(on_click.ovalA)
        my_canvas.delete(on_click.textA)
        my_canvas.delete(on_click.lineAB)
    A_cor = A_button.get()
    B_cor = B_button.get()
    a = A_cor.split(',')
    b = B_cor.split(',')
    x_A, y_A = int(a[0]), int(a[1])
    x_B, y_B = int(b[0]), int(b[1])
    

    point_A = np.array((x_A, y_A))
    on_click.ovalA = my_canvas.create_oval(x_A - 3, y_A - 3, x_A + 3, y_A + 3, width=3, fill='black', outline='black')
    on_click.textA = my_canvas.create_text(x_A+5,y_A+25,fill="black",font="Times 20", text="A")
  

    point_B = np.array((x_B, y_B))
    on_click.ovalB = my_canvas.create_oval(x_B - 3, y_B - 3, x_B + 3, y_B + 3, width=3, fill='black', outline='black')
    on_click.textB = my_canvas.create_text(x_B+5,y_B+25,fill="black",font="Times 20", text="B")
    on_click.lineAB = my_canvas.create_line(x_A, y_A, x_B, y_B, width=3, fill='black')
    my_canvas.bind('<Motion>', draw_lines)
    
    print(x_A, y_A)
    
def button_command():
    
    return None
    
my_window = Tk()
my_window.wm_title("Far Field Approximation Simulator")
# Creating the frame with the canvas and lines etc.
top_frame = Frame(my_window, width=500, height=500)
top_frame.grid(row=0, column=0, padx=2, pady=2)

my_canvas = Canvas(top_frame, width=500, height=500, background='white')
create_grid(my_canvas)
#my_canvas.bind('<Button-1>', callback)
my_canvas.grid()


bottom_frame = Frame(my_window, width=500, height=200)
bottom_frame.grid(row=1, column=0, padx=2, pady=2)



box_frame = Frame(bottom_frame, width=100, height=100)
box_frame.grid(row=0, column=0, padx=2, pady=2)
A_button = Entry(box_frame, width=10)
A_button.grid(row=0, column=0, padx=2, pady=2)

B_button = Entry(box_frame, width=10)
B_button.grid(row=0, column=1, padx=2, pady=2)


ok_btn = Button(box_frame, text='OK', command=on_click)
ok_btn.grid(row=0, column=3, padx=2, pady=2)

btn = Button(box_frame, text='Show Plots', command=plot_all)
btn.grid(row=0, column=4, padx=150, pady=2)


right_frame = Frame(my_window, width=500, height=500)
right_frame.grid(row=0, column=1, padx=2, pady=2)

# btn = Button(btn_frame, text='Show Plots', command=(lambda arg=(dist3,x_A,y_A,x_B,y_B): plot_all(event,arg)))


# fr = Frame(my_canvas)
# B_button = Text(fr, width=5, height=5)
# B_button.pack(pady=50, padx=50)

#button_A.grid()
#button_B = Entry()

my_window.mainloop()





