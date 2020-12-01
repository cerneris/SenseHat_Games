import click
from snake import Snake
from flappy_pird import FlappyPird
#from sense_hat import SenseHat
import time
import random
import os

@click.command()
@click.option("--game", help = "Choose game, snake or flappypird.")
def main(game):
    print("Starting game {}".format(game))
    if game == "snake":
        snake = Snake()
        snake.main()
    if game == "flappypird":
        flappy = FlappyPird()
        flappy.main()

if __name__ == '__main__':
    main()