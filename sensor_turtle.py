#coding:utf-8

import numpy as np
from random import random
import pygame
from pygame.locals import *
import sys

clock = pygame.time.Clock()

def normalize_angle(x):
    return x % 360

def vector2angle(vector):
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


class Field:
    def __init__(self, row, col, title="sensor-turtle"):
        pygame.init()
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode(Rect(0,0,row,col).size)
        self.row = row
        self.col = col
        self.scr_rect = Rect(0,0,row,col)
        self.obstacles = []
        self.turtle = None
        self.color_model = {"field":(255,255,200),
                            "turtle":(0, 255, 0),
                            "head":(0, 0, 255),
                            "sensor":(255,255,150),
                            "obstacle":(50,0,50),
                            "feed":(255,0,0)}
        self.message_font = pygame.font.SysFont(None, 20)

    def set_colormodel(self,model):
        self.color_model.update(model)

    def set_fontsize(self,size):
        self.message_font = pygame.font.SysFont(None,size)

    def set_turtle(self, pos,size, sensor_range):
        self.turtle = Turtle(pos, size, sensor_range)

    def set_obstacle(self,pos,size,type):
        obstacle = Obstacle(pos,size,type)
        self.obstacles.append(obstacle)

    def get_obstacle(self,type):
        return_list = []
        for obstacle in self.obstacles:
            if obstacle.type == type:
                return_list.append(obstacle)
        return return_list

    def remove_obstacle(self, obstacle):
        self.obstacles.remove(obstacle)

    def get_sensor(self):
        sensors = []
        pos = self.turtle.pos
        for obstacle in self.obstacles:
            turtle_obstacle_distance = np.linalg.norm(obstacle.pos - pos)
            if turtle_obstacle_distance <= self.turtle.sensor_range + self.turtle.size + obstacle.size:
                angle = normalize_angle(vector2angle(obstacle.pos-pos) - self.turtle.direction)
                is_collision = True if turtle_obstacle_distance <= obstacle.size + self.turtle.size else False
                sensors.append({"distance":    turtle_obstacle_distance,
                                "angle":        angle,
                                "type":         obstacle.type,
                                "collision":   is_collision,
                                "obstacle":    obstacle})

        if pos[0] <= self.turtle.size or self.row-self.turtle.size <= pos[0]:
            sensors.append({"distance": np.abs((pos[0]-self.row*1.0/2)-self.row*1.0/2),
                            "angle": -self.turtle.direction+90,
                            "type": "wall",
                            "collision": True})
        if pos[1] <= self.turtle.size or self.col-self.turtle.size <= pos[1]:
            sensors.append({"distance": np.abs((pos[1]-self.col*1.0/2)-self.col*1.0/2),
                            "angle": -self.turtle.direction,
                            "type": "wall",
                            "collision": True})
        return sensors

    def draw(self,message={}):
        clock.tick(60)
        pygame.display.flip()

        screen = self.screen
        screen.fill(self.color_model["field"])

        pygame.draw.circle(screen,
                           self.color_model["sensor"],
                           self.turtle.get_intpos(),
                           int(self.turtle.size+self.turtle.sensor_range)
                            )
        pygame.draw.line(screen,
                         self.color_model["head"],
                         self.turtle.get_intpos(),
                         self.turtle.get_intpos() + self.turtle.get_direction() * self.turtle.size*1.5,
                         self.turtle.size/4)
        pygame.draw.circle(screen,
                           self.color_model["turtle"],
                           self.turtle.get_intpos(),
                           self.turtle.size)

        for obstacle in self.obstacles:
            try:
                pygame.draw.circle(screen, self.color_model[obstacle.type], obstacle.get_intpos(), obstacle.size)
            except:
                print("Define color model of %s"%obstacle.type)
                pygame.quit()
                sys.exit()

        if message:
            for num,key in  enumerate(message.keys()):
                message_rect = (5,5+num*25)
                message_surface = self.message_font.render("%s: %s"%(key, message[key]),False,(0,0,0))
                screen.blit(message_surface,message_rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


class Turtle:
    def __init__(self, pos, size, sensor_range):
        self.size = size
        self.sensor_range = float(sensor_range)
        self.pos = np.array(map(float,pos))
        self.speed = 0.0
        self.direction = 0

    def move(self):
        self.pos += [self.speed * np.sin(np.deg2rad(self.direction)),
                     self.speed * np.cos(np.deg2rad(self.direction))]

    def rot(self,direction):
        self.direction = normalize_angle(self.direction + direction)

    def set_pos(self,pos):
        self.pos = map(float,pos)

    def set_speed(self,speed):
        self.speed = float(speed)

    def set_direction(self,direction):
        self.direction = float(direction)

    def get_intpos(self):
        return np.array(map(int,self.pos))

    def get_direction(self):
        return np.array([np.sin(np.deg2rad(self.direction)),
                         np.cos(np.deg2rad(self.direction))])

    def get_intvel(self):
        return np.array([int(self.speed * np.sin(np.deg2rad(self.direction))),
                         int(self.speed * np.cos(np.deg2rad(self.direction)))])


class Obstacle:
    def __init__(self,pos,size,type_str):
        self.pos = np.array(map(float, pos))
        self.size = size
        self.type = type_str

    def get_intpos(self):
        return map(int,self.pos)
