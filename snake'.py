import PySimpleGUI as sg
from time import time
from random import randint


def place_dot():
    dot_pos = randint(0, CELL_NUM - 1), randint(0, CELL_NUM - 1)
    while dot_pos in snake_body:
        dot_pos = randint(0, CELL_NUM - 1), randint(0, CELL_NUM - 1)
    return dot_pos


def pos_to_pixel(cell):
    top_left_1 = cell[0] * CEll_SIZE, cell[1] * CEll_SIZE
    bottom_right_1 = top_left_1[0] + CEll_SIZE, top_left_1[1] + CEll_SIZE
    return top_left_1, bottom_right_1


sg.theme('DarkPurple')

# window/game settings
Field_size = 400
CELL_NUM = 10
CEll_SIZE = Field_size / CELL_NUM

# create snake
snake_body = [(4, 4), (3, 4), (2, 4)]
move_direction = {'left': (-1, 0), 'right': (1, 0), 'up': (0, 1), 'down': (0, -1)}
direction = move_direction['down']

# dot to eat
dot_pos = place_dot()
dot_eaten = False

field = sg.Graph(
    canvas_size=(Field_size, Field_size),
    graph_bottom_left=(0, 0),
    graph_top_right=(Field_size, Field_size),
    background_color='black'
)

layout = [[field]]

window = sg.Window('Snake_game', layout, return_keyboard_events=True)

start_time = time()

while True:
    event, values = window.read(timeout=10)
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Left:37': direction = move_direction['left']
    if event == 'Up:38': direction = move_direction['up']
    if event == 'Right:39': direction = move_direction['right']
    if event == 'Down:40': direction = move_direction['down']

    time_since_start = time() - start_time
    if time_since_start >= 0.5:
        start_time = time()

        # snake collide dot
        if snake_body[0] == dot_pos:
            dot_pos = place_dot()
            dot_eaten = True

        # snake_update
        new_head = (snake_body[0][0] + direction[0], snake_body[0][1] + direction[1])
        snake_body.insert(0, new_head)
        if not dot_eaten:
            snake_body.pop()
        dot_eaten = False

        # death
        if not 0 <= snake_body[0][0] <= CELL_NUM - 1 or \
                not 0 <= snake_body[0][1] <= CELL_NUM - 1 or \
                snake_body[0] in snake_body[1:]:
            print('Game is over')
            break

        field.DrawRectangle((0, 0), (Field_size, Field_size), 'black')

        top_left, bottom_right = pos_to_pixel(dot_pos)
        field.DrawRectangle(top_left, bottom_right, 'lightblue')

        # draw snake
        for index, i in enumerate(snake_body):
            top_left, bottom_right = pos_to_pixel(i)
            color = 'green' if index == 0 else 'red'
            field.DrawRectangle(top_left, bottom_right, color)

window.close()
