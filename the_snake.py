from random import choice, randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position, body_color):
        """Инициализирует объект с позицией и цветом.

        Args:
            position (tuple): Позиция объекта на игровом поле (x, y).
            body_color (tuple): Цвет объекта в формате RGB.
        """
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Метод для отрисовки объектов, который переопределяется в подклассах."""
        raise NotImplementedError("Этот метод должен быть реализован в подклассе.")


class Apple(GameObject):
    """Класс, представляющий яблоко."""

    def __init__(self, grid_size=20, screen_width=640, screen_height=480, color=APPLE_COLOR):
        """Инициализация яблока.

        Args:
            grid_size (int): Размер одной ячейки.
            screen_width (int): Ширина экрана.
            screen_height (int): Высота экрана.
            color (tuple): Цвет яблока в формате RGB.
        """
        self.grid_size = grid_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        position = self.random_position()
        super().__init__(position, color)

    def random_position(self):
        """Генерация случайной позиции для яблока."""
        x = randint(0, (self.screen_width // self.grid_size) - 1) * self.grid_size
        y = randint(0, (self.screen_height // self.grid_size) - 1) * self.grid_size
        return (x, y)

    def draw(self, surface):
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(self.position, (self.grid_size, self.grid_size))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку."""

    def __init__(self, grid_size=20, screen_width=640, screen_height=480, color=SNAKE_COLOR):
        """Инициализация змейки.

        Args:
            grid_size (int): Размер одной ячейки.
            screen_width (int): Ширина экрана.
            screen_height (int): Высота экрана.
            color (tuple): Цвет змейки в формате RGB.
        """
        self.grid_size = grid_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.positions = [(screen_width // 2, screen_height // 2)]  # Начальная позиция
        self.direction = RIGHT
        self.next_direction = None
        super().__init__(self.positions[0], color)

    def update_direction(self, direction):
        """Обновляет направление движения змейки."""
        if (self.direction[0] * -1, self.direction[1] * -1) != direction:
            self.next_direction = direction

    def move(self):
        """Перемещает змейку в новом направлении."""
        if self.next_direction:
            self.direction = self.next_direction
        head_x, head_y = self.positions[0]
        new_head = ((head_x + self.direction[0] * self.grid_size) % self.screen_width,
                    (head_y + self.direction[1] * self.grid_size) % self.screen_height)
        self.positions = [new_head] + self.positions[:-1]

    def grow(self):
        """Увеличивает длину змейки."""
        self.positions.append(self.positions[-1])

    def draw(self, surface):
        """Отрисовка змейки."""
        for segment in self.positions:
            rect = pygame.Rect(segment, (self.grid_size, self.grid_size))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


def main():
    """Основной игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.update_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.update_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.update_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.update_direction(RIGHT)

        snake.move()

        # Проверка столкновения с яблоком
        if snake.positions[0] == apple.position:
            snake.grow()
            apple.position = apple.random_position()

        screen.fill(BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()

        clock.tick(SPEED)

    pygame.quit()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None