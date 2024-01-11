import pygame


class healthBar:
    def __init__(self, pos, text, font) -> None:
        self.pos = pos
        self.green_rect = pygame.Rect(pos[0], pos[1], 600, 20)
        self.red_rect = pygame.Rect(pos[0], pos[1], 600, 20)
        self.text = font.render(text, False, (0,0,0))

    def draw(self, screen):
        pygame.draw.rect(screen, "red", self.red_rect)
        pygame.draw.rect(screen, "green", self.green_rect)
        screen.blit(self.text, (self.pos[0], self.pos[1] - 30))