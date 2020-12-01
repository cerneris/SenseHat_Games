from sense_emu import *
import time
import random
import os

class FlappyPird:
    def __init__(self):
        self.Rd = (255, 0, 0)
        self.W = (0, 0, 0)

    # Create a new empty map
    def create_map(self):
        _map = [
            [self.W, self.W, self.W, self.W, self.W, self.W, self.W, self.W],
            [self.W, self.W, self.W, self.W, self.W, self.W, self.W, self.W],
            [self.W, self.W, self.W, self.W, self.W, self.W, self.W, self.W],
            [self.W, self.W, self.W, self.W, self.W, self.W, self.W, self.W],
            [self.W, self.W, self.W, self.W, self.W, self.W, self.W, self.W],
            [self.W, self.W, self.W, self.W, self.W, self.W, self.W, self.W],
            [self.W, self.W, self.W, self.W, self.W, self.W, self.W, self.W],
            [self.W, self.W, self.W, self.W, self.W, self.W, self.W, self.W]
            ]
        return _map

    # Set current max points
    def set_max_points(self, points):
        file = open("Points.txt", "w+")
        file.write(str(points))
        file.close()

    # Get current max points from text file, if file exists
    def get_max_points(self):
        try:
            if os.path.exists("Points.txt"):
                file = open("Points.txt", "r")
                max_points = int(file.readline())
                file.close()
            else:
                max_points = 0
        except:
            max_points = 0
        finally:
            return max_points

    # Check if the char is currently at a wall location
    def check_map(self, hat, char, _map):
        map_top = _map[7][char[0]]
        map_bot = _map[0][char[0]]
        if map_top == self.Rd or map_bot == self.Rd:
            return True
        else:
            return False

    # Check if the char hits a wall and return if it hit and give points if not. 
    def detect_collision(self, hat, mapx, char, points):
        _points = points
        hit = False
        print(mapx[char[1]][char[0]])
        if mapx[char[1]][char[0]] == self.Rd:
            hit = True
        else:
            _points += 1
        return _points, hit

    # Create a new random generated wall, with user given max pixel count.
    def createWall(self, wallPixelCount):
        wallPixel = 0
        wallPixelRand1 = 0
        wallPixelRand2 = random.randint(4, 7)
        if random.randint(0, 4) == 1:
            wallPixel = wallPixelRand1
        else:
            wallPixel = wallPixelRand2

        wall = [self.W, self.W, self.W, self.W, self.W, self.W, self.W, self.W]
        for x in range(wallPixelCount):
            wall[wallPixel] = self.Rd
            wallPixel = wallPixel + 1
            if wallPixel > 7:
                wallPixel = 0

        return wall

    # Add the wall to the map.
    def addWall(self, wall, _map):
        for x in range(8):
            #print("setting ", _map[7][x], " to ", wall[x])
            _map[x][7] = wall[x]
        return _map

    # Move the current map forward.
    def moveMap(self, _map):
        for y in range(1, 8):
            for x in range(8):
                _map[x][y-1] = _map[x][y]
                if _map[x][y] == self.Rd:
                    _map[x][y] = self.W
        return _map

    # Show a message, made for easier use of main menu.
    def message_shower(self, hat, choice, current_selection, color):
        hat.show_message("{}".format(choice[current_selection]), 0.05, color)

    # The main menu that is shown when the script is started.
    def main_menu(self, hat, color):
        choice = ["Start Game", "Exit Game", "Points"]
        current_selection = 0
        self.message_shower(hat, choice, current_selection, color)
        while True:
            event = hat.stick.wait_for_event(emptybuffer=True)
            if event.action == ACTION_PRESSED:
                if event.direction == DIRECTION_UP:
                        if current_selection == 2:
                            current_selection = 0
                        else:
                            current_selection += 1
                if event.direction == DIRECTION_DOWN:
                        if current_selection == 0:
                            current_selection = 2
                        else:
                            current_selection -= 1
                if event.direction == DIRECTION_MIDDLE:
                    choice = choice[current_selection]
                    break
            else:
                self.message_shower(hat, choice, current_selection, color)
        return choice

    # Countdown when start game button is clicked
    def countdown(self, hat, color):
        hat.show_message("3..", 0.05, color)
        hat.show_message("2..", 0.05, color)
        hat.show_message("1..", 0.05, color)
        hat.show_message("GO", 0.05, color)

    # Function to create a char of the selected color for the game.
    def char(self, color):
        x = 2
        y = 4
        char = [x, y, color]
        return char

    # Main game loop function.
    def game(self, hat, color, max_points):
        _map = self.create_map()
        game_char = self.char(color)
        wall_parameter = 0
        event_parameter = False
        points = 0
        hit = False
        timerTime = 0.5
        while True:
            if hit == True:
                hat.show_message("GAME OVER")
                hat.show_message("POINTS: {}".format(points))
                if points > max_points:
                    hat.show_message("NEW RECORD")
                    self.set_max_points(points)
                break
            flattenedList = []
            for x in range(8):
                for y in range(8):
                    flattenedList.append(_map[x][y])
            hat.set_pixels(flattenedList)
            hat.set_pixel(game_char[0], game_char[1], game_char[2])
            if wall_parameter % 4 == 0:
                wall = self.createWall(random.randrange(4,7))
                self.addWall(wall, _map)
            wall_parameter += 1
            current = game_char[1]
            for event in hat.stick.get_events():
                event_parameter = True
                if event.action == ACTION_PRESSED:
                    if event.direction == DIRECTION_MIDDLE:
                        game_char[1] = current - 1
                        if game_char[1] <= 0:
                            game_char[1] = 0
                            hat.set_pixel(game_char[0], game_char[1], game_char[2])
                        else:
                            hat.set_pixel(game_char[0], current, self.W)
                            hat.set_pixel(game_char[0], game_char[1], game_char[2])
            if game_char[1] >= 7:
                game_char[1] = 7
                # hat.show_message("GAME OVER", 0.05, color)
            else:
                if event_parameter == True:
                    event_parameter = False
                    pass
                else:
                    current = game_char[1]
                    game_char[1] = game_char[1] + 1
            time.sleep(timerTime)
            if timerTime > 0.1:
                timerTime -= 0.002
            hat.set_pixel(game_char[0], current, self.W)
            # If the char is currently at wall location, detect if it hits the wall.
            if self.check_map(hat, game_char, _map):
                points, hit = self.detect_collision(hat, _map, game_char, points)
                # Debug purposes
                print("Current points: {}".format(points))
            self.moveMap(_map)
            
    # Main loop that initiates the main menu.
    def main(self):
        color = (255, 255, 255)
        hat = SenseHat()
        while True:
            choice = self.main_menu(hat, color)
            max_points = self.get_max_points()
            if choice == "Start Game":
                self.countdown(hat, color)
                self.game(hat, color, max_points)
            if choice == "Points":
                hat.show_message("Max points: {}".format(max_points))
            if choice == "Exit Game":
                hat.show_message("GOODBYE", 0.05, color)
                exit()
            
    if __name__ == "__main__":
        main()
