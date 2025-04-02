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
SPEED = 12

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""
    
    def __init__(self, position=None, body_color=None):
        """Инициализирует игровой объект.
        
        Args:
            position (tuple, optional): Начальная позиция объекта. По умолчанию None.
            body_color (tuple, optional): Цвет объекта в формате RGB. По умолчанию None.
        """
        self.position = position if position else (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color
    
    def draw(self):
        """Абстрактный метод для отрисовки объекта."""
        pass
    
    def draw_cell(self, position, color):
        """Отрисовывает одну ячейку объекта.
        
        Args:
            position (tuple): Координаты ячейки.
            color (tuple): Цвет ячейки в формате RGB.
        """
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс для представления яблока в игре."""
    
    def __init__(self):
        """Инициализирует яблоко со случайной позицией и красным цветом."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()
    
    def randomize_position(self, snake_positions=None):
        """Устанавливает случайную позицию для яблока, избегая позиций змейки.
        
        Args:
            snake_positions (list, optional): Список позиций змейки. По умолчанию None.
        """
        if snake_positions is None:
            snake_positions = []
        
        # Генерируем все возможные позиции
        all_positions = set(
            (x * GRID_SIZE, y * GRID_SIZE)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
        )
        
        # Исключаем позиции змейки
        free_positions = list(all_positions - set(snake_positions))
        
        if free_positions:
            self.position = choice(free_positions)
    
    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Класс для представления змейки в игре."""
    
    def __init__(self):
        """Инициализирует змейку с начальными параметрами."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()
    
    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        self.positions = [(center_x, center_y)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
    
    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
    
    def get_head_position(self):
        """Возвращает позицию головы змейки.
        
        Returns:
            tuple: Координаты головы змейки.
        """
        return self.positions[0]
    
    def move(self):
        """Перемещает змейку в текущем направлении."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        
        # Вычисляем новую позицию головы с учетом прохождения через границы
        new_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        
        # Проверяем столкновение с собой
        if (new_x, new_y) in self.positions[1:]:
            self.reset()
            return False
        
        # Добавляем новую голову
        self.positions.insert(0, (new_x, new_y))
        self.last = self.positions[-1]
        
        # Удаляем хвост только если длина не увеличивается
        if len(self.positions) > self.length:
            self.positions.pop()
        
        return True
    
    def draw(self):
        """Отрисовывает змейку на игровом поле."""
        # Отрисовываем все сегменты змейки
        for position in self.positions[1:]:
            self.draw_cell(position, self.body_color)
        
        # Отрисовываем голову
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        
        # Затираем последний сегмент, если он есть и если змейка не растет
        if self.last and len(self.positions) >= self.length:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой.
    
    Args:
        snake (Snake): Объект змейки, которой нужно управлять.
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
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit


def main():
    """Основная функция игры, содержащая главный игровой цикл."""
    # Инициализация PyGame:
    pygame.init()
    
    # Создание объектов игры
    snake = Snake()
    apple = Apple()
    
    # Переменная для хранения рекорда
    record = 1
    
    while True:
        clock.tick(SPEED)
        
        # Обработка ввода пользователя
        handle_keys(snake)
        
        # Обновление направления змейки
        snake.update_direction()
        
        # Перемещение змейки
        if not snake.move():
            continue
        
        # Проверка съедения яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1  # Увеличиваем длину змейки
            apple.randomize_position(snake.positions)
            
            # Обновление рекорда
            if snake.length > record:
                record = snake.length
                pygame.display.set_caption(f'Змейка (Рекорд: {record})')
        
        # Отрисовка игрового поля
        screen.fill(BOARD_BACKGROUND_COLOR)
        
        # Отрисовка объектов
        apple.draw()
        snake.draw()
        
        # Обновление экрана
        pygame.display.update()


if __name__ == '__main__':
    main()