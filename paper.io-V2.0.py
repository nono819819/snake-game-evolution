import pygame
import math
import sys

# --- Configuration ---
WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_SPEED = 4
TURN_SPEED = 0.1  # How fast the player rotates
TRAIL_GAP = 5     # Distance between points in the trail for smoothness

# Colors
WHITE = (240, 240, 240)
BLUE  = (52, 152, 219)
TRAIL_BLUE = (174, 214, 241)
RED   = (231, 76, 60)

class SmoothPlayer:
    def __init__(self, x, y, color, trail_color):
        self.pos = pygame.Vector2(x, y)
        self.angle = 0.0
        self.color = color
        self.trail_color = trail_color
        
        self.territory = [] # List of polygons/points
        self.trail = [pygame.Vector2(x, y)]
        self.alive = True

    def update(self):
        # 1. Get Mouse Position to Steer
        mouse_x, mouse_y = pygame.mouse.get_pos()
        target_angle = math.atan2(mouse_y - self.pos.y, mouse_x - self.pos.x)
        
        # 2. Smoothly rotate towards the mouse
        angle_diff = (target_angle - self.angle + math.pi) % (2 * math.pi) - math.pi
        self.angle += angle_diff * TURN_SPEED

        # 3. Move Forward
        velocity = pygame.Vector2(math.cos(self.angle), math.sin(self.angle)) * PLAYER_SPEED
        self.pos += velocity

        # 4. Add to trail if moved far enough (prevents massive lists)
        if self.pos.distance_to(self.trail[-1]) > TRAIL_GAP:
            self.trail.append(pygame.Vector2(self.pos))

    def draw(self, surface):
        # Draw the trail as a thick line
        if len(self.trail) > 1:
            pygame.draw.lines(surface, self.trail_color, False, [p for p in self.trail], 10)
        
        # Draw the "Head" (Circle)
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), 12)

    def check_bounds(self):
        if self.pos.x < 0 or self.pos.x > WIDTH or self.pos.y < 0 or self.pos.y > HEIGHT:
            self.alive = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Smooth Paper.io - Mouse Control")
    clock = pygame.time.Clock()

    player = SmoothPlayer(WIDTH//2, HEIGHT//2, BLUE, TRAIL_BLUE)

    while player.alive:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update Logic
        player.update()
        player.check_bounds()

        # Draw Logic
        player.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    print("Game Over! You hit the wall.")
    pygame.quit()

if __name__ == "__main__":
    main()