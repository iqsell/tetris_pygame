from settings import *
from game import *
from Register import LoginWindow
from score import Score
class Records:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION))
        self.rect = self.surface.get_rect(topright=(WINDOW_WIDTH - PADDING, PADDING))
        self.best_results = {}
        self.game = Game.check_game_over()
        self.login = LoginWindow()
        self.score = Score()

    def update_best_results(self, player_name, score):
        if player_name in self.best_results:
            if score > self.best_results[player_name]:
                self.best_results[player_name] = score
        else:
            self.best_results[player_name] = score

    def save_best_results(self):
        pass
    # Добавить код для сохранения лучших результатов в файл или базу данных
    # Например, сохранить self.best_results в текстовый файл или в формате JSON

    def run(self, next_shapes):
        self.surface.fill(GRAY)
        self.display_pieces(next_shapes)
        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)
        if self.game:
            self.update_best_results(self.login.username, self.score.score)
