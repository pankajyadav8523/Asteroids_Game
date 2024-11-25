"""
Subcontroller module for Planetoids

This module contains the subcontroller to manage a single level (or wave) in the 
Planetoids game.  Instances of Wave represent a single level, and should correspond
to a JSON file in the Data directory. Whenever you move to a new level, you are 
expected to make a new instance of the class.

The subcontroller Wave manages the ship, the asteroids, and any bullets on screen. These 
are model objects. Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Ed Discussions and we will answer.

Author : Pankaj Yadav
Date : 3 April, 2023
"""
from game2d import *
from consts import *
from models import *
from math import *
import random
import datetime

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Level is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)

class Wave(object):
    """
    This class controls a single level or wave of Planetoids.
    
    This subcontroller has a reference to the ship, asteroids, and any bullets on screen.
    It animates all of these by adding the velocity to the position at each step. It
    checks for collisions between bullets and asteroids or asteroids and the ship 
    (asteroids can safely pass through each other). A bullet collision either breaks
    up or removes a asteroid. A ship collision kills the player. 
    
    The player wins once all asteroids are destroyed.  The player loses if they run out
    of lives. When the wave is complete, you should create a NEW instance of Wave 
    (in Planetoids) if you want to make a new wave of asteroids.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 25 for an example.  This class will be similar to
    than one in many ways.
    
    All attributes of this class are to be hidden. No attribute should be accessed 
    without going through a getter/setter first. However, just because you have an
    attribute does not mean that you have to have a getter for it. For example, the
    Planetoids app probably never needs to access the attribute for the bullets, so 
    there is no need for a getter there. But at a minimum, you need getters indicating
    whether you one or lost the game.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # THE ATTRIBUTES LISTED ARE SUGGESTIONS ONLY AND CAN BE CHANGED AS YOU SEE FIT
    # Attribute _data: The data from the wave JSON, for reloading 
    # Invariant: _data is a dict loaded from a JSON file
    # Attribute _ship: The player ship to control 
    # Invariant: _ship is a Ship object
    #
    # Attribute _asteroids: the asteroids on screen 
    # Invariant: _asteroids is a list of Asteroid, possibly empty
    #
    # Attribute _bullets: the bullets currently on screen 
    # Invariant: _bullets is a list of Bullet, possibly empty
    #
    # Attribute _lives: the number of lives left 
    # Invariant: _lives is an int >= 0
    #
    # Attribute _firerate: the number of frames until the player can fire again 
    # Invariant: _firerate is an int >= 0
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER (standard form) TO CREATE SHIP AND ASTEROIDS
    
    # UPDATE METHOD TO MOVE THE SHIP, ASTEROIDS, AND BULLETS
    
    # DRAW METHOD TO DRAW THE SHIP, ASTEROIDS, AND BULLETS
    
    # RESET METHOD FOR CREATING A NEW LIFE
    
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION

    def __init__(self, data):
        """
        It craete ship and asteroid
        Parameter data: It is a python dictionary about the value of ship and asteroid.
        """
        x = data['ship']['position'][0]
        y = data['ship']['position'][1]
        angle = data['ship']['angle']
        self._ship = Ship(x, y, angle, SHIP_IMAGE)
        Source = [LARGE_IMAGE, MEDIUM_IMAGE, SMALL_IMAGE]
        hw = [LARGE_RADIUS, MEDIUM_RADIUS, SMALL_RADIUS]
        self._firerate = 0
        self._lives = SHIP_LIVES
        self._data = data
        asteroid_lst = []
        for i in data['asteroids']:
            if i['size'] == 'large':
                direction = i['direction']
                asteroid_lst.append(Asteroid(i['position'][0],i['position'][1],2*hw[0],2*hw[0],Source[0], direction, 'large'))
            elif i['size'] == 'medium':
                direction = i['direction']
                asteroid_lst.append(Asteroid(i['position'][0],i['position'][1],2*hw[1],2*hw[1],Source[1], direction, 'medium'))
            else:
                direction = i['direction']
                asteroid_lst.append(Asteroid(i['position'][0],i['position'][1],2*hw[2],2*hw[2],Source[2], direction, 'small'))
        self._asteroids = asteroid_lst

    
    def update(self, other):
        """
        It moves the ship and asteroid.
        """
        if self._ship == None:
            pass
            
        else:
            self._ship.turn_angle(other)
            self._ship.impulse(other)
            self._ship.wrapping()     
            
            for i in range(len(self._asteroids)):
                self._asteroids[i].wrapping()
                self._asteroids[i].moving()
            self.add_bullet(other)
            i = 0
            while i<len(self._bullets):
                self._bullets[i].moving()
                self._bullets[i].delbullet(Wave.bul_lst)
                i += 1
            self.detect_collision()
            self.ship_collision()
    
    
    
    def getLives(self):
        """
        Return: It return True or False
        It check the value of ship object is None or not.
        """
        return self._ship == None


    def setShip(self):
        """
        It sets the value of object ship
        """
        data = self._data
        x = data['ship']['position'][0]
        y = data['ship']['position'][1]
        angle = data['ship']['angle']
        self._ship = Ship(x, y, angle, SHIP_IMAGE)

        
    
    bul_lst = []
    def add_bullet(self, other):
        """
        It creates the bullet object and stores in the list which is class attribute
        bul_lst.
        Parameter Other: Other is a input object of Ginput
        """
        
        tip_ship = self._ship.getFace()*SHIP_RADIUS + self._ship.getPos() 
        
        if other.is_key_down('spacebar') and self._firerate >= BULLET_RATE: 
            Wave.bul_lst.append(Bullet(tip_ship.x, tip_ship.y, 2*BULLET_RADIUS, 2*BULLET_RADIUS, self._ship.getFace()*BULLET_SPEED))
            self._firerate = 0
        self._firerate += 1
        self._bullets = Wave.bul_lst

        


    def draw(self, view):
        """
        Draw the wave object to view
        Parameter view: view is the object of Game view.
        """
        if self._ship == None:
            for i in range(len(self._asteroids)):
                self._asteroids[i].draw(view)

        else:
            self._ship.draw(view)
            for i in range(len(self._asteroids)):
                self._asteroids[i].draw(view)
            for i in range(len(self._bullets)):
                self._bullets[i].draw(view)

    
    
    def detect_collision(self):
        """
        It detect the collision between bullet and asteroid
        """
        i = 0
        while i < len(self._bullets):
            self.Ast_collision(i)
            
            i += 1
        
    
    def Ast_collision(self, index):
        """
        It checks the condition of collision and call the method delete to remove bullet and 
        asteroid objects.
        Parameter index: It is index of bullet object for collision.
        """
        
        i = 0
        while i < len(self._asteroids):
            
            dist_bullet = ((self._bullets[index].x - self._asteroids[i].x)**2 + (self._bullets[index].y-self._asteroids[i].y)**2)**(0.5)
            
            if self._asteroids[i]._size=='large':
                if (LARGE_RADIUS + BULLET_RADIUS)>dist_bullet:
                    self.create_ast([i, index])
                    pewSound = Sound('pew1.wav')
                    pewSound.play()
                    self.delete([i, index])
                    break                

            elif self._asteroids[i]._size=='medium':
                if (MEDIUM_RADIUS + BULLET_RADIUS)>dist_bullet:
                    self.create_ast([i, index])
                    pewSound = Sound('pew1.wav')
                    pewSound.play()
                    self.delete([i, index])
                    break                    
                
            else:
                if (SMALL_RADIUS + BULLET_RADIUS)>dist_bullet:
                    pewSound = Sound('pew1.wav')
                    pewSound.play()
                    self.delete([i, index])
                    break
                
            i += 1
    
    
    
    def ship_collision(self):
        """
        It checks the condition of collision between ship and asteroid and delete the objects and create asteroid
        at the place.
        It sets the value of ship object to None after collision with asteroid.
        """

        i = 0
        while i < len(self._asteroids):
            if self._asteroids[i]._size == 'large':
                if self.Centre_dist(i) < LARGE_RADIUS + SHIP_RADIUS:
                    self.create_asteroid_ship(i)
                    self._lives -= 1
                    self._ship = None
                    del self._asteroids[i]
                    break
            elif self._asteroids[i]._size == 'medium':
                if self.Centre_dist(i) < MEDIUM_RADIUS + SHIP_RADIUS:
                    self.create_asteroid_ship(i)
                    self._lives -= 1
                    self._ship = None
                    del self._asteroids[i]
                    break
            else:
                if self.Centre_dist(i) < SMALL_RADIUS + SHIP_RADIUS:
                    self.create_asteroid_ship(i)
                    self._lives -= 1
                    self._ship = None
                    del self._asteroids[i]
                    break

            i += 1


    def create_asteroid_ship(self, index):
        """
        It creates asteroid after collision with the ship and asteroid.
        Parameter index: It is the index of asteroid object.
        """

        if self._ship.getVelocity().length() == 0:
            dir_ship = self._ship.getFace()*SHIP_MAX_SPEED
        else:
            dir_ship = self._ship.getVelocity()
        
        ast1_dir = Vector2((dir_ship.x)*cos(2*pi/3) - (dir_ship.y)*sin(2*pi/3), (dir_ship.x)*sin(2*pi/3)+(dir_ship.y)*cos(2*pi/3))
        ast2_dir = Vector2((dir_ship.x)*cos(-2*pi/3) - (dir_ship.y)*sin(-2*pi/3), (dir_ship.x)*sin(-2*pi/3)+(dir_ship.y)*cos(-2*pi/3))
        lst = [dir_ship, ast1_dir, ast2_dir]
        
        if self._asteroids[index]._size == 'large':
            
            for direction in lst:
                x = MEDIUM_RADIUS*(direction.normalize()).x + self._asteroids[index].x
                y = MEDIUM_RADIUS*(direction.normalize()).y + self._asteroids[index].y
                self._asteroids.append(Asteroid(x, y, 2*MEDIUM_RADIUS, 2*MEDIUM_RADIUS, MEDIUM_IMAGE, [direction.x, direction.y], 'medium'))
        
        if self._asteroids[index]._size == 'medium':
            
            for direction in lst:
                x = (SMALL_RADIUS*direction.normalize()).x + self._asteroids[index].x
                y = (SMALL_RADIUS*direction.normalize()).y + self._asteroids[index].y
                self._asteroids.append(Asteroid(x, y, 2*SMALL_RADIUS, 2*SMALL_RADIUS, SMALL_IMAGE, [direction.x, direction.y], 'small'))
            
        

    def Centre_dist(self,index):
        """
        Returns: It return the distance between centre of two objects.
        Parameter index: It is the index of asteroid objects
        """
        return ((self._ship.x - self._asteroids[index].x)**2 + (self._ship.y - self._asteroids[index].y)**2)**(0.5)



    def delete(self, other):
        """
        It delete the asteroid and bullet object
        Parameter other: other is the list of index of bullets and asteroid
        """
        del self._asteroids[other[0]]
        del self._bullets[other[1]]

    
    def create_ast(self,other):
        """
        It creates asteroid object after collision with the bullet
        Parameter other: other is the list of index of bullets and asteroid
        """
        dir_bullet = self._bullets[other[1]].getVelocity()
        ast1_dir = Vector2((dir_bullet.x)*cos(2*pi/3) - (dir_bullet.y)*sin(2*pi/3), (dir_bullet.x)*sin(2*pi/3)+(dir_bullet.y)*cos(2*pi/3))
        ast2_dir = Vector2((dir_bullet.x)*cos(-2*pi/3) - (dir_bullet.y)*sin(-2*pi/3), (dir_bullet.x)*sin(-2*pi/3)+(dir_bullet.y)*cos(-2*pi/3))
        
        lst = [dir_bullet, ast1_dir, ast2_dir]
        
        if self._asteroids[other[0]]._size == 'large':
            
            for direction in lst:
                x = MEDIUM_RADIUS*(direction.normalize()).x + self._asteroids[other[0]].x
                y = MEDIUM_RADIUS*(direction.normalize()).y + self._asteroids[other[0]].y
                self._asteroids.append(Asteroid(x, y, 2*MEDIUM_RADIUS, 2*MEDIUM_RADIUS, MEDIUM_IMAGE, [direction.x, direction.y], 'medium'))
        
        if self._asteroids[other[0]]._size == 'medium':
            
            for direction in lst:
                x = (SMALL_RADIUS*direction.normalize()).x + self._asteroids[other[0]].x
                y = (SMALL_RADIUS*direction.normalize()).y + self._asteroids[other[0]].y
                self._asteroids.append(Asteroid(x, y, 2*SMALL_RADIUS, 2*SMALL_RADIUS, SMALL_IMAGE, [direction.x, direction.y], 'small'))
        
        
    
