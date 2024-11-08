from tkinter import *
import time
import random

class Ball():
    def __init__(self, canvas, platform, color):
        self.canvas = canvas
        self.platform = platform
        self.oval = canvas.create_oval(200, 200, 215, 215, fill=color)
        self.dir = [-3, -2, -1, 1, 2, 3]
        self.x = random.choice(self.dir)
        self.y = -1
        self.touch_bottom = False
        self.bounce_count = 0

    def touch_platform(self, ball_pos):
        platform_pos = self.canvas.coords(self.platform.rect)
        if ball_pos[2] >= platform_pos[0] and ball_pos[0] <= platform_pos[2]:
            if ball_pos[3] >= platform_pos[1] and ball_pos[3] <= platform_pos[3]:
                return True
        return False

    def draw(self):
        self.canvas.move(self.oval, self.x, self.y)
        pos = self.canvas.coords(self.oval)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= 400:
            self.touch_bottom = True
        if self.touch_platform(pos):
            self.y = -3
            self.bounce_count += 1
            score_text.set(f"Score: {self.bounce_count}")
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= 500:
            self.x = -3

class Platform():
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(230, 300, 330, 310, fill=color)
        self.x = 0
        self.canvas.bind_all('<KeyPress-Left>', self.left)
        self.canvas.bind_all('<KeyPress-Right>', self.right)

    def left(self, event):
        # Проверка перед движением влево
        pos = self.canvas.coords(self.rect)
        if pos[0] > 0:
            self.x = -3

    def right(self, event):
        # Проверка перед движением вправо
        pos = self.canvas.coords(self.rect)
        if pos[2] < 500:
            self.x = 3

    def draw(self):
        self.canvas.move(self.rect, self.x, 0)
        pos = self.canvas.coords(self.rect)
        # Останавливаем платформу после движения
        if pos[0] <= 0 or pos[2] >= 500:
            self.x = 0




def start_game():
    global ball, platform, score_text, best_score
    canvas.delete("all")
    platform = Platform(canvas, 'green')
    ball = Ball(canvas, platform, 'red')
    score_text.set("Score: 0")
    ball.bounce_count = 0
    game_loop()

def game_loop():
    if not ball.touch_bottom:
        ball.draw()
        platform.draw()
        window.update()
        window.after(10, game_loop)
    else:
        global best_score
        if ball.bounce_count > best_score:
            best_score = ball.bounce_count
            best_score_text.set(f"Best Score: {best_score}")
        main_menu()

def main_menu():
    canvas.delete("all")
    canvas.create_text(250, 150, text="Аркада", font=("Arial", 24))
    play_button = Button(window, text="Играть", command=start_game)
    exit_button = Button(window, text="Выйти", command=window.destroy)
    canvas.create_window(250, 200, window=play_button)
    canvas.create_window(250, 250, window=exit_button)
    score_text.set("Score: 0")

window = Tk()
window.title("Аркада")
window.resizable(0, 0)
window.wm_attributes("-topmost", 1)

best_score = 0
score_text = StringVar()
best_score_text = StringVar(value="Best Score: 0")

canvas = Canvas(window, width=500, height=400)
canvas.pack()

score_label = Label(window, textvariable=score_text, font=("Arial", 12))
score_label.pack()
best_score_label = Label(window, textvariable=best_score_text, font=("Arial", 12))
best_score_label.pack()

main_menu()
window.mainloop()
