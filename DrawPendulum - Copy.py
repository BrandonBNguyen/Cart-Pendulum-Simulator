import turtle
import math
from time import sleep


class DrawPendulum():

    def __init__(self, length, scale=800):
        self.scale = scale  # Represents the number of pixel lengths per meter

        # Create Turtle screen and update as needed.
        self.win = turtle.Screen()
        self.win.bgcolor("black")
        self.win.setup(width=800, height=800)
        self.win.tracer(0)

        # Draw track
        track_length = 700
        track_height = 20
        track_turtle = turtle.Turtle()
        track_turtle.color("white", "black")
        track_turtle.hideturtle()
        track_turtle.speed(0)
        track_turtle.penup()
        track_turtle.goto(track_length / 2, track_height / 2)
        track_turtle.pendown()
        track_turtle.begin_fill()
        track_turtle.goto(track_length / 2, -track_height / 2)
        track_turtle.goto(-track_length / 2, -track_height / 2)
        track_turtle.goto(-track_length / 2, track_height / 2)
        track_turtle.goto(track_length / 2, track_height / 2)
        track_turtle.end_fill()
        track_turtle.penup()

        # Cart draw properties
        self.cart_height = 50
        self.cart_length = 100
        self.cart_turtle = turtle.Turtle()
        self.cart_turtle.color("white", "black")
        self.cart_turtle.hideturtle()
        self.cart_turtle.speed(0)
        self.cart_turtle.penup()

        # Pendulum draw properties
        self.pendulum_length = length * self.scale
        self.pendulum_radius = 15
        self.pendulum_turtle = turtle.Turtle()
        self.pendulum_turtle.color("white", "black")
        self.pendulum_turtle.hideturtle()
        self.pendulum_turtle.speed(0)
        self.pendulum_turtle.penup()

    def draw(self, u):
        x, theta = u[0:3]
        x = x * self.scale

        # Draw cart
        self.cart_turtle.clear()
        self.cart_turtle.goto(x + self.cart_length / 2, self.cart_height / 2)
        self.cart_turtle.pendown()
        self.cart_turtle.begin_fill()
        self.cart_turtle.goto(x + self.cart_length / 2, - self.cart_height / 2)
        self.cart_turtle.goto(x - self.cart_length / 2, - self.cart_height / 2)
        self.cart_turtle.goto(x - self.cart_length / 2, self.cart_height / 2)
        self.cart_turtle.goto(x + self.cart_length / 2, self.cart_height / 2)
        self.cart_turtle.end_fill()
        self.cart_turtle.penup()

        # Draw pendulum
        self.pendulum_turtle.clear()
        self.pendulum_turtle.goto(x + self.pendulum_radius * math.cos(theta), self.pendulum_radius * math.sin(theta))
        self.pendulum_turtle.setheading(90 + theta*180/math.pi)
        self.pendulum_turtle.pendown()
        self.pendulum_turtle.begin_fill()
        self.pendulum_turtle.forward(self.pendulum_length - self.pendulum_radius)
        self.pendulum_turtle.circle(self.pendulum_radius, 180)
        self.pendulum_turtle.forward(self.pendulum_length - self.pendulum_radius)
        self.pendulum_turtle.circle(self.pendulum_radius, 180)
        self.pendulum_turtle.end_fill()
        self.pendulum_turtle.penup()

        # Update screen
        self.win.update()


if __name__ == "__main__":
    drawing = DrawPendulum(0.4)
    drawing.draw([0, 0])
    sleep(3)