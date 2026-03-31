import tkinter as tk


WIDTH = 600
HEIGHT = 450

def make_enemy_sprite():
    pattern = [
        "00100000100",
        "00010001000",
        "00111111100",
        "01101110110",
        "11111111111",
        "10111111101",
        "10100000101",
        "00011011000",
    ]
    h = len(pattern)
    w = len(pattern[0])

    img = tk.PhotoImage(width=w, height=h)

    for y in range(h):
        for x in range(w):
            if pattern[y][x] == "1":
                img.put("#0f0", (x, y))
    
    return img


def make_player_sprite():
    h = 16
    w = 24
    img = tk.PhotoImage(width=w, height=h)
    for y in range(h):
        for x in range(w):
            if (y == 0 and 4 <= x <= 19):
                img.put("#0f0", (x, y))
    
    return img

root = tk.Tk()
root.title("Space Invaders")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

player_img = make_player_sprite()
enemy_img = make_enemy_sprite()

player = canvas.create_image(WIDTH//2, HEIGHT-30, image=player_img, anchor=tk.CENTER)
enemy = canvas.create_image(WIDTH//2, 30, image=enemy_img, anchor=tk.CENTER)

ROWS = 4
CELLS = 8
CELL = 32

enemies = []

def create_enemy_formation():
    enemies.clear()
    start_x = 100
    start_y = 60
    for r in range(ROWS):
        for c in range(CELLS):
            x = start_x + c * CELL
            y = start_y + r * CELL

            e = canvas.create_image(x, y, image=enemy_img, anchor="nw")

            enemies.append(e)

def move_left(event):
    canvas.move(player, -15, 0)
def move_right(event):
    canvas.move(player, 15, 0)
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)

lasers = []

def make_laser_sprite():
    img = tk.PhotoImage(width=2, height=10)
    for y in range(10):
        for x in range(2):
            img.put("yellow", (x, y))
    return img

laser_img = make_laser_sprite()

def shoot(event):
        
    lasers.append(canvas.create_image(canvas.coords(player), image=laser_img, anchor=tk.CENTER))
root.bind("<space>", shoot)

def collision(a, l):
    ax1, ay1, ax2, ay2 = canvas.bbox(a)
    lx1, ly1, lx2, ly2 = canvas.bbox(l)
    return ax1 < lx2 and ax2 > lx1 and ay1 < ly2 and ay2 > ly1

enemy_dx = 4

def move_enemies():
    global enemy_dx

    hit_wall = False
    for e in enemies:
        x1, y1, x2, y2 = canvas.bbox(e)

        if x2 >= WIDTH-10 and enemy_dx > 0:
            hit_wall = True
        if x1 <= 10 and enemy_dx < 0:
            hit_wall = True

    if hit_wall:
        enemy_dx = -enemy_dx
        for e in enemies:
            canvas.move(e, 0, 10)

    else:
        for e in enemies:
            canvas.move(e, enemy_dx, 0)
alive = True

def game_loop():
    global alive

    if not alive:
        canvas.delete("all")
        canvas.create_text(WIDTH//2, HEIGHT//2, text="Game Over", fill = "red", font=("Arial", 24))
        return
    move_enemies()

    for l in lasers[:]:
        canvas.move(l, 0, -12)
        x1, y1, x2, y2 = canvas.bbox(l)
        if y2 < 0:
            canvas.delete(l)
            lasers.remove(l)

    for l in lasers[:]:
        for e in enemies[:]:
            if collision(e, l):
                canvas.delete(e)
                canvas.delete(l)
                if l in lasers:
                    lasers.remove(l)
                if e in enemies:
                    enemies.remove(e)
                break

    
    root.after(40, game_loop)

def start():
    global player
    player = canvas.create_image(WIDTH//2, HEIGHT-30, image=player_img, anchor=tk.CENTER)
    game_loop()

def reset():
    global alive, enemy_dx
    canvas.delete("all")
    lasers.clear()
    enemies.clear()

    alive = True
    enemy_dx = 4

    create_enemy_formation()
    start()

root.bind("r", reset)

reset()
root.mainloop()
