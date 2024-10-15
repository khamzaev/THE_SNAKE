from random import choice, randint
import pygame

# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20

CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2

screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption(f'Змейка | Скорость: {SPEED} | Управление: стрелки')

clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех объектов на игровом поле."""

    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        """Инициализация объекта с заданной позицией.

        Args:
            position (tuple): Координаты объекта на игровом поле.
        """
        self.position = position
        self.body_color = body_color

    def draw_cell(screen, color, border_color, position, size):
        """Отрисовывает клетку на экране.

        Args:
            screen (Surface): Экран, на котором рисуется объект.
            color (tuple): Цвет заливки объекта.
            border_color (tuple): Цвет границы объекта.
            position (tuple): Позиция клетки.
            size (tuple): Размер клетки.
        """
        rect = pygame.Rect(position, size)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, border_color, rect, 1)

    def draw(self):
        """Метод для отрисовки объекта.

        Raises:
            NotImplementedError: Если метод не переопределен в дочернем классе.
        """
        raise NotImplementedError("Необходимо переопределить метод draw()")


class Apple(GameObject):
    """Класс для создания и отображения яблока."""

    def __init__(self):
        """Инициализация яблока в случайной позиции."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Случайным образом задает позицию яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовка яблока на экране."""
        GameObject.draw_cell(
            screen, self.body_color, BORDER_COLOR,
            self.position, (GRID_SIZE, GRID_SIZE)
        )


class Snake(GameObject):
    """Класс для управления змейкой."""

    def __init__(self):
        """Инициализация змейки в центре игрового поля."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()  # Вызываем метод reset для инициализации

    def reset(self):
        """Сбрасывает состояние змейки к начальному."""
        self.position = (CENTER_X, CENTER_Y)
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last_segment = None

    def draw(self):
        """Отрисовка змейки на экране."""
        # Отрисовываем все сегменты змейки
        for position in self.positions[:-1]:
            GameObject.draw_cell(
                screen, self.body_color, BORDER_COLOR, position,
                (GRID_SIZE, GRID_SIZE)
            )

        # Отрисовываем голову змейки
        GameObject.draw_cell(
            screen, self.body_color, BORDER_COLOR,
            self.positions[0], (GRID_SIZE, GRID_SIZE)
        )

        # Убираем последний сегмент, если он был удален
        if self.last_segment:
            GameObject.draw_cell(
                screen, BOARD_BACKGROUND_COLOR, BOARD_BACKGROUND_COLOR,
                self.last_segment, (GRID_SIZE, GRID_SIZE)
            )

    def move(self):
        """Движение змейки в заданном направлении."""
        head_x, head_y = self.positions[0]
        delta_x, delta_y = self.direction
        new_head = (
            (head_x + delta_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + delta_y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.last_segment = self.positions[-1]
        self.positions = [new_head] + self.positions[:-1]

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

        elif event.type == pygame.KEYDOWN:
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

    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.positions[0] == apple.position:
            snake.positions.append(snake.last_segment)
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
