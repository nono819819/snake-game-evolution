import pygame
import math
import sys

# --- Configuration ---
WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_SPEED = 4
TURN_SPEED = 0.1
TRAIL_GAP = 10 

# Colors
BG_COLOR = (236, 240, 241)
MAIN_COLOR = (52, 152, 219)    # Solid Blue
FILL_COLOR = (174, 214, 241)    # Light Blue
BORDER_COLOR = (41, 128, 185)   # Dark Blue

class Player:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.angle = 0.0
        
        # Start with a small square territory
        self.territory = [
            pygame.Vector2(x-40, y-40),
            pygame.Vector2(x+40, y-40),
            pygame.Vector2(x+40, y+40),
            pygame.Vector2(x-40, y+40)
        ]
        
        self.trail = []
        self.is_outside = False
        self.alive = True

    def is_inside_polygon(self, point, polygon):
        """Checks if a point is inside the territory polygon."""
        n = len(polygon)
        inside = False
        p1x, p1y = polygon[0].x, polygon[0].y
        for i in range(n + 1):
            p2x, p2y = polygon[i % n].x, polygon[i % n].y
            if point.y > min(p1y, p2y):
                if point.y <= max(p1y, p2y):
                    if point.x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (point.y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or point.x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

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
        currently_inside = self.is_inside_polygon(self.pos, self.territory)

        if not currently_inside:
            self.is_outside = True
            # Record trail
            if not self.trail or self.pos.distance_to(self.trail[-1]) > TRAIL_GAP:
                self.trail.append(pygame.Vector2(self.pos))
        else:
            if self.is_outside and len(self.trail) > 2:
                # HIT HOME: Add trail to territory
                # This simple version just appends. 
                # A full 'fill' requires complex math, so we extend the shape.
                self.territory.extend(self.trail)
                self.trail = []
                self.is_outside = False

    def draw(self, surface):
        # Draw Territory Polygon
        if len(self.territory) > 2:
            pygame.draw.polygon(surface, FILL_COLOR, self.territory)
            pygame.draw.polygon(surface, BORDER_COLOR, self.territory, 3)

        # Draw Trail
        if len(self.trail) > 1:
            pygame.draw.lines(surface, MAIN_COLOR, False, self.trail, 6)
        
        # Draw Player
        pygame.draw.circle(surface, BORDER_COLOR, (int(self.pos.x), int(self.pos.y)), 12)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    player = Player(WIDTH//2, HEIGHT//2)

    while player.alive:
        screen.fill(BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        player.update()
        
        # Wall Check
        if not (0 < player.pos.x < WIDTH and 0 < player.pos.y < HEIGHT):
            player.alive = False

        player.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    print("Game Over!")
    pygame.quit()

if __name__ == "__main__":
    main()