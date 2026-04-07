import pygame
import sys

# --- Configuration ---
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
FPS = 15

# Colors
WHITE = (255, 255, 255)
GRAY  = (200, 200, 200)
P1_COLOR = (52, 152, 219)  # Blue
P1_TRAIL = (174, 214, 241)
P2_COLOR = (231, 76, 60)   # Red
P2_TRAIL = (245, 183, 177)

class Player:
    def __init__(self, x, y, color, trail_color, controls):
        self.pos = [x, y]
        self.color = color
        self.trail_color = trail_color
        self.controls = controls # [Up, Down, Left, Right]
        self.direction = [0, 0]
        self.territory = set([(x, y)])
        self.trail = []
        self.alive = True

    def move(self):
        if self.direction != [0, 0]:
            new_x = self.pos[0] + self.direction[0] * GRID_SIZE
            new_y = self.pos[1] + self.direction[1] * GRID_SIZE
            self.pos = [new_x, new_y]
            
            # If outside territory, leave a trail
            if (self.pos[0], self.pos[1]) not in self.territory:
                self.trail.append(tuple(self.pos))
            else:
                # If returned to territory, solidify the trail
                if self.trail:
                    self.territory.update(self.trail)
                    self.trail = []

    def check_collision(self, other_player):
        # Wall collision
        if not (0 <= self.pos[0] < WIDTH and 0 <= self.pos[1] < HEIGHT):
            self.alive = False
        
        # Trail collision (Hit your own trail or enemy trail)
        pos_tuple = tuple(self.pos)
        if pos_tuple in self.trail[:-1]: # Hit own trail
            self.alive = False
        if pos_tuple in other_player.trail: # Hit enemy trail
            other_player.alive = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    p1 = Player(100, 100, P1_COLOR, P1_TRAIL, [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d])
    p2 = Player(600, 400, P2_COLOR, P2_TRAIL, [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Handle Inputs
            if event.type == pygame.KEYDOWN:
                # Player 1
                if event.key == p1.controls[0] and p1.direction != [0, 1]: p1.direction = [0, -1]
                elif event.key == p1.controls[1] and p1.direction != [0, -1]: p1.direction = [0, 1]
                elif event.key == p1.controls[2] and p1.direction != [1, 0]: p1.direction = [-1, 0]
                elif event.key == p1.controls[3] and p1.direction != [-1, 0]: p1.direction = [1, 0]
                # Player 2
                if event.key == p2.controls[0] and p2.direction != [0, 1]: p2.direction = [0, -1]
                elif event.key == p2.controls[1] and p2.direction != [0, -1]: p2.direction = [0, 1]
                elif event.key == p2.controls[2] and p2.direction != [1, 0]: p2.direction = [-1, 0]
                elif event.key == p2.controls[3] and p2.direction != [-1, 0]: p2.direction = [1, 0]

        # Logic
        p1.move()
        p2.move()
        p1.check_collision(p2)
        p2.check_collision(p1)

        if not p1.alive or not p2.alive:
            print("Game Over!")
            break

        # Draw
        screen.fill(WHITE)
        for p in [p1, p2]:
            # Draw Territory
            for tile in p.territory:
                pygame.draw.rect(screen, p.trail_color, (tile[0], tile[1], GRID_SIZE, GRID_SIZE))
            # Draw Trail
            for tile in p.trail:
                pygame.draw.rect(screen, p.color, (tile[0], tile[1], GRID_SIZE, GRID_SIZE), 2)
            # Draw Player Head
            pygame.draw.rect(screen, p.color, (p.pos[0], p.pos[1], GRID_SIZE, GRID_SIZE))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
