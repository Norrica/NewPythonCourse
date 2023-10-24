# Imports
import pygame

# Settings
''' window '''
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "Name of Game"
FPS = 60

''' colors '''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

''' fonts '''
TITLE_FONT = None
DEFAULT_FONT = None

# Make window
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Load assets
font_sm = pygame.font.Font(DEFAULT_FONT, 24)
font_md = pygame.font.Font(DEFAULT_FONT, 32)
font_xl = pygame.font.Font(TITLE_FONT, 96)


# Scenes
class Scene():
    def __init__(self):
        self.next_scene = self

    def process_input(self, events, pressed_keys):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

    def terminate(self):
        self.next_scene = None


class TitleScene(Scene):
    def __init__(self):
        super().__init__()

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_scene = PlayScene()

    def update(self):
        pass

    def render(self):
        screen.fill(BLACK)
        text = font_xl.render(TITLE, 1, WHITE)
        rect = text.get_rect()
        rect.centerx = SCREEN_WIDTH // 2
        rect.centery = SCREEN_HEIGHT // 2
        screen.blit(text, rect)


class PlayScene(Scene):
    def __init__(self):
        super().__init__()

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_scene = EndScene()

    def update(self):
        pass

    def render(self):
        screen.fill(BLACK)
        text = font_xl.render("Playing", 1, WHITE)
        rect = text.get_rect()
        rect.centerx = SCREEN_WIDTH // 2
        rect.centery = SCREEN_HEIGHT // 2
        screen.blit(text, rect)


class EndScene(Scene):
    def __init__(self):
        super().__init__()

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_scene = TitleScene()

    def update(self):
        pass

    def render(self):
        screen.fill(BLACK)
        text = font_xl.render("Game Over", 1, WHITE)
        rect = text.get_rect()
        rect.centerx = SCREEN_WIDTH // 2
        rect.centery = SCREEN_HEIGHT // 2
        screen.blit(text, rect)


# Main game class
class Game():
    def __init__(self):
        self.active_scene = TitleScene()

    def is_quit_event(self, event, pressed_keys):
        x_out = event.type == pygame.QUIT
        ctrl = pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]
        q = pressed_keys[pygame.K_q]

        return x_out or (ctrl and q)

    def run(self):
        while self.active_scene != None:
            # Get user input
            pressed_keys = pygame.key.get_pressed()
            filtered_events = []

            for event in pygame.event.get():
                if self.is_quit_event(event, pressed_keys):
                    self.active_scene.terminate()
                else:
                    filtered_events.append(event)

            # Manage scene
            self.active_scene.process_input(filtered_events, pressed_keys)
            self.active_scene.update()
            self.active_scene.render()
            self.active_scene = self.active_scene.next_scene

            # Update and tick
            pygame.display.flip()
            clock.tick(FPS)


# Let's do this!
if __name__ == "__main__":
    g = Game()
    g.run()
    pygame.quit()