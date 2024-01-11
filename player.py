import pygame, random, math
from health_bar import healthBar

class Player:
    def __init__(self, starting_pos, health_bar_pos, text, font, mass=1) -> None:
        self.player_surface = None
        self.cur_pos = starting_pos
        self.cur_vel = [0, 0]
        self.player_rect = pygame.Rect(self.cur_pos[0], self.cur_pos[1], 0, 0)
        self.mass = mass
        self.health = 600
        self.alive = True
        self.text = text
        self.base_damage_multiplier = 10
        self.health_bar = healthBar((health_bar_pos[0], health_bar_pos[1]), text, font)

        
    def move_horizontal(self, screen_width):
        self.player_rect.x += self.cur_vel[0]

        if self.player_rect.left < 0:
            self.player_rect.left = 0
            self.cur_vel[0] *= -1
        if self.player_rect.right > screen_width:
            self.player_rect.right = screen_width
            self.cur_vel[0] *= -1

    def move_vertical(self, dt, floor_y):
        self.cur_vel[1] += 10 * dt
        self.player_rect.y += self.cur_vel[1]
        if self.player_rect.bottom > floor_y:
            self.player_rect.bottom = floor_y
            # this results in a players death
            if self.cur_vel[1] < 5:
                self.cur_vel[0] = 0
                self.cur_vel[1] = 0
            else:
                # the range will eventually be determined by the mass of the player
                self.cur_vel[0] = random.randint(-10, 10)
                self.cur_vel[1] *= -1
        
        if self.player_rect.top < 0:
            self.player_rect.top = 0
            self.cur_vel[1] *= -0.2

    # https://unacademy.com/content/jee/study-material/physics/velocities-of-colliding-bodies-after-collision-in-1-dimension/
            
    # damage taken will be determined by others_vel and type advantage/disadvantage
    def horizontal_collision(self, others_mass, others_vel):
        type_multiplier = 1
        damage_taken = abs(others_vel) * type_multiplier * self.base_damage_multiplier
        self.health -= damage_taken
        if self.health <= 0:
            self.alive = False
            print(f"{self.text} died")
            self.health_bar.green_rect.update(self.health_bar.green_rect.left, self.health_bar.green_rect.top, 0, self.health_bar.green_rect.height)
            return 0
        
        self.health_bar.green_rect.update(self.health_bar.green_rect.left, self.health_bar.green_rect.top, self.health_bar.green_rect.width-damage_taken, self.health_bar.green_rect.height)
        return .75 * ((2 * others_mass * others_vel) + (self.cur_vel[0]*(others_mass - self.mass)))/others_mass + self.mass

    def vertical_collision(self, others_mass, others_vel):
        type_multiplier = 1
        damage_taken = abs(others_vel) * type_multiplier * self.base_damage_multiplier
        self.health -= damage_taken
        if self.health <= 0:
            self.alive = False
            print(f"{self.text} died")
            self.health_bar.green_rect.update(self.health_bar.green_rect.left, self.health_bar.green_rect.top, 0, self.health_bar.green_rect.height)
            return 0
        self.health_bar.green_rect.update(self.health_bar.green_rect.left, self.health_bar.green_rect.top, self.health_bar.green_rect.width-damage_taken, self.health_bar.green_rect.height)
        return .75 * ((2 * others_mass * others_vel) + (self.cur_vel[1]*(others_mass - self.mass)))/others_mass + self.mass

    def draw_health_bars(self, screen):
        self.health_bar.draw(screen)
        