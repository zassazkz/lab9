import pygame

pygame.init()  # Initialize pygame

screen = pygame.display.set_mode((800, 600))  # Set window dimensions

clock = pygame.time.Clock()  # Create Clock object to control FPS

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen.fill(WHITE)  # Fill screen with white color
pygame.display.flip()  # Update the display

colors = [RED, GREEN, BLUE]  # List of available colors
color = BLACK  # Default color

eraser = pygame.image.load('paint2/eraser.webp')  # Load eraser image
eraser = pygame.transform.scale(eraser, (70, 70))  # Resize image
eraser_rect = eraser.get_rect(topleft=(1010, 0))  # Define rectangle area for eraser

# Function to draw color selection rectangles
def draw_rect(index):
    pygame.draw.rect(screen, colors[index], (index*40, 0, 40, 40))

# Function to determine selected color
def pick_color():
    click = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    if click[0]:
        if 0 <= x <= 40 and 0 <= y <= 40:
            return RED
        elif 40 < x <= 80 and 0 <= y <= 40:
            return GREEN
        elif 80 < x <= 120 and 0 <= y <= 40:
            return BLUE
        elif 1010 <= x <= 1080 and 0 <= y <= 40:
            return BLACK
    return color

# Function for painting on screen
def painting(color, mode):
    click = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    if click[0] and not (0 <= x <= 400 and 0 <= y <= 90):
        if mode == 'circle':
            pygame.draw.circle(screen, color, (x, y), 27)
        elif mode == 'rect':
            pygame.draw.rect(screen, color, (x, y, 40, 40), 4)
        elif mode == 'equal_triangle':
            pygame.draw.polygon(screen, color, ((x,y), (x+20, y-40), (x+40, y)))
        elif mode == 'eraser':
            pygame.draw.circle(screen, WHITE, (x, y), 20)  

mode = 'circle'  # Initial mode - circle

# Function to draw text on screen
font_size = 24
font = pygame.freetype.SysFont("Arial", font_size)

def draw_text(text, position, color):
    font.render_to(screen, position, text, color)
    
draw_text("E: Eraser", (10, 40), BLACK)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:  # Check if 'E' key is pressed
                mode = 'eraser'

    for i in range(len(colors)):
        draw_rect(i)  # Draw color selection rectangles

    screen.blit(eraser, (1010, 0))  # Display eraser image
    rect = pygame.draw.rect(screen, (0,0,0), (130, 0, 40, 40), 3)
    circle = pygame.draw.circle(screen, (0,0,0), (197, 20), 23, 3)
    equal = pygame.draw.polygon(screen, (0,0,0), ((230, 0), (230, 40), (270, 40)), 3)

    pos = pygame.mouse.get_pos()
    if rect.collidepoint(pos):
        mode = "rect"
    if circle.collidepoint(pos):
        mode = "circle"
    if equal.collidepoint(pos):
        mode = 'equal_triangle'
    if eraser_rect.collidepoint(pos):  
        mode = 'eraser'

    color = pick_color()
    painting(color, mode)  # Draw with selected color and mode

    clock.tick(370)  # Set FPS
    pygame.display.update()
