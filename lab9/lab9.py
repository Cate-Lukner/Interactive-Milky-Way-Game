""" Razors and Rubies Game
The player must collect as many rubies as they
can while avoiding the razors.
 """

# Imports
import random
import math
import arcade


# --- Constants ---
SPRITE_SCALING_PLAYER = 0.6
SPRITE_SCALING_RUBY = 0.3
SPRITE_SCALING_RAZOR = 0.3
RUBY_COUNT = 50
RAZOR_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Ruby(arcade.Sprite):
    """
    This class represents the rubies on our screen. It is a
    child class of the arcade library's "Sprite" class.
    """

    def __init__(self, filename, sprite_scaling):
        """ Constructor Function """

        # Calls __init__ function from parent class
        super().__init__(filename, sprite_scaling)

        # current angle in radians
        self.circle_angle = 0

        # How far away form the center to orbit (pixels)
        self.circle_radius = 0
        self.circle_speed = 0.008

        # Set the center of the point we orbit
        self.circle_center_x = 0
        self.circle_center_y = 0


    def update(self):
        """ Updates the rubies locations, thus animating
        them. """

        # Caclulate a new x, y
        self.center_x = self.circle_radius * math.sin(
            self.circle_angle
        ) + self.circle_center_x
        self.center_y = self.circle_radius * math.cos(
            self.circle_angle
        ) + self.circle_center_y

        # The angle of the rubies moves in increments
        # of the circle speed
        self.circle_angle += self.circle_speed

class Razors(arcade.Sprite):
    """
    This class represents the razors on our screen. It is a
    child class of the arcade library's "Sprite" class.
    """

    def __init__(self, filename, sprite_scaling):
        """ Constructor function """

        # Calls the __init__ function of parent class
        super().__init__(filename, sprite_scaling)
    
    def reset_position(self):
        """ Resets the position of the razors in a random
        x and y to the right of the screen after they
        have slid off the screen. """

        # random y
        self.center_y = random.randrange(SCREEN_HEIGHT)

        # random x to right of the screen
        self.center_x = random.randrange(
            SCREEN_WIDTH + 20, SCREEN_WIDTH + 100
        )
    
    def update(self):
        """ Updates the razors positions causing them
        to animate in a sliding motion. """

        # Move the razors left in increments of 1
        self.center_x -= 1

        # Reset the positon of the razors after
        # they have slid off the screen. 
        if self.left < -2:
            self.reset_position()



class MyGame(arcade.Window):
    """ MyGame class has as all the attributes and methods 
    associated with our game window.  """

    def __init__(self):
        """ Initializer """

        # Call the parent class initializer
        super().__init__(
            SCREEN_WIDTH, SCREEN_HEIGHT, "Rubies and Razors"
            )

        # Variables that will hold sprite lists
        self.player_list = None
        self.ruby_list = None
        self.razor_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        # Sounds downloaded from ZapSplat.com
        self.razor_sound = arcade.load_sound(
            "sound_effects/razor.mp3"
            )
        self.ruby_sound = arcade.load_sound(
            "sound_effects/ruby_sound.mp3"
            )




    def setup(self):
        """ Set up the game and initalize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.ruby_list = arcade.SpriteList()
        self.razor_list = arcade.SpriteList()
        self.tile_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the player
        # Character image from kenney.nl
        self.player_sprite = arcade.Sprite(
            "images/character_jumping.png", 
            SPRITE_SCALING_PLAYER
            )
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)


        # Instigates rubies of random x and y positions and
        # adds them to the ruby_list
        for i in range(RUBY_COUNT):

            # Ruby image from kenney.nl
            ruby = Ruby(
                "images/rubies.png", SPRITE_SCALING_RUBY
                )

            ruby.circle_center_x = random.randrange(
                SCREEN_WIDTH
            )
            ruby.circle_center_y = random.randrange(
                SCREEN_HEIGHT
            )

            ruby.circle_radius = random.randrange(10, 200)
            ruby.circle_angle = random.random() * 2 * math.pi

            self.ruby_list.append(ruby)

        # Instigates razors of random x and y positions and
        # adds them to the razor_list
        for i in range(RAZOR_COUNT):

            # Razor image from kenney.nl
            razor = Razors(
                "images/blue_razor.png", SPRITE_SCALING_RAZOR
                )

            razor.center_x = random.randrange(SCREEN_WIDTH)
            razor.center_y = random.randrange(SCREEN_HEIGHT)

            self.razor_list.append(razor)
        

        
    def on_draw(self):
        """ Draw Everything. """
        arcade.start_render()

        # Milky Way Background texture
        texture = arcade.load_texture("images/milky_way.jpg")
        arcade.draw_texture_rectangle(
            SCREEN_WIDTH//2, SCREEN_HEIGHT // 2, 
            SCREEN_WIDTH, SCREEN_HEIGHT, 
            texture
            )

        # Draw player, rubies, and razors
        self.ruby_list.draw()
        self.player_list.draw()
        self.razor_list.draw()

        # Put the score text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(
            output, 10, 20, arcade.color.WHITE, 14
        )

        # Draw Game Over text when all rubies
        # are captured by player
        if len(self.ruby_list) == 0:
            game_over_text = "GAME OVER"
            arcade.draw_text(
                game_over_text, 150, 300, 
                arcade.color.GREEN, 72
            )


    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the
        # mouse x, y
        if len(self.ruby_list) > 0:
            self.player_sprite.center_x = x 
            self.player_sprite.center_y = y 
        
    def update(self, delta_time):
        """ Movement and game Logic """
        
        # Call update on all sprites
        if len(self.ruby_list) > 0:
            self.ruby_list.update()
            self.razor_list.update()


        # Generate list of all sprites that collided with
        # the player
        rubies_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.ruby_list
        )
        razor_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.razor_list, 
        )

        # Loop through each colliding ruby, remove it,
        # add to the score, and play sound effect
        for ruby in rubies_hit_list:
            ruby.kill()
            self.score += 1
            arcade.play_sound(self.ruby_sound)

        # Loop through each colliding razor, remove it,
        # add to the score, and play sound effect
        for razor in razor_hit_list:
            razor.kill()
            self.score -= 1
            arcade.play_sound(self.razor_sound)



def main():
    """ Main method """

    # Create instance of window class
    window = MyGame()

    # Start the game
    window.setup()
    arcade.run()

# Call main function
if __name__ == "__main__":
    main()