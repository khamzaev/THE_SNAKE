from random import choice, randint
import pygame

# --- Константы ---
SCREEN_WIDTH = 640  # Ширина игрового окна
SCREEN_HEIGHT = 480  # Высота игрового окна
GRID_SIZE = 20  # Размер одной ячейки сетки
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE  # Количество ячеек по ширине
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE  # Количество ячеек по высоте

# --- Направления движения ---
UP = (0, -1)  # Вверх
DOWN = (0, 1)  # Вниз
LEFT = (-1, 0)  # Влево
RIGHT = (1, 0)  # Вправо

# --- Цвета ---
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Цвет фона - черный
BORDER_COLOR = (93, 216, 228)  # Цвет границы ячейки
APPLE_COLOR = (255, 0, 0)  # Цвет яблока
SNAKE_COLOR = (0, 255, 0)  # Цвет змейки

# --- Скорость ---
SPEED = 20  # Скорость змейки (кадры в секунду)

# --- Инициализация игрового окна ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Настройка окна
pygame.display.set_caption('Змейка')  # Название окна

# --- Часы для контроля времени ---
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех объектов на игровом поле."""

    def __init__(self, position):
        """Инициализация объекта с заданной позицией."""
        self.position = position

    def draw(self):
        """Метод для отрисовки объекта. Обязательно переопределить."""
        raise NotImplementedError("Необходимо переопределить метод draw()")


class Apple(GameObject):
    """Класс для создания и отображения яблока."""

    def __init__(self):
        """Инициализация яблока в случайной позиции."""
        random_position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )
        super().__init__(random_position)

    def draw(self):
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))  # Размеры яблока
        pygame.draw.rect(screen, APPLE_COLOR, rect)  # Рисуем яблоко
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)  # Рисуем его границу


class Snake(GameObject):
    """Класс для управления змейкой."""

    def __init__(self):
        """Инициализация змейки в центре игрового поля."""
        initial_position = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)
        super().__init__(initial_position)
        self.positions = [self.position]  # Массив сегментов змейки
        self.direction = choice([UP, DOWN, LEFT, RIGHT])  # Случайное начальное направление
        self.next_direction = None  # Новое направление (если изменится)
        self.last_segment = None  # Запоминаем последний сегмент

    def draw(self):
        """Отрисовка змейки на экране."""
        # Рисуем тело змейки (все сегменты кроме головы)
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, SNAKE_COLOR, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Рисуем голову змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, SNAKE_COLOR, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Убираем последний сегмент змейки, если он переместился
        if self.last_segment:
            last_rect = pygame.Rect(self.last_segment, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Движение змейки в заданном направлении."""
        head_x, head_y = self.positions[0]  # Текущая позиция головы
        delta_x, delta_y = self.direction  # Направление движения
        new_head = (
            (head_x + delta_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + delta_y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.last_segment = self.positions[-1]  # Сохраняем последний сегмент
        self.positions = [new_head] + self.positions[:-1]  # Обновляем позицию головы

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
            pygame.quit()  # Закрываем игру
            raise SystemExit

        elif event.type == pygame.KEYDOWN:
            # Изменяем направление змейки в зависимости от нажатой клавиши
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
    pygame.init()  # Инициализация pygame

    apple = Apple()  # Создаем яблоко
    snake = Snake()  # Создаем змейку

    while True:
        clock.tick(SPEED)  # Ограничение FPS
        handle_keys(snake)  # Обработка клавиш
        snake.update_direction()  # Обновление направления движения
        snake.move()  # Движение змейки

        # Проверка на поедание яблока
        if snake.positions[0] == apple.position:
            snake.positions.append(snake.last_segment)  # Увеличение змейки
            apple = Apple()  # Создание нового яблока

        # Очистка экрана
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Отрисовка объектов
        apple.draw()
        snake.draw()

        # Обновление экрана
        pygame.display.update()


if __name__ == '__main__':
    main()  # Запуск игры
