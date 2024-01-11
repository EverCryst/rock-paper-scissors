import pygame
import random
import os

speed = 5 # Скорость
amount = 16 # количество объектов 1 вида

collision = False # Если True то объеты разных типов отталкиваются друг от друга (могут быть баги)
stop = True # True - в случае если остались объекты одного вида ставит игру на "ПАУЗУ" || False - в случае если остались объекты одного вида закрывает окно и выводит в консоль "ПОБЕДИТЕЛЯ"

pygame.init()
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rock Paper Scissors by @EverCryst")
white = (100, 100, 100)

# Путь к изображениям
image_folder = "images/"

rock_image = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, 'rock.png')), (50, 50))
scissors_image = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, 'scissors.png')), (50, 50))
paper_image = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, 'paper.png')), (50, 50))

objects = []
for _ in range(amount):
    objects.append({
        'image': rock_image,
        'x': random.randint(10, screen_width - 50),
        'y': random.randint(10, screen_height - 50),
        'speed_x': random.choice([-speed, speed]),
        'speed_y': random.choice([-speed, speed])
    })
    objects.append({
        'image': scissors_image,
        'x': random.randint(10, screen_width - 50),
        'y': random.randint(10, screen_height - 50),
        'speed_x': random.choice([-speed, speed]),
        'speed_y': random.choice([-speed, speed])
    })
    objects.append({
        'image': paper_image,
        'x': random.randint(10, screen_width - 50),
        'y': random.randint(10, screen_height - 50),
        'speed_x': random.choice([-speed, speed]),
        'speed_y': random.choice([-speed, speed])
    })


def check_winner(objects):
    rock_count = 0
    scissors_count = 0
    paper_count = 0
    for obj in objects:
        if obj['image'] == rock_image:
            rock_count += 1
        elif obj['image'] == scissors_image:
            scissors_count += 1
        elif obj['image'] == paper_image:
            paper_count += 1
    if rock_count > 0 and scissors_count == 0 and paper_count == 0:
        return "Rock wins!"
    elif scissors_count > 0 and rock_count == 0 and paper_count == 0:
        return "Scissors wins!"
    elif paper_count > 0 and rock_count == 0 and scissors_count == 0:
        return "Paper wins!"
    return None


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Движение объектов и отталкивание от столкновений c границами экрана
    for obj in objects:
        obj['x'] += obj['speed_x']
        obj['y'] += obj['speed_y']
        if obj['x'] <= 0 or obj['x'] + obj['image'].get_width() >= screen_width:
            obj['speed_x'] = -obj['speed_x']
        if obj['y'] <= 0 or obj['y'] + obj['image'].get_height() >= screen_height:
            obj['speed_y'] = -obj['speed_y']

    # Отталкивание от объкта другого типа
    if collision: 
        for i, obj in enumerate(objects):
            for other_obj in objects[i + 1:]:
                if obj['image'] != other_obj['image']:
                    if obj['x'] < other_obj['x'] + 50 and obj['x'] + 50 > other_obj['x'] and obj['y'] < other_obj['y'] + 50 and obj['y'] + 50 > other_obj['y']:
                        obj['speed_x'] = -obj['speed_x']
                        obj['speed_y'] = -obj['speed_y']
                        other_obj['speed_x'] = -other_obj['speed_x']
                        other_obj['speed_y'] = -other_obj['speed_y']

    # Смена типа при столкновении 
    for obj1 in objects:
        for obj2 in objects:
            if obj1 != obj2 and abs(obj1['x'] - obj2['x']) < 50 and abs(obj1['y'] - obj2['y']) < 50:
                if obj1['image'] == rock_image and obj2['image'] == paper_image:
                    obj1['image'] = paper_image
                elif obj1['image'] == scissors_image and obj2['image'] == rock_image:
                    obj1['image'] = rock_image
                elif obj1['image'] == paper_image and obj2['image'] == scissors_image:
                    obj1['image'] = scissors_image

    screen.fill(white)
    for obj in objects:
        screen.blit(obj['image'], (obj['x'],obj['y']))
    pygame.display.update()
    pygame.time.Clock().tick(25)
    winner = check_winner(objects)
    if winner:
        if stop:
            for obj in objects:
                obj['speed_x'] = 0
                obj['speed_y'] = 0
        else:
            running = False


pygame.quit()
