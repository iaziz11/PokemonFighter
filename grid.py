import pygame

index_map = {
    0:0,
    1:5,
    2:10,
    3:15,
    4:20,
    5:1,
    6:6,
    7:11,
    8:16,
    9:21,
    10:2,
    11:7,
    12:12,
    13:17,
    14:22,
    15:3,
    16:8,
    17:13,
    18:18,
    19:23,
    20:4,
    21:9,
    22:14,
    23:19,
    24:24
}

inv_map = {v: k for k, v in index_map.items()}


class Grid:
    def __init__(self, starting_pos, player, block_size) -> None:
        self.pos = starting_pos
        self.player = player
        self.page_num = 0
        self.surfaces = []
        self.rects = []
        self.block_size = block_size
        self.setRects()
        self.setSurfaces()

    def setRects(self):
        for x in range(5):
            for y in range(5):
                rect = pygame.Rect(x * self.block_size + self.pos[0], y * self.block_size + self.pos[1], self.block_size, self.block_size)
                self.rects.append(rect)

    def setSurfaces(self, new_page=0):
        if self.page_num + new_page < 0 or self.page_num + new_page > 6:
            return
        self.surfaces.clear()
        self.page_num += new_page
        cur_idx = 25 * self.page_num + 1
        for _ in range(25):
            if cur_idx > 151:
                break
            img = pygame.image.load(f"./sprites/{cur_idx}.png")
            self.surfaces.append(img)
            cur_idx += 1

    def drawSurfaces(self, screen):
        for i in range(len(self.surfaces)):
            s = self.surfaces[i]
            r = self.rects[index_map[i]]
            screen.blit(s, r)

    def checkClick(self, mouse_pos):
        for idx_i, i in enumerate(self.rects):
            if i.collidepoint(mouse_pos):
                new_surface = self.surfaces[inv_map[idx_i]]
                self.player.player_surface = new_surface
                self.player.player_rect.update(self.player.player_rect.left, self.player.player_rect.top, new_surface.get_width(), new_surface.get_height())

