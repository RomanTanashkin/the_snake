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


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=None, body_color=None):
        if position is None:
            position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Базовый метод отрисовки (для наследников)."""
        # Исправлено: удален лишний pass, так как есть docstring

    def draw_cell(self, position):
        """Метод для отрисовки одной ячейки (чтобы не дублировать код)."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Игровое яблоко."""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color=body_color)
        self.randomize_position()

    def randomize_position(self):
        """Случайно разместить яблоко на поле по сетке."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Отрисовка яблока."""
        # Исправлено: используем общий метод отрисовки ячейки
        self.draw_cell(self.position)


class Snake(GameObject):
    """Игровая змейка."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color=body_color)
        self.reset()

    def reset(self):
        """Вернуть змейку в начальное состояние."""
        start_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.position = start_pos
        self.length = 1
        self.positions = [start_pos]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Получить координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Применить направление, выбранное пользователем."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Сдвинуть змейку на одну клетку вперёд."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        # Вычисляем новую позицию с учетом заворачивания за край экрана
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )

        self.positions.insert(0, new_head)
        self.position = new_head

        # Если длина не увеличилась, удаляем хвост
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовать все сегменты змейки."""
        # Отрисовка тела (без головы)
        for segment in self.positions[:-1]:
            self.draw_cell(segment)

        # Отрисовка головы
        # Исправлено: используем метод get_head_position
        self.draw_cell(self.get_head_position())

        # Затирание следа хвоста
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обработка нажатий клавиш пользователем."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Точка входа в игру."""
    pygame.init()

    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка на столкновение с собой
        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position()

        # Проверка на поедание яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Исправлено: проверка, чтобы яблоко не появилось внутри змейки
            while apple.position in snake.positions:
                apple.randomize_position()

        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
