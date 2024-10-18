from random import choice, randint

import pygame

# Константы для игрового поля
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Константы для центра экрана
CENTER_POSITION = (
    (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE,
    (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE
)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость игры
SPEED = 20

# Настройки экрана
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)

# Параметры по умолчанию
DEFAULT_POSITION = (0, 0)
DEFAULT_BODY_COLOR = (0, 0, 0)

# Часы для контроля FPS
clock = pygame.time.Clock()
score = 0
current_speed = SPEED
controls_info = "Управление: Стрелки (↑ ↓ ← →)"


class GameObject:
    """Базовый класс для всех объектов на игровом поле."""

    def __init__(
            self, position=DEFAULT_POSITION,
            body_color=DEFAULT_BODY_COLOR
    ):
        """Инициализация объекта с заданной позицией.

        Args:
            position (tuple): Координаты объекта на игровом поле.
        """
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position, size):
        """Отрисовка клетки на экране.

        Args:
            position (tuple): Позиция клетки на экране.
            size (int): Размер клетки.
        """
        rect = pygame.Rect(position, (size, size))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Метод для отрисовки объекта.

        Raises:
            NotImplementedError: Если метод не переопределен в дочернем классе.
        """
        raise NotImplementedError("Необходимо переопределить метод draw()")


class Apple(GameObject):
    """Класс для создания и отображения яблока."""

    def __init__(self, occupied_positions):
        """Инициализация яблока в случайной позиции."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Случайным образом задает позицию яблока"""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            # Проверяем, не занята ли эта позиция
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовка яблока на экране."""
        self.draw_cell(self.position, GRID_SIZE)


class Snake(GameObject):
    """Класс для управления змейкой."""

    def __init__(self):
        """Инициализация змейки в центре игрового поля."""
        super().__init__(body_color=SNAKE_COLOR)
        # Инициализация атрибутов
        self.positions = []
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last_segment = None

        self.reset()

    def reset(self):
        """Сбрасывает состояние змейки к начальному."""
        self.position = CENTER_POSITION
        self.positions = [self.position]

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def draw(self):
        """Отрисовка змейки на экране."""
        # Отрисовка головы змейки с использованием метода
        # get_head_position()
        self.draw_cell(self.get_head_position(), GRID_SIZE)
        for position in self.positions[1:]:
            self.draw_cell(position, GRID_SIZE)

    def move(self):
        """Движение змейки в заданном направлении."""
        head_x, head_y = self.get_head_position()
        delta_x, delta_y = self.direction
        new_head = (
            (head_x + delta_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + delta_y * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.last_segment = self.positions[-1]
        self.positions.insert(0, new_head)
        self.positions.pop()

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(snake):
    """Обработка нажатий клавиш для управления змейкой.

    Args:
        snake (Snake): Экземпляр класса змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Главная функция игры. Управляет основным игровым циклом."""
    pygame.init()

    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка на столкновение с яблоком
        if snake.get_head_position() == apple.position:
            snake.positions.append(snake.last_segment)
            apple.randomize_position(snake.positions)

        # Проверка на самокус
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        pygame.display.set_caption(
            f'Змейка | Скорость:'
            f' {current_speed} | Счет: {score} | {controls_info}'
        )

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
