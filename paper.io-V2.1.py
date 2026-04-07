import pygame
import math
import sys

# --- Configuration ---
WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_SPEED = 4
TURN_SPEED = 0.12 
TRAIL_GAP = 5     

# Colors
WHITE = (240, 240, 240)
BLUE  = (52, 152, 219)
TRAIL_BLUE = (174, 214, 241)
DARK_BLUE = (41, 128, 185)

class SmoothPlayer:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.angle = 0.0
        
        # Territory is a list of circles (simulating a filled area)
        self.territory = [pygame.Vector2(x, y)]
        self.home_radius = 50 
        
        self.trail = []
        self.is_outside = False
        self.alive = True

    def update(self):
        # 1. Mouse Steering
        mx, my = pygame.mouse.get_pos()
        target_angle = math.atan2(my - self.pos.y, mx - self.pos.x)
        diff = (target_angle - self.angle + math.pi) % (2 * math.pi) - math.pi
        self.angle += diff * TURN_SPEED

        # 2. Movement
        vel = pygame.Vector2(math.cos(self.angle), math.sin(self.angle)) * PLAYER_SPEED
        self.pos += vel

        # 3. Territory Logic
        dist_to_home = self.pos.distance_to(self.territory[0])
        
        # Are we outside our starting home?
        if dist_to_home > self.home_radius:
            if not self.is_outside:
                self.is_outside = True
            
            # Leave a trail point every few pixels
            if not self.trail or self.pos.distance_to(self.trail[-1]) > TRAIL_GAP:
                self.trail.append(pygame.Vector2(self.pos))
        else:
            # We are inside home! 
            if self.is_outside:
                # Capture: Add trail to territory and clear trail
                self.territory.extend(self.trail)
                self.trail = []
                self.is_outside = False

    def draw(self, surface):
        # Draw Territory (The safe zone)
        for p in self.territory:
            pygame.draw.circle(surface, TRAIL_BLUE, (int(p.x), int(p.y)), 15)
        
        # Draw the starting "Base" circle so you can see where to return
        pygame.draw.circle(surface, DARK_BLUE, (int(self.territory[0].x), int(self.territory[0].y)), self.home_radius, 2)

        # Draw Trail (The dangerous part)
        if len(self.trail) > 1:
            pygame.draw.lines(surface, BLUE, False, [p for p in self.trail], 5)
        
        # Draw Player Head
        pygame.draw.circle(surface, DARK_BLUE, (int(self.pos.x), int(self.pos.y)), 10)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    player = SmoothPlayer(WIDTH//2, HEIGHT//2)

    while player.alive:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        player.update()
        
        # Simple Wall Death
        if not (0 < player.pos.x < WIDTH and 0 < player.pos.y < HEIGHT):
            player.alive = False

        player.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    print("Hit the wall! Game Over.")
    pygame.quit()

if __name__ == "__main__":
    main()