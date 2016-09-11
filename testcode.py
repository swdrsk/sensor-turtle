#coding:utf-8
"""
test code or workflow to use sensor-turtle
"""
from random import random

import sensor_turtle as st
from turtle_rule import robot_rule

row,col = 600, 600

F = st.Field(row,col)
obstacles = [(random()*row,random()*col) for _ in range(30)]
feeds = [(random()*row,random()*col) for _ in range(4)]

F.set_turtle(pos=(row/2,col/2),size=10,sensor_range=40)

#
# for pos in obstacles:
#     F.set_obstacle(pos,size=10,type="obstacle")
# for pos in feeds:
#     F.set_obstacle(pos,size=10,type="feed")
#

R = F.turtle
R.set_speed(2)
rot = 1

while True:
    F.draw()
    R.rot(rot)
    R.move()
    sensors = F.get_sensor()
    speed, rot = robot_rule(sensors,R)
    # if not F.get_obstacle("feed"):
    #     break
