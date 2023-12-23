from preview import Preview
from settings import *
from sys import exit
from Register import *

# components
from game import Game
from score import Score
from random import choice



# ---------------pygame---------------
class Main:
    def __init__(self):

        # general
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Tetris')

        # shapes
        self.next_shapes = [choice(list(TETROMINOS.keys())) for shape in range(3)]

        # components
        self.game = Game(self.get_next_shape, self.update_score)
        self.score = Score()
        self.preview = Preview()
        self.login = LoginWindow()

    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice(list(TETROMINOS.keys())))
        return next_shape

    def run(self):
        Reg_Window()
        if self.login.login():

            running = True
            self.preview.start_screen()
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                        # отображение
                self.display_surface.fill(GRAY)

                # компоненты

                self.game.run()
                self.score.run()

                # обновление экрана
                pygame.display.update()
                self.clock.tick()
            pygame.quit()
            exit()


if __name__ == '__main__':
    main = Main()
    main.run()
