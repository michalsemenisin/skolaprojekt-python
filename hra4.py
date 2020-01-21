import turtle
import math
import random
import sys
import os
from win32api import GetSystemMetrics
import datetime


print("Width =", GetSystemMetrics(0))
print("Height =", GetSystemMetrics(1))

#inicializace
hra = turtle.Screen()
#setup okna
hra.setup (width=900, height=900, startx=GetSystemMetrics(0)/4, starty=GetSystemMetrics(1)/12)
hra.bgcolor("red")
hra.title("Hra")
hra.register_shape("coin.gif")
hra.register_shape("asteroid1.gif")
run = True
hra.bgpic("pozadi2.gif")
health = turtle.Turtle()

class Game(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.hideturtle()
        self.speed(0)
        self.color("White")
        self.goto(-390,400)
        self.score = 0
        self.i = 0
    #Výpis skóre
    def update_score(self):
        self.clear()
        self.write("Score: {}".format(self.score), False, align="left", font=("Arial",14,"normal"))
    def update_health(self):
        health.penup()
        health.hideturtle()
        health.speed(0)
        health.color("white")
        health.goto(320,400)
        health.clear()
        if (player.life > -1):
            health.clear()
            health.write("Health: {}".format(player.life), False, align="left", font=("Arial",14,"normal"))
        if (player.life == 0):
            health.clear()
            health.goto(-130,0)
            health.write("GAME OVER, press R to restart", False, align="left", font=("Arial",14,"normal"))
    #Změna skóre
    def change_score(self, points):
        self.score += points
        self.update_score()
    #Funkce na ukládání
    def save(self):
        if player.life < 1 and self.i == 0:
            my_file = open("skore.txt", "a")
            my_file.write(str(datetime.datetime.now()))
            my_file.write(str("  -  "))            
            my_file.write(str(self.score))
            my_file.write("\n")
            self.i += 1
        
    #Funkce na restartování okna
    def restart_program(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)

#Ohraničení
class Border(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.hideturtle()
        self.speed(0)
        self.color("White")
        self.pensize(5)
    #Vykreslení ohraničení
    def draw_border(self):
        self.penup()
        self.goto(-400, -400)
        self.pendown()
        self.goto(-400, 400)
        self.goto(400, 400)
        self.goto(400, -400)
        self.goto(-400, -400)
#Hráč
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.shape("triangle")
        self.color("white")
        self.speed = 0.5
        self.life = 5
        self.rightTurn = False
        self.leftTurn = False
    #Funkce na pohyb
    def move(self):
        #Rychlost pohybu
        self.forward(self.speed)
        #Při naražení do ohraničení, odvrátit o 60 stupňů
        if self.xcor() > 390 or self.xcor() < -390:
            self.left(60)
        if self.ycor() > 390 or self.ycor() < -390:
            self.left(60)
        #Pohyb doboku
        if self.rightTurn:
            self.right(0.5)
        if self.leftTurn:
            self.left(0.5)
    
    #Poškození
    def health(self, damage):
        self.life -= damage
        print(self.life)


    #Funkce na pohyb
    def turnleft(self):
        self.leftTurn = True
    def turnright(self):
        self.rightTurn = True
    def turnleftrelease(self):
        self.leftTurn = False
    def turnrightrelease(self):
        self.rightTurn = False      
    def incspeed(self):
        if self.speed < 2:
            self.speed += 0.1
    def decspeed(self):
        if self.speed > 0.1:
            self.speed -= 0.1
class Npc(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.speed = 0.5
        self.goto(random.randint(-380,380), random.randint(-380,380))
        self.setheading(random.randint(0,360))
    #Při sebrání - Vložit zpět na plátno na náhodnou pozici
    def jump(self):
        self.goto(random.randint(-380,380), random.randint(-380,380))
        self.setheading(random.randint(0,360))

    def move(self):
        self.forward(self.speed)

        if self.xcor() > 390 or self.xcor() < -390:
            self.left(60)
        if self.ycor() > 390 or self.ycor() < -390:
            self.left(60)
#Npc na kladné body    
class Goal(Npc):
    def __init__(self):
        super().__init__()
        self.color("green")
        self.type = "ball"
        self.shape("coin.gif")
#Npc na záporné body
class Enemy(Npc):
    def __init__(self):
        super().__init__()
        self.type = "enemy"
        self.damage = 1
        self.color("black")
        self.shape("asteroid1.gif")


#Detekce kolize
def isCollision(t1, t2):
    a = t1.xcor() - t2.xcor()
    b = t1.ycor() - t2.ycor()
    distance = math.sqrt((a ** 2) + (b ** 2))
    #Sbírání
    if distance < 20:
        return True
    else:
        return False

player = Player()
border = Border()
game = Game()
border.draw_border()

#Objekty na plátně
entities = []
#Vkládání nových objektů
for count in range(6):
    entities.append(Goal())
    entities.append(Enemy())

#Klávesové zkratky
turtle.listen()
turtle.onkeypress(player.turnleft, "Left")
turtle.onkeypress(player.turnright, "Right")
turtle.onkeyrelease(player.turnleftrelease, "Left")
turtle.onkeyrelease(player.turnrightrelease, "Right")
turtle.onkey(player.incspeed, "Up")
turtle.onkey(player.decspeed, "Down")
turtle.onkey(hra.bye, "q")
turtle.onkey(game.restart_program, "r")
turtle.onkey(game.save, "p")
#Zrychlení hry
hra.tracer(0)

#Hlavní cyklus
while run:
        hra.update()
        player.move()
        for goal in entities:
            goal.move()
            if isCollision(player, goal):
                if(goal.type == "ball"):         
                    goal.jump()
                    game.update_health()
                    game.change_score(10)
                if(goal.type == "enemy"):         
                    goal.jump()
                    game.change_score(-10)
                    player.health(goal.damage)
                    game.update_health()

        game.save()
turtle.mainloop()