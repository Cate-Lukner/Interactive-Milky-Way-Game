""" Sprite Sample Program """

import random
import math
import arcade
from sys import argv

# coin_motion can be sliding, bouncing, line_dancing
script, coin_motion = argv

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
COIN_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Coin(arcade.Sprite):
    """
    This class represents the coins on our screen. It is a
    child class of the arcade library's "Sprite" class.
    """

    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)

        if coin_motion == "bouncing":
            self.change_x = 0
            self.change_y = 0

        elif coin_motion == "circling":
            # current angle in radians
            self.circle_angle = 0

            # How far away form the center to orbit (pixels)
            self.circle_radius = 0
            self.circle_speed = 0.008

            # Set the center of the point we orbit
            self.circle_center_x = 0
            self.circle_center_y = 0


    def reset_position(self):
        # Reset the coin to a random spot above the screen
        self.center_y = random.randrange(
            SCREEN_HEIGHT + 20, SCREEN_HEIGHT + 100
        )
        self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self):

        if coin_motion == "sliding":
            # Move the coin
            self.center_y -= 1

            # See if the coin has fallen off the bottom of the
            # the screen. If so, reset it. 
            if self.top < 0:
                self.reset_position()
        elif coin_motion == "bouncing" or coin_motion == "line_dancing":
            
            # Move the coin
            self.center_x += self.change_x
            self.center_y += self.change_y

            # If we are out-of-bounds, then 'bounce'
            if self.left < 0 or self.right > SCREEN_WIDTH:
                self.change_x *= -1

            if self.bottom < 0 or self.top > SCREEN_HEIGHT:
                self.change_y *= -1
        elif coin_motion == "circling":
            # Caclulate a new x, y
            self.center_x = self.circle_radius * math.sin(
                self.circle_angle
            ) + self.circle_center_x
            self.center_y = self.circle_radius * math.cos(
                self.circle_angle
            ) + self.circle_center_y

            self.circle_angle += self.circle_speed         

class MyGame(arcade.Window):
    """ Our custom Window Class """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(
            SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example"
            )

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initalize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the player
        # Character image from kenney.nl
        self.player_sprite = arcade.Sprite(
            "images/character.png", SPRITE_SCALING_PLAYER
            )
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Create the coins
        for i in range(COIN_COUNT):

            # Create the coin instance
            # Coin image from kenney.nl
            coin = Coin(
                "images/coin_01.png", SPRITE_SCALING_COIN
                )

            # Position the coin
            if coin_motion == "sliding":
                coin.center_x = random.randrange(SCREEN_WIDTH)
                coin.center_y = random.randrange(SCREEN_HEIGHT)

            elif coin_motion == "bouncing":
                coin.center_x = random.randrange(SCREEN_WIDTH)
                coin.center_y = random.randrange(SCREEN_HEIGHT)
                coin.change_x = random.randrange(-3, 4)
                coin.change_y = random.randrange(-3, 4)

            elif coin_motion == "line_dancing":
                coin.center_x = 400

                coin.center_y += 5 + i * 20
                coin.change_y = 0
                
                if i%2 == 0:
                    coin.change_x = -3
                else:
                    coin.change_x = 3

            elif coin_motion == "circling":
                coin.circle_center_x = random.randrange(
                    SCREEN_WIDTH
                )
                coin.circle_center_y = random.randrange(
                    SCREEN_HEIGHT
                )

                coin.circle_radius = random.randrange(10, 200)
                coin.circle_angle = random.random() * 2 * math.pi

            # Add the coin to the lists
            self.coin_list.append(coin)
        

        
    def on_draw(self):
        """ Draw Everything. """
        arcade.start_render()

        self.coin_list.draw()
        self.player_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(
            output, 10, 20, arcade.color.WHITE, 14
        )

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the
        # mouse x, y

        self.player_sprite.center_x = x 
        self.player_sprite.center_y = y 
        
    def update(self, delta_time):
        """ Movement and game Logic """
        
        # Call update on all sprites
        self.coin_list.update()

        # Generate list of all sprites that collided with
        # the player
        coins_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.coin_list
        )

        # Loop through each colliding sprite, remove it,
        # and add to the score

        for coin in coins_hit_list:
            coin.kill()
            self.score += 1


def main():
    """ Main method """
    window = MyGame()
    window.setup()

    arcade.run()

if __name__ == "__main__":
    main()