import tkinter
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from numpy.linalg import solve

th_1 = np.pi/8
th_2 = np.pi/4
th_3 = 3*np.pi/8
th_4 = np.pi/2

def equations(lambda_, A=10, m=5.5):
    mu_0 = m/(2*(1+lambda_)*A)
    left = [[(mu_0*(1-(1-lambda_)*np.cos(th_1))+np.sin(th_1))*np.sin(th_1),(3*mu_0*(1-(1-lambda_)*np.cos(th_1))+np.sin(th_1))*np.sin(3*th_1),\
        (5*mu_0*(1-(1-lambda_)*np.cos(th_1))+np.sin(th_1))*np.sin(5*th_1),(7*mu_0*(1-(1-lambda_)*np.cos(th_1))+np.sin(th_1))*np.sin(7*th_1)],
        [(mu_0*(1-(1-lambda_)*np.cos(th_2))+np.sin(th_2))*np.sin(th_2),(3*mu_0*(1-(1-lambda_)*np.cos(th_2))+np.sin(th_2))*np.sin(3*th_2),\
        (5*mu_0*(1-(1-lambda_)*np.cos(th_2))+np.sin(th_2))*np.sin(5*th_2),(7*mu_0*(1-(1-lambda_)*np.cos(th_2))+np.sin(th_2))*np.sin(7*th_2)],
        [(mu_0*(1-(1-lambda_)*np.cos(th_3))+np.sin(th_3))*np.sin(th_3),(3*mu_0*(1-(1-lambda_)*np.cos(th_3))+np.sin(th_3))*np.sin(3*th_3),\
        (5*mu_0*(1-(1-lambda_)*np.cos(th_3))+np.sin(th_3))*np.sin(5*th_3),(7*mu_0*(1-(1-lambda_)*np.cos(th_3))+np.sin(th_3))*np.sin(7*th_3)],
        [(mu_0*(1-(1-lambda_)*np.cos(th_4))+np.sin(th_4))*np.sin(th_4),(3*mu_0*(1-(1-lambda_)*np.cos(th_4))+np.sin(th_4))*np.sin(3*th_4),\
        (5*mu_0*(1-(1-lambda_)*np.cos(th_4))+np.sin(th_4))*np.sin(5*th_4),(7*mu_0*(1-(1-lambda_)*np.cos(th_4))+np.sin(th_4))*np.sin(7*th_4)]]
    right = [mu_0*(1-(1-lambda_)*np.cos(th_1))*np.sin(th_1),mu_0*(1-(1-lambda_)*np.cos(th_2))*np.sin(th_2),\
        mu_0*(1-(1-lambda_)*np.cos(th_3))*np.sin(th_3),mu_0*(1-(1-lambda_)*np.cos(th_4))*np.sin(th_4)]


    result = solve(left, right)
    delta = (3*result[1]**2+5*result[2]**2+7*result[3]**2)/(result[0]**2)
    e_w = 1/(1+delta)
    return e_w

def total_calc(x_list, A, m):
    result = []
    top_e_w = 0
    best_lambda = 0
    for lambda_ in x_list:
        # print(lambda_)
        e_w = equations(lambda_, A, m)
        result.append(e_w)
        if top_e_w < e_w:
            top_e_w = e_w
            best_lambda = lambda_
    # print(result)
    return result, best_lambda, top_e_w




root = tkinter.Tk()
root.title(u"Best_Taper_Ratio @Vultur")
root.geometry("650x450")

#テーパー比
tapet_ration=tkinter.Label(text=u'テーパー比', font=("",12))
tapet_ration.place(x=50, y=20)
taper_low_label=tkinter.Label(text=u'(下限)')
taper_low_label.place(x=38,y=70)
taper_high_label=tkinter.Label(text=u'(上限)')
taper_high_label.place(x=103,y=70)
taper_from_to=tkinter.Label(text=u'～')
taper_from_to.place(x=80,y=50)
taper_low_entry=tkinter.Entry(width=5)
taper_low_entry.place(x=40,y=50)
taper_high_entry=tkinter.Entry(width=5)
taper_high_entry.place(x=105,y=50)

#アスペクト比
A_label=tkinter.Label(text=u'アスペクト比',font=("",12))
A_label.place(x=200,y=20)
A_entry=tkinter.Entry(width=10)
A_entry.place(x=210, y=50)

#揚力傾斜
slope_of_lift_curve_label=tkinter.Label(text=u'揚力傾斜',font=("",12))
slope_of_lift_curve_label.place(x=350,y=20)
slope_of_lift_curve_entry=tkinter.Entry(width=10)
slope_of_lift_curve_entry.place(x=353, y=50)
slope_of_lift_curve_entry.insert(tkinter.END, 5.5)

#canvasの生成
F = Figure(figsize=(7, 3), dpi=100)
re = F.add_subplot(111)
canvas = FigureCanvasTkAgg(F, master=root)
canvas.get_tk_widget().pack(side=tkinter.BOTTOM, expand=0)
canvas._tkcanvas.pack(side=tkinter.BOTTOM, expand=0)
# canvas.get_tk_widget().grid(row=0, column=0, rowspan=10)


def Make_graphs(event):
    try:
        start = float(taper_low_entry.get())
        stop = float(taper_high_entry.get())
        A = float(A_entry.get())
        m = float(slope_of_lift_curve_entry.get())
        x_list = np.linspace(start, stop, 1000)
        result, best_lambda, top_e_w = total_calc(x_list,A,m)

        delete_label = tkinter.Label(text='　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　', font=("",12))
        delete_label.place(x=350, y=125)
        top_e_w_label = tkinter.Label(text='テーパー比'+str(round(best_lambda,4))+\
            'の時、最大値'+str(round(top_e_w,4)), font=("",12),\
            background='pink')
        top_e_w_label.place(x=350, y=125)
        
        re.cla()
        re.plot(x_list, result, "r")
        re.set_title('x:Taper ratio    y:Wing efficiency')
        canvas.draw()
    except:
        pass

Button = tkinter.Button(text=u'更新', width=15, background='#ffaacc')
Button.bind("<Button-1>",Make_graphs)
Button.place(x=500, y=50)

# Make_graphs()
root.mainloop()