from sense_hat import SenseHat
import random
import time

class Snake:
    def __init__(self):
        pass
    def check_collision(self, snake):
        head = snake[0]
        tail = snake[1:]
        for parts in tail:
            if head == parts:
                return True
        else:
            return False
        
    def generate_food(self):
        rand_x = random.randint(0, 7)
        rand_y = random.randint(0, 7)
        return rand_x, rand_y
        
    def check_hit(self, x, y, food_x, food_y):
        if x == food_x and y == food_y:
            return True
        else:
            return False
        
    def main(self):
        white = (255, 255, 255)
        red = (255, 0, 0)
        sense = SenseHat()
        x = 3
        y = 4
        head = [x, y]
        snake = [head]
        food = self.generate_food()
        sense.clear()
        sense.set_pixel(x, y, white)
        key_pressed = {"up" : True, "down" : False, "left" : False, "right" : False}
        points = 0
        while True:
            for event in sense.stick.get_events():
                if event.action == "pressed":
                    if event.direction == "up":
                        if key_pressed["down"] == True:
                            pass
                        else:
                            for keys in key_pressed:
                                key_pressed[keys] = False
                            key_pressed["up"] = True
                            break
                    if event.direction == "down":
                        if key_pressed["up"] == True:
                            pass
                        else:
                            for keys in key_pressed:
                                key_pressed[keys] = False
                            key_pressed["down"] = True
                            break
                    if event.direction == "left":
                        if key_pressed["right"] == True:
                            pass
                        else:
                            for keys in key_pressed:
                                key_pressed[keys] = False
                            key_pressed["left"] = True
                            break
                    if event.direction == "right":
                        if key_pressed["left"] == True:
                            pass
                        else:
                            for keys in key_pressed:
                                key_pressed[keys] = False
                            key_pressed["right"] = True
                            break
            if key_pressed["up"]:
                if y > 0:
                    y -= 1
                else:
                    y = 7
            if key_pressed["down"]:
                if y < 7:
                    y += 1
                else:
                    y = 0
            if key_pressed["left"]:
                if x > 0:
                    x -= 1
                else:
                    x = 7
            if key_pressed["right"]:
                if x < 7:
                    x += 1
                else:
                    x = 0
            time.sleep(0.2)
            new_head = [x, y]
            sense.clear()
            print(x, y)
            snake.pop()
            snake.insert(0, new_head)
            if self.check_collision(snake):
                sense.show_message("GAME OVER")
                break
            for part in snake:
                sense.set_pixel(part[0], part[1], white)
                sense.set_pixel(food[0], food[1], white)
            if self.check_hit(snake[0][0], snake[0][1], food[0], food[1]):
                points += 1
                food = self.generate_food()
                tail = snake[0]
                snake.insert(len(snake), tail)
            print("Points: {}".format(points))

    if __name__ == '__main__':
        main()