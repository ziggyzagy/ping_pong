from pygame import *


# базовый класс для спрайтов
class GameSprite(sprite.Sprite):
    """
    image_file - имя файла с картинкой для спрайта
    x - координата x спрайта
    y - координата y спрайта
    speed - скорость спрайта
    size_x - размер спрайта по горизонтали
    size_y - размер спрайта по вертикали
    """

    def __init__(self, image_file, x, y, speed, size_x, size_y):
        super().__init__()  # конструктор суперкласса
        self.image = transform.scale(
            image.load(image_file), (size_x, size_y)
        )  # создание внешнего вида спрайта - картинки
        self.speed = speed  # скорость
        self.rect = (
            self.image.get_rect()
        )  # прозрачная подложка спрайта - физическая модель
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        # отобразить картинку спрайта в тех же координатах, что и его физическая модель
        window.blit(self.image, (self.rect.x, self.rect.y))


# класс для игрока
class Player(GameSprite):
    # метод для управления игроком №2 (правая ракетка)
    def update_r(self):
        # получаем словарь состояний клавиш
        keys = key.get_pressed()

        # если нажата клавиша "стрелка вверх" и физическая модель не ушла за верхнюю границу игры
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed

        # если нажата клавиша "стрелка вниз" и физическая модель не ушла за нижнюю границу игры
        if keys[K_DOWN] and self.rect.y < height - 150:
            self.rect.y += self.speed

    # метод для управления игроком №1 (левая ракетка)
    def update_l(self):
        # получаем словарь состояний клавиш
        keys = key.get_pressed()

        # если нажата клавиша "W" и физическая модель не ушла за верхнюю границу игры
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed

        # если нажата клавиша "S" и физическая модель не ушла за нижнюю границу игры
        if keys[K_s] and self.rect.y < height - 150:
            self.rect.y += self.speed


""" 
Основная часть программы
Создание окна, задание параметров,
создание спрайтов
"""

# размеры окна
width = 600
height = 500

# создание окна
window = display.set_mode((width, height))
display.set_caption("Ping Pong")
back = (200, 255, 255)  # цвет заливки для фона
window.fill(back)  # заливка фона

# внутриигровые часы и ФПС
clock = time.Clock()
FPS = 60

# шрифт и надписи
font.init()
font1 = font.SysFont("Arial", 36)
lose1 = font1.render("PLAYER 1 LOSE!", True, (180, 0, 0))
lose2 = font1.render("PLAYER 2 LOSE!", True, (180, 0, 0))

""" Создание спрайтов """
# левая ракетка (Игрок №1)
racket1 = Player("racket.png", 30, 200, 4, 50, 150)
# правая ракетка (Игрок №2)
racket2 = Player("racket.png", 520, 200, 4, 50, 150)
# мяч
ball = GameSprite("tenis_ball.png", 200, 200, 4, 50, 50)

# скорости мячика по вертикали и горизонтали
ball_x = 3
ball_y = 3

# переменная окончания игры
finish = False  # когда True, то спрайты перестают работать
# переменная завершения программы
game = True  # завершается при нажатии кнопки закрыть окно


""" Игровой цикл"""

# игровой цикл (как программы)
while game:
    # обработка нажатия кнопки Закрыть окно
    for e in event.get():
        if e.type == QUIT:
            game = False  # завершение игрового цикла (как программы)

    # игровой цикл (как игры)
    if finish != True:
        window.fill(back)  # заливка фона
        racket1.update_l()  # обновление положения левой ракетки
        racket2.update_r()  # обновление положения правой ракетки

        # перемещение мячика
        ball.rect.x += ball_x
        ball.rect.y += ball_y

        # проверка на отскок от левой ракетки
        # если касаемся левой ракетки
        if sprite.collide_rect(racket1, ball):
            # разворачиваем мяч в противоположную сторону
            # по горизонтали (влево или вправо)
            ball_x *= -1

        # проверка на отскок от правой ракетки
        # если касаемся правой ракетки
        if sprite.collide_rect(racket2, ball):
            # разворачиваем мяч в противоположную сторону
            # по горизонтали (влево или вправо)
            ball_x *= -1

        # отскок от нижней или верхней границы
        # если касаемся нижней или верхней границы
        if ball.rect.y < 0 or ball.rect.y > height - 50:
            # разворачиваем мяч в противоположную сторону
            # по вертикали (вверх или вниз)
            ball_y *= -1

        # проигрыш левой ракетки, игрок 1
        # если касаемся левой границы
        if ball.rect.x < 0:
            finish = True  # завершаем игру
            window.blit(lose1, (200, 200))  # выводим надпись о проигрыше игрока №1

        # проигрыш правой ракетки, игрок 2
        if ball.rect.x > width - 50:
            finish = True  # завершаем игру
            window.blit(lose2, (200, 200))  # выводим надпись о проигрыше игрока №2

        # обновление картинок объектов
        racket1.reset()  # добавление игрока №1 на кадр
        racket2.reset()  # добавление игрока №2 на кадр
        ball.reset()  # добавление мячика на кадр

    # обновляем все содержимое на экране
    display.update()
    clock.tick(FPS)
