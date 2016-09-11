#coding:utf-8

"""
sensors = (type,distance,angle)
"""
from random import random

from numpy import abs
import numpy as np
import pdb


def reflection(sensor,turtle):
    speed = turtle.speed
    turtle.set_speed(-speed * 1.5)
    turtle.move()
    rot = 2 * sensor["angle"] - 180
    # print(sensor["angle"], turtle.direction)
    turtle.set_speed(speed)
    return speed,rot


def vecpear2angle(x,y):
    return np.rad2deg(np.arccos(np.dot(x,y)/np.linalg.norm(x)/np.linalg.norm(y)))


def vec2angle(vector):
    """
    :param vector: [sinX,cosX]
    :return: X [0,360)
    """
    if vector[1] == 0:
        angle = 90 if vector[1] > 0 else 270
    elif vector[1] > 0:
        if vector[0] > 0:
            angle = np.rad2deg(np.arctan(vector[0]/vector[1]))
        else:
            angle = 360 + np.rad2deg(np.arctan(vector[0]/vector[1]))
    else:
        angle = 180 + np.rad2deg(np.arctan(vector[0]/vector[1]))
    return angle


def change_round(x):
    """
    change round range [0,360] -> [-180,180]
    """
    x = x%360
    if 0<=x and  x<90:
        return x
    elif  90<=x and x<=270:
        return 0
    elif 270<x and x<=360:
        return 360-x

def robot_rule(sensors,field):
    turtle = field.turtle
    speed = turtle.speed
    rot = 0
    for sensor in sensors:
        if sensor["collision"]:
            if sensor["type"] == "obstacle":
                speed, rot = reflection(sensor,turtle)
                break
            elif sensor["type"] == "feed":
                field.remove_obstacle(sensor["obstacle"])
                field.set_obstacle((random()*600,random()*600), size=20, type="feed")
            else:
                speed, rot = reflection(sensor,turtle)
                break
    else:
        for sensor in sensors:
            if sensor["type"] == "feed":
                #rot += change_round(- sensor["angle"])/10
                turtle.set_direction(vec2angle((sensor["obstacle"].pos - turtle.pos)))
                # print(sensor["angle"], vecpear2angle(turtle.get_direction(), (sensor["obstacle"].pos - turtle.pos)))
                break
        else:
            for sensor in sensors:
                if sensor["type"] == "obstacle":
                    angle = sensor["angle"]
                    if 0<= angle and angle<90:
                        rot += (change_round(angle)-90)/20
                    elif 90 <= angle and angle <= 270:
                        pass
                    elif 270<= angle and angle<=360:
                        rot += (change_round(angle) + 90)/20
                else:
                    pass

    rot += (random()-0.5)*10
    return speed, rot


def sample1(sensors,turtle):
    for sensor in sensors:
        if sensor["collision"]:
            speed, rot = reflection(sensor, turtle)
            break
    else:
        speed = turtle.speed
        rot = 0 #-5 if random() < 0.5 else 5
    return speed, rot


def sample2(sensors,field):
    turtle = field.turtle
    speed = turtle.speed
    rot = 0
    for sensor in sensors:
        if sensor["collision"]:
            if sensor["type"] == "obstacle":
                speed, rot = reflection(sensor,turtle)
                break
            elif sensor["type"] == "feed":
                field.remove_obstacle(sensor["obstacle"])
                field.set_obstacle((random()*600,random()*600), size=20, type="feed")
            else:
                speed, rot = reflection(sensor,turtle)
                break
    return speed, rot
