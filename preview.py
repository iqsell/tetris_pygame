# need realize bd with  scores, records, requests scores
from game import *
from settings import *
import sys

class Preview:

    def __init__(self):
        self.surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.rect = self.surface.get_rect(bottomright=(WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING))
        self.display_surface = pygame.display.get_surface()

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def start_screen(self):

        img_path = os.path.join('data', 'images.jpeg')
        gameover_img = pygame.image.load(img_path)
        gameover_img = pygame.transform.scale(gameover_img, (700, 850))
        self.display_surface.blit(gameover_img, (0, 0))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.flip()  # Обновление экрана после отрисовки
