import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


'''
复旦大学2022级物理学系 吕昱奇
光学荣誉课作业：正入射透射型闪耀光栅和阶梯光栅衍射的模拟
考虑标量场衍射和理想光栅，忽略倾斜因子，自变量选择为衍射角度/°
可调控组件有入射光波长，光栅倾角（阶梯光栅的厚度随之改变），阶梯级数，光栅条数和光栅常数
当阶梯数增加时应该观察到阶梯光栅的光强逐步趋近于闪耀光栅
'''
plt.rcParams['font.family']='Microsoft YaHei'  # 设置matplotlib绘图的中文字体

# 创建窗口
window = tk.Tk()
window.title("闪耀光栅和阶梯光栅")
window.geometry("1280x960")


# 绘制闪耀光栅光强图
def fshow1():
    global lam
    lam=s1.get() # 入射光波长
    gam=s2.get() # 闪耀角
    M=s3.get() # 阶梯级数
    N=s4.get() # 光栅条数
    p=s5.get() # 光栅常数（周期）
    n=1.5 # 折射率
    if style.get()==1: # 出于精度和运行速度考虑，绘制光强示意图时采用更低精度，代价是主极大和它周围的副极大界限变模糊
        the=np.linspace(-30,30,2000) # 角度范围-30°-30°，精度2000
    else:
        the=np.linspace(-30,30,20000) # 角度范围-30°-30°，精度20000
    del1=np.pi*p/lam*(np.sin(the*np.pi/180)-(n-np.cos(the*np.pi/180))*np.tan(gam/180*np.pi)) # 衍射相位差
    del2=np.pi*p/lam*np.sin(the*np.pi/180) # 干涉相位差
    I0=(np.sin(del1)/del1)**2*(np.sin(N*del2)/np.sin(del2))**2 # 光强
    fb.clear()
    if style.get()==0: # 显示光强曲线
        fb.plot(the,I0) # 相对光强为y，角度为x轴
        fb.set_xlim(-20, 20)
        fb.set_xticks(np.linspace(-30, 30, 7))
        fb.set_xlabel('衍射角度/°')
        fb.set_ylabel('相对光强')
        fb.set_title('闪耀光栅光强曲线')
        fb.axis('tight')
    else: # 显示光强示意图
        I00=[I0]*1000 # 光强扩展为二维数组
        fb.imshow(I00,cmap='gray',norm='log',vmin=0.5,vmax=10000) # 对数归一化使图片符合真实人眼
        fb.axis('off')
        fb.set_title('闪耀光栅光强示意图')
    canvas.draw()

    
# 绘制阶梯光栅光强图
def fshow2():
    global lam
    lam=s1.get()
    gam=s2.get()
    M=s3.get()
    N=s4.get()
    p=s5.get()
    n=1.5
    if style.get()==1: # 出于精度和运行速度考虑，绘制光强示意图时采用更低精度
        the=np.linspace(-30,30,2000) # 角度范围-30°-30°，精度2000
    else:
        the=np.linspace(-30,30,20000) # 角度范围-30°-30°，精度20000
    del1=np.pi*p/lam*(np.sin(the*np.pi/180)-(n-np.cos(the*np.pi/180))*np.tan(gam/180*np.pi))
    del2=np.pi*p/lam*np.sin(the*np.pi/180)
    I1=(np.sin(del2/M)/(del2/M)/M)**2*(np.sin(del1)/np.sin(del1/M))**2*(np.sin(N*del2)/np.sin(del2))**2
    fd.clear()
    if style.get()==0:
        fd.plot(the,I1)
        fd.set_xlim(-30, 30)
        fd.set_xticks(np.linspace(-30, 30, 7))
        fd.set_xlabel('衍射角度/°')
        fd.set_ylabel('相对光强')
        fd.set_title('阶梯光栅光强曲线')
        fd.axis('tight')
    else:
        I11=[I1]*1000
        fd.imshow(I11,cmap='gray',norm='log',vmin=0.5,vmax=10000)
        fd.axis('off')
        fd.set_title('阶梯光栅光强示意图')
    canvas.draw()

    
# 计算并调节至闪耀波长
def getlam():
    p=s5.get()
    gam=s2.get()*np.pi/180
    lam=p*(np.cos(gam)*(1.5*np.sin(gam)-0.125*np.cos(gam)*np.sqrt(64*np.tan(gam)**2-80*np.tan(gam)**4))) # 一级闪耀波长
    i=2
    nlam=lam # 可调节范围内最大闪耀波长
    while 1:
        if nlam>780: # 波长大于最大之后调节新波长为原波长i分之一，此时波长为i级闪耀波长
            nlam=lam/i
            i+=1
        else:
            break
    s1.set(nlam)



    
# 绘制闪耀光栅和阶梯光栅示意图
def fshow3():
    fa.clear()
    fc.clear()
    m=2
    M=s3.get()
    gam=s2.get()
    p=s5.get()
    lam=s1.get()
    xstart=-50*m
    ystart=0
    # 闪耀光栅
    
    # 画三角形
    for i in range(2*m): 
        x0=np.array([xstart,xstart+50])
        y0=np.array([ystart,ystart+50*np.sin(gam*np.pi/180)])
        fa.plot(x0,y0,c='k',lw=1) # 斜边
        x1=np.array([xstart+50,xstart+50])
        y1=np.array([ystart,ystart+50*np.sin(gam*np.pi/180)])
        fa.plot(x1,y1,c='k',lw=1) # 竖直线
        xstart+=50
    fa.plot(np.array([-50*4/3,-50*4/3]),np.array([-70,-5]),c='k',lw=0.75) # 画入射光，五条平行光线
    fa.plot(np.array([-50*2/3,-50*2/3]),np.array([-70,-5]),c='k',lw=0.75)
    fa.plot(np.array([0,0]),np.array([-70,-5]),c='k',lw=0.75)
    fa.plot(np.array([50*2/3,50*2/3]),np.array([-70,-5]),c='k',lw=0.75)
    fa.plot(np.array([50*4/3,50*4/3]),np.array([-70,-5]),c='k',lw=0.75)
    # 画出射光
    fa.plot([0,0],[5+50*np.sin(gam*np.pi/180),40],c='k',lw=0.75) # 零级衍射光
    if 2*lam/p<1: # 1级衍射光（如果有的话）
        fa.plot([10,10+(35-50*np.sin(gam*np.pi/180))*(lam/p)/np.sqrt(1-(lam/p)**2)],[5+50*np.sin(gam*np.pi/180),40],c='k',lw=0.75)
    if 3*lam/p<1:
        fa.plot([20,20+(35-50*np.sin(gam*np.pi/180))*(2*lam/p)/np.sqrt(1-(2*lam/p)**2)],[5+50*np.sin(gam*np.pi/180),40],c='k',lw=0.75)
    if 4*lam/p<1:
        fa.plot([30,30+(35-50*np.sin(gam*np.pi/180))*(3*lam/p)/np.sqrt(1-(3*lam/p)**2)],[5+50*np.sin(gam*np.pi/180),40],c='k',lw=0.75)
    # 一些文本和注释
    fa.text(-90,25,'$'+str(p)+r'\mathrm{nm}$')  # 光栅周期
    fa.plot([-50,-50],[0,40],ls='--',lw=0.75,c='k')
    fa.plot([-100,-100],[0,40],ls='--',lw=0.75,c='k')
    fa.text(-130,-40,r'$n=1.5$') # 折射率
    fa.text(-130,30,r'$n_0=1$')
    
    fa.set_ylim(-75,50)
    fa.set_xlim(-m*50,m*50+40)
    fa.axis('off')
    xstart=-m*50
    ystart=0
    
    
    # 阶梯光栅 基本同上
    for i in range(2*m):
        for j in range(M):
            x0=np.array([xstart,xstart])
            y0=np.array([ystart,ystart+50*np.sin(gam*np.pi/180)/M])
            fc.plot(x0,y0,c='k',lw=1) # 短竖线
            x1=np.array([xstart,xstart+50/M])
            y1=np.array([ystart+50*np.sin(gam*np.pi/180)/M,ystart+50*np.sin(gam*np.pi/180)/M])
            fc.plot(x1,y1,c='k',lw=1) # 横线
            xstart+=50/M
            ystart+=50*np.sin(gam*np.pi/180)/M
        ystart=0
        fc.plot([xstart,xstart],[0,50*np.sin(gam*np.pi/180)],c='k',lw=1) # 长竖线
        
    fc.plot(np.array([-50*4/3,-50*4/3]),np.array([-70,-5]),c='k',lw=0.75)
    fc.plot(np.array([-50*2/3,-50*2/3]),np.array([-70,-5]),c='k',lw=0.75)
    fc.plot(np.array([0,0]),np.array([-70,-5]),c='k',lw=0.75)
    fc.plot(np.array([50*2/3,50*2/3]),np.array([-70,-5]),c='k',lw=0.75)
    fc.plot(np.array([50*4/3,50*4/3]),np.array([-70,-5]),c='k',lw=0.75)
    
    fc.plot([0,0],[5+50*np.sin(gam*np.pi/180),40],c='k',lw=0.75)
    if 2*lam/p<1:
        fc.plot([10,10+(35-50*np.sin(gam*np.pi/180))*(lam/p)/np.sqrt(1-(lam/p)**2)],[5+50*np.sin(gam*np.pi/180),40],c='k',lw=0.75)
    if 3*lam/p<1:
        fc.plot([20,20+(35-50*np.sin(gam*np.pi/180))*(2*lam/p)/np.sqrt(1-(2*lam/p)**2)],[5+50*np.sin(gam*np.pi/180),40],c='k',lw=0.75)
    if 4*lam/p<1:
        fc.plot([30,30+(35-50*np.sin(gam*np.pi/180))*(3*lam/p)/np.sqrt(1-(3*lam/p)**2)],[5+50*np.sin(gam*np.pi/180),40],c='k',lw=0.75)    
    
    fc.text(-90,25,'$'+str(p)+r'\mathrm{nm}$')
    fc.plot([-50,-50],[0,40],ls='--',lw=0.75,c='k')
    fc.plot([-100,-100],[0,40],ls='--',lw=0.75,c='k')
    fc.text(-130,-40,r'$n=1.5$')
    fc.text(-130,30,r'$n_0=1$')
    
    fc.set_ylim(-75,50)
    fc.set_xlim(-m*50,m*50+40)
    fc.axis('off')
    fa.set_title('闪耀光栅')
    fc.set_title('阶梯光栅')
    canvas.draw()




# 创建并绘制图形
f = Figure(figsize=(12,7),dpi=100)
fa=f.add_subplot(221) # 闪耀光栅示意图
fb=f.add_subplot(222) # 闪耀光栅衍射图
fc=f.add_subplot(223) # 阶梯光栅示意图
fd=f.add_subplot(224) # 阶梯光栅衍射图
f.subplots_adjust(hspace=0.4)
canvas = FigureCanvasTkAgg(f, master=window)
canvas.draw()
canvas.get_tk_widget().grid(row=0,column=0,columnspan=3,padx=40)
f.suptitle('正入射下透射型闪耀光栅和阶梯光栅衍射')

# 更新图像的函数
def fshow(x=None):
    fshow1()
    fshow2()
    fshow3()

# 创建调控组件

# 五个调节滑块
s1=tk.Scale(window,from_=20,to=780,orient=tk.HORIZONTAL,length=500,sliderlength=10,showvalue=1,label="入射光波长/nm",tickinterval=80,
             resolution=0.1,command=fshow)
s2=tk.Scale(window,from_=0,to=30,orient=tk.HORIZONTAL,length=500,sliderlength=10,showvalue=1,label="光栅倾角/°",tickinterval=5,
             resolution=0.1,command=fshow)
s3=tk.Scale(window,from_=1,to=50,orient=tk.HORIZONTAL,length=500,sliderlength=10,showvalue=1,label="阶梯级数",
             resolution=1,command=fshow)
s4=tk.Scale(window,from_=1,to=100,orient=tk.HORIZONTAL,length=500,sliderlength=10,showvalue=1,label="光栅条数",
             resolution=1,command=fshow)
s5=tk.Scale(window,from_=500,to=20000,orient=tk.HORIZONTAL,length=500,sliderlength=10,showvalue=1,label="光栅常数/nm",
             resolution=10,command=fshow)
# 调节为闪耀波长的按钮
b1=tk.Button(window,text="调节为闪耀波长",height=2,width=20,command=getlam)
style=tk.IntVar()
# 选择显示方式
r1=tk.Radiobutton(window,text='显示光强曲线',variable=style,value=0,command=fshow)
r2=tk.Radiobutton(window,text='显示光强示意图',variable=style,value=1,command=fshow)
# 设置初值并绘画
s1.set(600)
s2.set(10)
s3.set(2)
s4.set(1)
s5.set(5000)


# 安装组件
s1.grid(row=1,column=0,padx=50)
s2.grid(row=2,column=0,padx=50)
s3.grid(row=1,column=1,padx=50,columnspan=2)
s4.grid(row=2,column=1,padx=50,columnspan=2)
s5.grid(row=3,column=0,padx=50,rowspan=2)
b1.grid(row=3,column=1,rowspan=2)
r1.grid(row=3,column=2,sticky='w')
r2.grid(row=4,column=2,sticky='w')

# 窗口循环
window.mainloop()