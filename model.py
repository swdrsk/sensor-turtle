#coding:utf-8
"""
test code or workflow to use sensor-turtle
"""
from random import random

import sensor_turtle as st
from turtle_rule import robot_rule

row,col = 600, 600

F = st.Field(row,col)
obstacles = [(random()*row,random()*col) for _ in range(10)]
feeds = [(random()*row,random()*col) for _ in range(4)]

F.set_turtle(pos=(row/2,col/2),size=20,sensor_range=150)


for pos in obstacles:
    F.set_obstacle(pos,size=20,type="obstacle")
for pos in feeds:
    F.set_obstacle(pos,size=20,type="feed")

R = F.turtle
R.set_speed(2)
rot = 30

while True:
    R.rot(rot)
    R.move()
    sensors = F.get_sensor()
    message = {}
    for i,sensor in enumerate(sensors):
        message.update({"(%s) %10s"%(i,sensor["type"]):"%3.1f"%sensor["angle"]})
    speed, rot = robot_rule(sensors,F)
    F.draw(message)
    # if not F.get_obstacle("feed"):
    #     break
