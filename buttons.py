from settings import *
import pygame
import math
class Buttons():
    def __init__(self, app, colour, x, y, width, height, text='', radius=10):
        self.app = app
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.radius = 65  # Bán kính bo tròn các góc

    def draw_button(self, outline=None):
        # Draw button with rounded corners
        if outline:
            pygame.draw.rect(self.app.screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        
        # Create an off-screen surface for drawing the button
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, self.colour, (self.radius, 0, self.width - 2 * self.radius, self.height))  # Center rectangle
        pygame.draw.rect(button_surface, self.colour, (0, self.radius, self.width, self.height - 2 * self.radius))  # Middle rectangle

        # Draw rounded corners
        pygame.draw.circle(button_surface, self.colour, (self.radius, self.radius), self.radius)  # Top-left
        pygame.draw.circle(button_surface, self.colour, (self.width - self.radius, self.radius), self.radius)  # Top-right
        pygame.draw.circle(button_surface, self.colour, (self.radius, self.height - self.radius), self.radius)  # Bottom-left
        pygame.draw.circle(button_surface, self.colour, (self.width - self.radius, self.height - self.radius), self.radius)  # Bottom-right

        # Blit the button_surface onto the main screen
        self.app.screen.blit(button_surface, (self.x, self.y))

        # Draw text in the center of the button
        if self.text != '':
            font = pygame.font.SysFont(FONT, 16)
            text = font.render(self.text, True, (0, 0, 0))
            self.app.screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False