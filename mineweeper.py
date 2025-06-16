# coding=gbk
import sys
import os
def source_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


cd = source_path('')
os.chdir(cd)
import sys
import pygame
import random
import time
import tkinter as tk
from tkinter import messagebox
from pygame.locals import *
margin=12
GUIsize=50
width=25
bombs=20
xnum=16
ynum=16
num=xnum*ynum
difficulties=[[9,9,10],[16,16,40],[30,30,120]]
def message_box(suject,content):
    root=tk.Tk()
    root.attributes("-topmost",True)
    root.withdraw()
    messagebox.showinfo(suject,content)
    try:
        root.destroy()
    except:pass
def form_map(xnum,ynum,bombs):
    map=[]
    lis=[0 for i in range(xnum*ynum-bombs)]
    lis+=[1 for k in range(bombs)]
    for x in range(xnum):
        xline=[]
        for y in range(ynum):
            xline.append(lis.pop(random.randint(0,len(lis)-1)))
        map.append(xline)
    return map
def newunder(Map,window):
    for i in range(xnum):
            for k in range(ynum):
                if Map[i][k]==0:
                    pygame.draw.rect(window,
                                    [255,255,255],
                                    (i*width+margin,k*width+margin+GUIsize,width,width))
                else:
                    pygame.draw.rect(window,
                                    [0,0,0],
                                    (i*width+margin,k*width+margin+GUIsize,width,width))
def newup(ground,window):
    for i in range(xnum):
            for k in range(ynum):
                if ground[i][k]==0:
                    pygame.draw.rect(window,
                                    [233,233,233],
                                    (i*width+margin,k*width+margin+GUIsize,width,width))
                elif ground[i][k]==2:
                    pygame.draw.rect(window,
                                    [233,2,2],
                                    (i*width+margin,k*width+margin+GUIsize,width,width))
def around(rect):
    res=[]
    for i in range(rect[0]-1,rect[0]+2):
        for k in range(rect[1]-1,rect[1]+2):
            if (i>=0 and i<xnum) and (k>=0 and k<ynum):
                res.append([i,k])
    res.remove(rect)
    return res
def detect(rect):
    if Map[rect[0]][rect[1]]==1:
        return "B"
    bombs=0
    aroundrect=around(rect)
    for rec in aroundrect:
        bomb=Map[rec[0]][rec[1]]
        bombs+=bomb
    return bombs
def mining(rect):
    global ground
    ground[rect[0]][rect[1]]=1
    if detect(rect)=="B":
        ground=[[1 for i in range(xnum)] for k in range(ynum)]

        return True
    elif detect(rect)==0:
        for rec in around(rect):
            if ground[rec[0]][rec[1]]==0:
                mining(rec)
    else:
        texts.append([rect,detect(rect)])
def showtext(texts,window,font):
    for t in texts:
        text = font.render(f"{t[1]}", True, (10, 10, 10))
        window.blit(text,(t[0][0]*width+margin+8,t[0][1]*width+margin+GUIsize))
def main(dif):
    global xnum,ynum,num,bombs,width,GUIsize,margin,Map,texts,ground
    running=True
    margin=12
    GUIsize=50
    width=25
    num=xnum*ynum
    xnum=difficulties[dif][0]
    ynum=difficulties[dif][1]
    bombs=difficulties[dif][2]
    pygame.init()
    window=pygame.display.set_mode((xnum*width+margin*2,ynum*width+margin*2+GUIsize))
    window.fill((100,200,255))
    Map=form_map(xnum,ynum,bombs)
    newunder(Map,window)
    ground=[[0 for i in range(xnum)] for k in range(ynum)]
    newup(ground,window)
    font = pygame.font.SysFont("arial", 20)
    texts=[]
    while running:
        events= pygame.event.get()
        for event in events:
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    Map=form_map(xnum,ynum,bombs)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    pos=pygame.mouse.get_pos()
                    if (pos[0]>=margin and pos[0]<=xnum*width+margin) and (
                            pos[1]>=margin+GUIsize and pos[1]<=ynum*width+margin+GUIsize):
                        rect=[(pos[0]-margin)//width,(pos[1]-GUIsize-margin)//width]
                        if ground[rect[0]][rect[1]]==0 or ground[rect[0]][rect[1]]==2:
                            if mining(rect):
                                running=False
                            newunder(Map,window)
                            newup(ground,window)
                elif mouse_presses[2]:
                    pos=pygame.mouse.get_pos()
                    if (pos[0]>=margin and pos[0]<=xnum*width+margin) and (
                            pos[1]>=margin+GUIsize and pos[1]<=ynum*width+margin+GUIsize):
                        rect=[(pos[0]-margin)//width,(pos[1]-GUIsize-margin)//width]
                        if ground[rect[0]][rect[1]]==0:
                            ground[rect[0]][rect[1]]=2
                        elif ground[rect[0]][rect[1]]==2:
                            ground[rect[0]][rect[1]]=0
                        newunder(Map,window)
                        newup(ground,window)
        showtext(texts,window,font)
        pygame.display.flip()
    message_box("Game Over!","Try again!")
    pygame.quit()
window=tk.Tk()
window.title('扫雷')
window.geometry('400x500')

l = tk.Label(window, 
    text='请选择一个难度!',   
    bg='white',    
    font=('Arial', 18),   
    width=40, height=4  
    )
l.pack()
var=tk.StringVar() 

b=tk.Button(window,text='简单',width=15,height=2,command=lambda:main(0))
c=tk.Button(window,text='中等',width=15,height=2,command=lambda:main(1))
d=tk.Button(window,text='困难',width=15,height=2,command=lambda:main(2))
b.pack()
c.pack()
d.pack()
window.mainloop()