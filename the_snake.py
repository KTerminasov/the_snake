"""Змейка. Автор: Кирилл Терминасов"""
from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты.
    Содержит общие атрибуты игровых объектов.
    """
        
    def __init__(self):
        """Инициализация класса. Атрибуты:
        position - позиция объекта на игровом поле
        body_color - цвет объекта.
        """
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Метод класса для отрисовки объекта на экране.
        Предназначен для переопределения в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс описывает яблоко и действия с ним."""

    def __init__(self):
        """Инициализация класса.

        Атрибуты (наследуются от GameObject):
        position - задается случайным образом.
        color - Красный (255, 0, 0)
        """
        super().__init__()
        self.position = self.randomize_position()
        self.body_color = (255, 0, 0)

    @staticmethod
    def randomize_position():
        """Метод класса для получения случайных координат на игровом поле."""
        return ((randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)))

    def draw(self):
        """Переопределение метода draw для отрисовки яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс описывает змейку и её поведение."""

    def __init__(self, body_color=(0, 255, 0)):
        """Инициализация класса.

        Атрибуты:
        position (наследуется от GameObject) - позиция головы змейки на экране
        body_color (наследуется от GameObject) - цвет змейки
        length - длина змейки
        positions — список позиций всех сегментов тела змейки
        direction — направление движения змейки
        next_direction — следующее направление движения
        """
        super().__init__()
        self.body_color = (0, 255, 0)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = self.position

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновление позиции змейки."""
        curr_pos = self.get_head_position()
        new_pos = (curr_pos[0]+self.direction[0],
                   curr_pos[1]+self.direction[1])

        self.positions = [new_pos] + self.positions
        self.positions.pop()

    def draw(self):
        """Отрисовка змейки на экране с затиранием следа."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возврат позиции шоловы змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс змейки после столкновения."""
        self.length = 1
        self.positions = [self.position]


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция программы."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    
    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.move()
        curr_pos = snake.get_head_position()

        if curr_pos == apple.position:
            snake.length += 1
            apple.ramdomize_position()
        elif curr_pos in snake.positions[1:]:
            snake.reset()
        
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
