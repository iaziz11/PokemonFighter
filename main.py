import pygame
from player import Player
from grid import Grid


#  pygame setup

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 20)
screen = pygame.display.set_mode((1280, 720))
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()
FLOOR_HEIGHT = 40
clock = pygame.time.Clock()
running = True
dt = 0

#  class setup

floor = pygame.Rect(0, screen.get_height() - FLOOR_HEIGHT, screen.get_width(), FLOOR_HEIGHT)
player1 = Player((SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2), (350, 40), "Player 1", my_font)
player2 = Player((2 * SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2), (350, 100),"Player 2", my_font)
p1_rect = player1.player_rect
p2_rect = player2.player_rect
grid1 = Grid((0, 0), player1, 60)
grid2 = Grid((((3 * SCREEN_WIDTH / 4) + 30, 0)), player2, 60)

#  main game loop

while running:
    #  poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                grid1.setSurfaces(1)
            if event.key == pygame.K_a:
                grid1.setSurfaces(-1)
            if event.key == pygame.K_RIGHT:
                grid2.setSurfaces(1)
            if event.key == pygame.K_LEFT:
                grid2.setSurfaces(-1)
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            grid1.checkClick(pos)
            grid2.checkClick(pos)
            

    #  move players and check for collisions if they are both alive
    if player1.alive and player2.alive:
        if player1.player_surface is not None and player2.player_surface is not None:

            #  horizontal collision
            player1.move_horizontal(SCREEN_WIDTH)
            player2.move_horizontal(SCREEN_WIDTH)
            
            if p1_rect.colliderect(p2_rect):
                if p1_rect.left < p2_rect.left:
                    p1_rect.right = p2_rect.left
                else:
                    p2_rect.right = p1_rect.left
                new_player1_horiz_vel = player1.horizontal_collision(player2.mass, player2.cur_vel[0])
                new_player2_horiz_vel = player2.horizontal_collision(player1.mass, player1.cur_vel[0])
                player1.cur_vel[0] = new_player1_horiz_vel
                player2.cur_vel[0] = new_player2_horiz_vel
            
            #  vertical collision
            player1.move_vertical(dt, SCREEN_HEIGHT - FLOOR_HEIGHT)
            player2.move_vertical(dt, SCREEN_HEIGHT - FLOOR_HEIGHT)

            if p1_rect.colliderect(p2_rect):
                if p1_rect.bottom > p2_rect.bottom:
                    p1_rect.top = p2_rect.bottom
                else:
                    p2_rect.top = p1_rect.bottom
                new_player1_vert_vel = player1.vertical_collision(player2.mass, player2.cur_vel[1])
                new_player2_vert_vel = player2.vertical_collision(player1.mass, player1.cur_vel[1])
                player1.cur_vel[1] = new_player1_vert_vel
                player2.cur_vel[1] = new_player2_vert_vel
    else:
        game_over_message = my_font.render("GAME OVER", False, (255, 0, 0))
        screen.blit(game_over_message, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            

    #  draw to screen
    screen.fill("purple")
    grid1.drawSurfaces(screen)
    grid2.drawSurfaces(screen)

    if player1.player_surface is not None:
        screen.blit(player1.player_surface, player1.player_rect)
    if player2.player_surface is not None:
        screen.blit(player2.player_surface, player2.player_rect)
    pygame.draw.rect(screen, "brown", floor)

    player1.draw_health_bars(screen)
    player2.draw_health_bars(screen)


    pygame.display.flip()

    #  limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
