from random import choice, randint

import pygame

# Constants for field and grid size:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Movement directions:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Background colour - black:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Cell border colour
BORDER_COLOR = (93, 216, 228)

# Apple colour
APPLE_COLOR = (255, 0, 0)

# Snake colour
SNAKE_COLOR = (0, 255, 0)

# Snake speed:
SPEED = 20

# Game window setup:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Game window title:
pygame.display.set_caption('Змейка')

# Clock setup:
clock = pygame.time.Clock()


class GameObject:
    """Base class for game objects."""

    def __init__(self, position=None, body_color=None):
        if position is None:
            position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Base draw method (to be overridden by subclasses)."""

    def draw_cell(self, position):
        """Draw a single cell (shared by all game objects)."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Game apple."""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color=body_color)
        self.randomize_position()

    def randomize_position(self):
        """Place the apple at a random grid position."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Draw the apple."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Game snake."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color=body_color)
        self.reset()

    def reset(self):
        """Reset the snake to its initial state."""
        start_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.position = start_pos
        self.length = 1
        self.positions = [start_pos]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Return the coordinates of the snake head."""
        return self.positions[0]

    def update_direction(self):
        """Apply the direction chosen by the user."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Move the snake one cell forward."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        # Compute the new position, wrapping around the screen edges
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )

        self.positions.insert(0, new_head)
        self.position = new_head

        # If the length has not grown, remove the tail
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Draw all snake segments."""
        # Draw the body (without the head)
        for segment in self.positions[:-1]:
            self.draw_cell(segment)

        # Draw the head
        self.draw_cell(self.get_head_position())

        # Erase the tail trace
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Handle user key presses."""
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
    """Game entry point."""
    pygame.init()

    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Check for collision with itself
        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position()

        # Check whether the apple is eaten
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Make sure the apple does not appear inside the snake
            while apple.position in snake.positions:
                apple.randomize_position()

        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
