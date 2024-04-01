import tkinter
from random import randint

SIDE = 700
SNAKE_SIZE = 50

class Snake:
    def __init__(self, window, canvas):
        self.window = window
        self.canvas = canvas
        self.body = [
            canvas.create_rectangle(
            SIDE//2 - SNAKE_SIZE, SIDE//2 - SNAKE_SIZE,
            SIDE//2, SIDE//2,
            fill = '#00FF00')
        ]
        self.direction = 'space'    # pause
        self.direction_x = 0    # направление движения по x
        self.direction_y = 0    # направление движения по y


    def move(self, food):
        '''Научим змейку двигаться'''
        global score
        if self.direction != 'space':
            for i in range(len(self.body)-1, 0, -1):  # начиная с хвоста (с конца) переносим каждую часть змейки на часть предыдущего хвоста
                prev_x, prev_y, _, _ = self.canvas.coords(self.body[i - 1])  # возьмем координаты предыдущей части
                curr_x, curr_y, _, _ = self.canvas.coords(self.body[i])  # возьмем координаты текущей части
                self.canvas.move(self.body[i], prev_x - curr_x, prev_y - curr_y)  # двигаем зеленый квадратик (body[i]) из curr на позицию prev на дельту координат
            self.canvas.move(self.body[0], self.direction_x, self.direction_y)   # Двигаем голову змейки (нулевой квадрат) по координатам
        self.fix_overflow()  # проверка не ушли ли за границу окна
        if self.collide_food(food):  # проверка совпадения координат головы и еды
            score += 1
            print(f'Score {score}')
            self.grow()  # add body part
            label.config(text=f'Score = {score}')   # score update
            food.recreate()  # recreate food
        elif self.collide_itself():
            game_over()
            return
        self.window.after(200, self.move, food)   # автоматическое движение змейки


    def collide_itself(self):
        '''Проверка на столкновение с собой'''
        head_x, head_y, _, _ = self.canvas.coords(self.body[0])
        for i in range(1, len(self.body)):
            x0, y0, _, _ = self.canvas.coords(self.body[i])
            if head_x == x0 and head_y == y0:
                return True
        return False


    def fix_overflow(self):
        '''Проверка не ушла ли змейка за пределы окна'''
        for part in self.body:  # проверяем для каждого элемента змейки
            x0, y0, x1, y1 = self.canvas.coords(part)
            if self.direction == 'Up' and y0 < 0:   # если змейка каснулась верхней границы экрана
                self.canvas.move(part, 0, SIDE)
            elif self.direction == 'Down' and y1 > SIDE:   # если змейка каснулась нижней границы экрана
                self.canvas.move(part, 0, -SIDE)
            elif self.direction == 'Left' and x0 < 0:   # если змейка каснулась левой границы экрана
                self.canvas.move(part, SIDE, 0)
            elif self.direction == 'Right' and x1 > SIDE:   # если змейка каснулась правой границы экрана
                self.canvas.move(part, -SIDE, 0)


    def turn(self, event):
        '''Определим направление движения змейки'''
        if len(self.body) == 1:
            if event.keysym == 'Up' and self.direction != 'Down':
                self.direction_x = 0
                self.direction_y = -SNAKE_SIZE
                self.direction = event.keysym  # запоминает какое сейчас направление (это нужно для функции fix_overflow)
            elif event.keysym == 'Down' and self.direction != 'Up':
                self.direction_x = 0
                self.direction_y = SNAKE_SIZE
                self.direction = event.keysym  # запоминает какое сейчас направление (это нужно для функции fix_overflow)
            elif event.keysym == 'Left' and self.direction != 'Right':
                self.direction_x = -SNAKE_SIZE
                self.direction_y = 0
                self.direction = event.keysym  # запоминает какое сейчас направление (это нужно для функции fix_overflow)
            elif event.keysym == 'Right' and self.direction != 'Left':
                self.direction_x = SNAKE_SIZE
                self.direction_y = 0
                self.direction = event.keysym  # запоминает какое сейчас направление (это нужно для функции fix_overflow)
            elif event.keysym == 'space':
                self.direction_x = 0
                self.direction_y = 0
                self.direction = event.keysym  # запоминает что направления нет (это нужно для паузы)
        else:
            head_x, head_y, _, _ = self.canvas.coords(self.body[0])
            body_x, body_y, _, _ = self.canvas.coords(self.body[1])
            if event.keysym == 'Up' and self.direction != 'Down':
                if self.direction == 'space':
                    if head_y - body_y == 50 and head_x - body_x == 0:
                        self.direction_x = 0
                        self.direction_y = 0
                        self.direction = 'space'
                self.direction_x = 0
                self.direction_y = -SNAKE_SIZE
                self.direction = event.keysym  # запоминает какое сейчас направление (это нужно для функции fix_overflow)
            elif event.keysym == 'Down' and self.direction != 'Up':
                if self.direction == 'space':
                    if body_y - head_y == 50 and head_x - body_x == 0:
                        self.direction_x = 0
                        self.direction_y = 0
                        self.direction = 'space'
                self.direction_x = 0
                self.direction_y = SNAKE_SIZE
                self.direction = event.keysym  # запоминает какое сейчас направление (это нужно для функции fix_overflow)
            elif event.keysym == 'Left' and self.direction != 'Right':
                if self.direction == 'space':
                    if head_y - body_y == 0 and head_x - body_x == 50:
                        self.direction_x = 0
                        self.direction_y = 0
                        self.direction = 'space'
                self.direction_x = -SNAKE_SIZE
                self.direction_y = 0
                self.direction = event.keysym  # запоминает какое сейчас направление (это нужно для функции fix_overflow)
            elif event.keysym == 'Right' and self.direction != 'Left':
                if self.direction == 'space':
                    if head_y - body_y == 0 and body_x - head_x == 50:
                        self.direction_x = 0
                        self.direction_y = 0
                        self.direction = 'space'
                self.direction_x = SNAKE_SIZE
                self.direction_y = 0
                self.direction = event.keysym  # запоминает какое сейчас направление (это нужно для функции fix_overflow)
            elif event.keysym == 'space':
                self.direction_x = 0
                self.direction_y = 0
                self.direction = event.keysym  # запоминает что направления нет (это нужно для паузы)


    def collide_food(self, food):
        '''Проверка совпадает ли голова змейки с едой'''
        head_x, head_y, _, _ = self.canvas.coords(self.body[0])  # нужно плучить координаты головы
        food_x, food_y, _, _ = self.canvas.coords(food.circle)  # нужно плучить координаты еды
        if head_x == food_x and head_y == food_y:
            return True
        return False


    def grow(self):
        '''Змейка растет'''
        x0, y0, x1, y1 = self.canvas.coords(self.body[-1])  # берем координаты головы
        new_part = self.canvas.create_rectangle(
            (x0 + self.direction_x, y0 + self.direction_y),
            (x1 + self.direction_x, y1 + self.direction_y),
            fill = '#00FF00')   # создаем еще один квадрат (хвост)
        self.body.append(new_part)  # добавляем хвост


class Food:
    def __init__(self, canvas):
        self.canvas = canvas
        self.circle = None
        self.create()   # Рисуем кружок (еду)


    def create(self):
        '''Создаем кружок (еду)'''
        number_of_cols = SIDE // SNAKE_SIZE  # 700 x 700 (side x side), 50 snake_size
        x = randint(0, number_of_cols - 1) * SNAKE_SIZE  # Случайная координата по x
        y = randint(0, number_of_cols - 1) * SNAKE_SIZE  # Случайная координата по y
        self.circle = self.canvas.create_oval(
            x, y, x + SNAKE_SIZE, y + SNAKE_SIZE,
            fill='red',
            tag='food')

    def recreate(self):
        '''Пересоздаем еду'''
        self.canvas.delete('food')
        self.create()


def game_over():
    '''Завершение игры'''
    canvas.delete(tkinter.ALL)
    canvas.create_text(
        canvas.winfo_width() // 2,
        canvas.winfo_height() // 2,
        font=('consolas', 50),
        text='GAME OVER',
        fill='red')
    snake.direction = 'space'


score = 0
window = tkinter.Tk()  # создаем корневой объект - окно
canvas = tkinter.Canvas(window, bg='black', height=SIDE, width=SIDE)  # создаем размеры и цвет окна
label = tkinter.Label(text=f'Score = {score}', font = ('consolas', 50))  # создаем текстовую метку
# snake
snake = Snake(window, canvas)  # создаем змейку (экземпляр 'snake' класса 'Snake')
# food
food = Food(canvas)   # зоздаем объект food класса Food
label.pack()  # размещаем метку в окне
canvas.pack()   # размещаем canvas
window.bind('<KeyPress>', snake.turn)   # Змейка начнет двигаться при нажатии кнопки (bind передает event 'какую кнопку нажали')
snake.move(food)    # Змейка начнет двигаться (параметр food нужен для проверки collide_food)
window.mainloop()
