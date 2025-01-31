"""Змейка. Автор: Кирилл Терминасов."""
from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Константа для остановки игры
STOP_GAME = False

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Константный словарь с направлениями

DIRECTIONS = {
     (pygame.K_UP, LEFT): UP,
     (pygame.K_UP, RIGHT): UP,
     (pygame.K_DOWN, LEFT): DOWN,
     (pygame.K_DOWN, RIGHT): DOWN,
     (pygame.K_LEFT, UP): LEFT,
     (pygame.K_LEFT, DOWN): LEFT,
     (pygame.K_RIGHT, UP): RIGHT,
     (pygame.K_RIGHT, DOWN): RIGHT
}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self):
        """Инициализация класса.

        Атрибуты:
        position - позиция объекта на игровом поле;
        body_color - цвет объекта.
        """
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw_cell(self, position):
        """Метод класса для отрисовки одной ячейки объекта на экране."""
        rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Метод класса для отрисовки объекта на экране.

        Предназначен для переопределения в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс описывает яблоко и действия с ним."""

    def __init__(self):
        """Инициализация класса. Атрибуты наследуются от GameObject."""
        super().__init__()
        self.body_color = (255, 0, 0)
        self.randomize_position()

    def randomize_position(self):
        """Метод класса для получения случайных координат на игровом поле."""
        x = randint(0, (GRID_WIDTH) - 1) * 20
        y = randint(0, (GRID_HEIGHT) - 1) * 20
        self.position = (x, y)

    def draw(self):
        """Переопределение метода draw для отрисовки яблока."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс описывает змейку и её поведение."""

    def __init__(self, record=1, body_color=(0, 255, 0)):
        """Инициализация класса.

        Атрибуты:
        length - длина змейки;
        record_length - рекордная длина змейки;
        positions — список позиций всех сегментов тела змейки;
        direction — направление движения змейки;
        next_direction — следующее направление движения.
        """
        super().__init__()
        self.body_color = (0, 255, 0)
        self.length = 1
        self.record_length = record
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновление позиции змейки."""
        self.update_direction()

        curr_pos = self.get_head_position()
        new_x = (curr_pos[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_y = (curr_pos[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        new_pos = (new_x, new_y)

        self.positions = [new_pos] + self.positions
        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.pop()

    def draw(self):
        """Отрисовка змейки на экране с затиранием следа."""
        # Отрисовка головы змейки
        self.draw_cell(self.positions[0])

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возврат позиции шоловы змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс змейки после столкновения."""
        if self.length > self.record_length:
            self.record_length = self.length
            pygame.display.set_caption(f'Змейка. Рекорд: {self.record_length}')

        self.__init__(record=self.record_length)


def handle_keys(game_object, stop_game):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit

            game_object.next_direction = DIRECTIONS.get((event.key,
                                                        game_object.direction))


def main():
    """Основная функция программы."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    stop_game = False

    while not stop_game:
        clock.tick(SPEED)

        handle_keys(snake, stop_game)
        snake.move()
        curr_pos = snake.get_head_position()

        if curr_pos == apple.position:
            snake.length += 1
            apple.randomize_position()
        elif curr_pos in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position()

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
