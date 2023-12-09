import random
import time
import pygame, sys, os
from button import Button
import sqlite3
import datetime
import pytz

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("터치 반응 게임")

# 미디어 파일 접속 경로
db_path = os.path.join('score_record.db')
assets_background = os.path.join('assets/background.jpg')
assets_select2 = os.path.join('assets/select2.png')
assets_quit_rect = os.path.join('assets/Quit Rect.png')
assets_peace_pic = os.path.join('assets/peace_pic.jpg')
assets_space = os.path.join('assets/space.png')
assets_ship = os.path.join('assets/ship.png')
assets_bang = os.path.join('assets/bang.png')
assets_quit_button = os.path.join('assets/Quit_Button.png')
# 사운드 파일
sound_game_ready = pygame.mixer.Sound(os.path.join('sounds/game_ready.mp3'))
sound_game_start = pygame.mixer.Sound(os.path.join('sounds/game_start.mp3'))
sound_main_touch = pygame.mixer.Sound(os.path.join('sounds/main_touch.mp3'))
sound_game_touch = pygame.mixer.Sound(os.path.join('sounds/game_touch.mp3'))
sound_react_end = pygame.mixer.Sound(os.path.join('sounds/react_end.mp3'))
sound_remem_correct = pygame.mixer.Sound(os.path.join('sounds/remem_correct.mp3'))
sound_remem_incorrect = pygame.mixer.Sound(os.path.join('sounds/remem_incorrect.mp3'))
sound_remem_end = pygame.mixer.Sound(os.path.join('sounds/remem_end.mp3'))
sound_space_bang = pygame.mixer.Sound(os.path.join('sounds/space_bang.mp3'))
sound_space_start = pygame.mixer.Sound(os.path.join('sounds/space_start.mp3'))
sound_space_end = pygame.mixer.Sound(os.path.join('sounds/space_end.mp3'))
sound_space_bg = pygame.mixer.Sound(os.path.join('sounds/space_bg.mp3'))

con = sqlite3.connect(db_path)
cur = con.cursor()

kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S")

DISPLAY_WIDTH = 1920
DISPLAY_HEIGHT = 1080
SCREEN = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
SCREEN = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
font_style = "malgungothic"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (105, 52, 52)
LIME = (0,255,0) 
BLUE = (0,0,255)
RED = (255, 0, 0)

# 일반적인 폰트
def get_font(size): 
    return pygame.font.SysFont(font_style, size)

# 굵은 폰트
def get_bold_font(size): 
    font = pygame.font.SysFont(font_style, size)
    bold_font = font.set_bold(True) # 굵은 글꼴로 설정
    return font.set_bold(True)

def reaction_game():
    # 게임 상수 설정
    GRID_SIZE = 8
    GRID_WIDTH, GRID_HEIGHT = DISPLAY_WIDTH // GRID_SIZE, DISPLAY_HEIGHT // GRID_SIZE
    MAX_TRIES = 30
    LEVEL = 1

    # 게임 루프
    success_count = 0
    total_time = 0
    running = True
    try_count = 0

    def react_first_menu():
        pygame.event.clear()
        run = True
        while run:
            SCREEN.fill(WHITE)
            QUIT_BUTTON = Button(image=pygame.image.load(assets_quit_button), pos=(DISPLAY_WIDTH - 200, 150), 
                            text_input="Quit", font=get_font(40), base_color="#FF0000", hovering_color="White")
            text = get_font(100).render("화면에 나타나는 사각형을", True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2 - 200)
            SCREEN.blit(text, textRect)
            text = get_font(100).render("빠르게 누르세요!", True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2 - 30)
            SCREEN.blit(text, textRect)
            text = get_font(80).render("화면을 눌러 시작하세요!", True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2 + 200)
            SCREEN.blit(text, textRect)
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            for button in [QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main_menu()
                # 게임시작 키 입력, ESC = 나가기
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        main_menu()
                if event.type == pygame.MOUSEBUTTONUP:
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        sound_main_touch.play()
                        main_menu()
                    do_react_game()

            pygame.display.update()

    def do_react_game():
        pygame.event.clear()
        nonlocal running, try_count, success_count, total_time
        RANDOM_COLOR = (random.randint(0, 255), random.randint(0, 255), 255)
        BG = pygame.image.load(assets_peace_pic)
        SCREEN.blit(BG, (0, 0))
        pygame.display.update()

        # 시작 전 카운트다운
        for i in range(4, 0, -1):
            SCREEN.blit(BG, (0, 0))
            # 마지막에 Start 출력
            if i == 1:
                sound_game_start.play()
                count_image = get_font(200).render("Start!", True, (0, 0, 255))
                SCREEN.blit(count_image, (DISPLAY_WIDTH / 2 - 300, DISPLAY_HEIGHT / 2 - 120))
            # 3, 2, 1 
            else:
                sound_game_ready.play()
                count_image = get_font(200).render(str(i-1), True, (0, 0, 0))
                SCREEN.blit(count_image, (DISPLAY_WIDTH / 2 - 100, DISPLAY_HEIGHT / 2 - 120))
            pygame.display.update()
            pygame.time.delay(1000)
            pygame.event.clear()
        
        while running and try_count < MAX_TRIES:
            clock.tick(60)  # 초당 60 프레임으로 제한
            
            # 랜덤 블록 위치 계산
            block_x = (random.randint(1, GRID_SIZE - 2) * GRID_WIDTH) + (GRID_WIDTH / 2)
            block_y = random.randint(1, GRID_SIZE - 2) * GRID_HEIGHT

            # 블록 그리기
            SCREEN.blit(BG, (0, 0))
            pygame.draw.rect(SCREEN, RANDOM_COLOR, (block_x, block_y, GRID_WIDTH, GRID_HEIGHT))

            start_time = time.time()
            tries_text = get_font(30).render(f"{try_count} / {MAX_TRIES}", True, (0,0,0))
            SCREEN.blit(tries_text, (DISPLAY_WIDTH - 150, 10))
            pygame.display.update()

            clicked = False

            # 이벤트 처리
            while not clicked and (time.time() - start_time) < 2 - (LEVEL - 1) * 0.2:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        react_first_menu()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            react_first_menu()
                    if event.type == pygame.MOUSEBUTTONUP:
                        x, y = pygame.mouse.get_pos()
                        if block_x <= x <= block_x + GRID_WIDTH and block_y <= y <= block_y + GRID_HEIGHT:
                            sound_game_touch.play()
                            clicked = True
                            success_count += 1
                            print("Click ", x, y, "Grid coordinates:", block_x, block_y)

            try_count += 1
            total_time += time.time() - start_time
        react_result()
    
    # 결과 화면 출력
    def react_result():
        pygame.event.clear()
        sound_react_end.play()
        run = True
        score = round(total_time / MAX_TRIES, 5)
        success_text = get_font(75).render(f"올바르게 반응한 횟수: {success_count} / {MAX_TRIES}", True, (0, 0, 0))
        avg_time_text = get_font(75).render(f"평균 반응 시간: {score}초", True, (0, 0, 0))
        quit_text = get_font(50).render("화면을 눌러 종료하세요", True, (0, 0, 0))
        record_text = get_font(50).render("Record", True, (0, 0, 0))
        player_name = "gdb"
        now_kst = datetime.datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("INSERT INTO ReactRecord Values(?, ?, ?)", (player_name, score, now_kst))
        con.commit()

        while run:
            SCREEN.fill(WHITE)
            SCREEN.blit(success_text, (DISPLAY_WIDTH // 2 - success_text.get_width() // 2, 2 * DISPLAY_HEIGHT // 6))
            SCREEN.blit(avg_time_text, (DISPLAY_WIDTH // 2 - avg_time_text.get_width() // 2, 3 * DISPLAY_HEIGHT // 6))
            SCREEN.blit(quit_text, (DISPLAY_WIDTH // 2 - quit_text.get_width() // 2, 4 * DISPLAY_HEIGHT // 6))
            SCREEN.blit(record_text, (50, 45))

            cur.execute('Select DISTINCT ReactionTime From ReactRecord Order By ReactionTime Limit 15')
            for i, row in enumerate(cur):
                if score == row[0]:
                    record_time_text = get_font(35).render(f"{i+1}. {row[0]}", True, (0, 0, 255))
                else:
                    record_time_text = get_font(35).render(f"{i+1}. {row[0]}", True, (0, 0, 0))
                SCREEN.blit(record_time_text, (40, 120 + (i * 50)))

            # 마우스 클릭이 발생하면 게임 종료
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main_menu()
                if event.type == pygame.MOUSEBUTTONUP:
                    main_menu()


            pygame.display.update()
    
    react_first_menu()

def remember_game():
    # 게임 상수 설정
    GRID_SIZE = 8
    MARGIN = 10
    GRID_WIDTH, GRID_HEIGHT = (DISPLAY_WIDTH - (MARGIN * (GRID_SIZE - 1))) // GRID_SIZE, (DISPLAY_HEIGHT - (MARGIN * (GRID_SIZE - 1))) // GRID_SIZE
    Tiles = 6
    MAX_TRIES = 5
    GAME_TRIES = 5
    NOW_GAME_COUNT = 1
    RETRY_COUNT = 0
    WRONG_COUNT = 0
    ALL_CLICK_COUNT = 0
    first_flag = 0
    total_time = 0

    def remem_first_menu():
        pygame.event.clear()
        run = True
        while run:
            SCREEN.fill(WHITE)
            QUIT_BUTTON = Button(image=pygame.image.load(assets_quit_button), pos=(DISPLAY_WIDTH - 200, 150), 
                            text_input="Quit", font=get_font(40), base_color="#FF0000", hovering_color="White")
            text = get_font(100).render("화면에 나타난 연두색 타일을", True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2 - 200)
            SCREEN.blit(text, textRect)
            text = get_font(100).render("기억한 뒤 누르세요!", True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2 - 30)
            SCREEN.blit(text, textRect)
            text = get_font(80).render("화면을 눌러 시작하세요!", True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2 + 200)
            SCREEN.blit(text, textRect)
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            for button in [QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # 게임시작 = 키 입력, ESC = 나가기
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        main_menu()
                if event.type == pygame.MOUSEBUTTONUP:
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        sound_main_touch.play()
                        main_menu()
                    do_remem_game()

            pygame.display.update()

    def do_remem_game():
        pygame.event.clear()
        nonlocal NOW_GAME_COUNT, RETRY_COUNT, WRONG_COUNT, ALL_CLICK_COUNT, Tiles, first_flag, total_time
        run = True
        grid = []
        correct_count = 0
        click_tries = 0
        print(f"NOW_GAME_COUNT = {NOW_GAME_COUNT}, Tiles = {Tiles}")

        # 시작 전 카운트다운
        if first_flag == 0:
            first_flag = 1
            for i in range(2, 0, -1):
                SCREEN.fill(BLACK)
                # 마지막에 Start 출력
                if i == 1:
                    sound_game_start.play()
                    count_image = get_font(200).render("Start!", True, (0, 0, 255))
                    SCREEN.blit(count_image, (DISPLAY_WIDTH / 2 - 280, DISPLAY_HEIGHT / 2 - 120))
                else:
                    sound_game_ready.play()
                    count_image = get_font(200).render("Let's", True, (255, 255, 255))
                    SCREEN.blit(count_image, (DISPLAY_WIDTH / 2 - 250, DISPLAY_HEIGHT / 2 - 120))
                pygame.display.update()
                pygame.time.delay(1000)
                pygame.event.clear()
            
        SCREEN.fill(BLACK)

        def make_problem():
            nonlocal grid
            # 인덱스가 0 또는 7인 위치의 값은 0으로 설정 
            # 그 외의 위치 (인덱스가 1~6인 곳)에 1 값을 할당
            grid = [[0 if i == 0 or i == 7 or j == 0 or j == 7 else 1 for j in range(8)] for i in range(8)]

            # 정답 타일 생성
            def get_random_indices(num_values):
                indices = []
                for i in range(num_values):
                    while True:
                        row = random.randint(1,6)
                        col = random.randint(1,6)
                        # 중복확인
                        if (row, col) not in indices: 
                            indices.append((row,col))
                            break
                            
                return indices
            
            indices = get_random_indices(Tiles)

            # 얻은 결과와 해당하는 값을 출력
            for index in indices:
                grid[index[0]][index[1]] = 2
                value = grid[index[0]][index[1]]
                print(f"Value: {value}, Index: {index}")
            
            return indices
        
        def draw_rect(grid_color):
            pygame.draw.rect(SCREEN, grid_color, [(MARGIN+GRID_WIDTH) * col + MARGIN, (MARGIN+GRID_HEIGHT) * row + MARGIN, GRID_WIDTH, GRID_HEIGHT])
        
        indices = make_problem()
        print(indices)
        grid_color = BROWN
        for row in range(GRID_SIZE - 2):
            row = row + 1
            for col in range(GRID_SIZE - 2):
                col = col + 1
                if (row, col) in indices:
                    grid_color = LIME
                elif (row, col) not in indices:
                    grid_color = BROWN
                draw_rect(grid_color)
                
        pygame.display.update()
        print("Some output")
        sys.stdout.flush()  # 출력 버퍼 비우기
        pygame.time.delay(2000)
        pygame.event.clear()

        grid_color = BROWN
        for row in range(GRID_SIZE - 2):
            row = row + 1
            for col in range(GRID_SIZE - 2):
                col = col + 1
                draw_rect(grid_color)

        # 클릭 좌표 중첩되지 않도록 설정
        clicked_points = []
        print((DISPLAY_WIDTH // GRID_SIZE))
        print((DISPLAY_HEIGHT // GRID_SIZE))

        start_time = time.time()
        # 실제 게임 실행 구간
        while run:
            # 클릭 좌표 출력 및 행렬 좌표 설정
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        remem_first_menu()
                # 클릭했을 때 이벤트 실행
                if event.type == pygame.MOUSEBUTTONUP:
                    MOUSE_POS = pygame.mouse.get_pos()
                    sound_game_touch.play()
                    col = MOUSE_POS[0] // (DISPLAY_WIDTH // GRID_SIZE)
                    row = MOUSE_POS[1] // (DISPLAY_HEIGHT // GRID_SIZE)
                    point_x, point_y = col, row
                    print("Click ", MOUSE_POS,"Grid coordinates:",row,col, "Color: ", grid_color)
                    click_tries = click_tries + 1
                    ALL_CLICK_COUNT = ALL_CLICK_COUNT + 1

                    if grid[row][col] == 1:
                        grid_color = RED
                        WRONG_COUNT = WRONG_COUNT + 1
                    elif grid[row][col] == 2:
                        grid_color = LIME
                        if (point_x, point_y) not in clicked_points:
                            clicked_points.append((point_x, point_y))
                            correct_count = correct_count + 1  
                            click_tries = 0
                        print(f"Now Point is {correct_count}!!! Great!!!")
                    elif grid[row][col] == 0:
                        grid_color = BLACK

                    draw_rect(grid_color)
                    # print("Click ", MOUSE_POS,"Grid coordinates:",row,col, "Color: ", grid_color)

            clock.tick(60)
            pygame.display.update()

            if click_tries >= MAX_TRIES:
                grid_color = RED
                sound_remem_incorrect.play()
                for row in range(GRID_SIZE - 2):
                    row = row + 1
                    for col in range(GRID_SIZE - 2):
                        col = col + 1
                        draw_rect(grid_color)
                pygame.display.update()
                RETRY_COUNT = RETRY_COUNT + 1
                pygame.time.delay(1000)
                do_remem_game()

            if correct_count >= Tiles: 
                pygame.time.delay(300)
                sound_remem_correct.play()
                grid_color = BLUE
                for row in range(GRID_SIZE - 2):
                    row = row + 1
                    for col in range(GRID_SIZE - 2):
                        col = col + 1
                        if row == 1 or row == 6 or col == 1 or col == 6:
                            draw_rect(grid_color)
                pygame.display.update()
                pygame.time.delay(1000)
                NOW_GAME_COUNT = NOW_GAME_COUNT + 1
                Tiles = Tiles + 1   
                total_time = time.time() - start_time
                if NOW_GAME_COUNT > GAME_TRIES:
                    remem_result()
                do_remem_game()
            
                    
    # 결과 화면 출력
    def remem_result():
        nonlocal total_time
        sound_remem_end.play()
        pygame.event.clear()
        run = True
        total_time = round(total_time, 2)
        total_time_text = get_font(75).render(f"걸린 시간 : {total_time}초", True, (0, 0, 0))
        wrong_text = get_font(75).render(f"정답 횟수(정확도) : {WRONG_COUNT} / {ALL_CLICK_COUNT}", True, (0, 0, 0))
        retry_text = get_font(75).render(f"재시도한 게임 횟수 : {RETRY_COUNT}", True, (0, 0, 0))
        quit_text = get_font(50).render("화면을 눌러 종료하세요", True, (0, 0, 0))
        record_text = get_font(50).render("Record", True, (0, 0, 0))
        score = round((ALL_CLICK_COUNT - WRONG_COUNT) / ALL_CLICK_COUNT * 100, 5)
        player_name = "hea"
        now_kst = datetime.datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("INSERT INTO RememRecord Values(?, ?, ?)", (player_name, score, now_kst))
        con.commit()

        while run:
            SCREEN.fill(WHITE)
            SCREEN.blit(total_time_text, (DISPLAY_WIDTH // 2 - total_time_text.get_width() // 2, 1 * DISPLAY_HEIGHT // 6))
            SCREEN.blit(wrong_text, (DISPLAY_WIDTH // 2 - wrong_text.get_width() // 2, 2 * DISPLAY_HEIGHT // 6))
            SCREEN.blit(retry_text, (DISPLAY_WIDTH // 2 - retry_text.get_width() // 2, 3 * DISPLAY_HEIGHT // 6))
            SCREEN.blit(quit_text, (DISPLAY_WIDTH // 2 - quit_text.get_width() // 2, 4 * DISPLAY_HEIGHT // 6))
            SCREEN.blit(record_text, (50, 50))

            cur.execute('Select DISTINCT CorrectPercent From RememRecord Order By CorrectPercent DESC Limit 15')
            for i, row in enumerate(cur):
                if score == row[0]:
                    record_time_text = get_font(35).render(f"{i+1}. {row[0]}%", True, (0, 0, 255))
                else:
                    record_time_text = get_font(35).render(f"{i+1}. {row[0]}%", True, (0, 0, 0))
                SCREEN.blit(record_time_text, (40, 120 + (i * 50)))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    main_menu()
        
    remem_first_menu()

def avoid_wall_game():
    score = 0

    def avoid_wall_first_menu():
        pygame.event.clear()
        run = True
        while run:
            SCREEN.fill(WHITE)
            QUIT_BUTTON = Button(image=pygame.image.load(assets_quit_button), pos=(DISPLAY_WIDTH - 200, 150), 
                            text_input="Quit", font=get_font(40), base_color="#FF0000", hovering_color="White")
            text = get_font(100).render("우주선을 길에서 이탈시키지 말고", True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2 - 200)
            SCREEN.blit(text, textRect)
            text = get_font(100).render("방향을 조절하여 운행하세요!", True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2 - 30)
            SCREEN.blit(text, textRect)
            text = get_font(80).render("화면을 눌러 시작하세요!", True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2 + 200)
            SCREEN.blit(text, textRect)
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            for button in [QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # 게임시작 = 키 입력, ESC = 나가기
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        main_menu()
                if event.type == pygame.MOUSEBUTTONUP:
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        sound_main_touch.play()
                        main_menu()
                    do_avoid_wall_game()

            pygame.display.update()

    def do_avoid_wall_game():
        pygame.event.clear()
        nonlocal score
        pygame.mouse.set_visible(False)
        walls = DISPLAY_HEIGHT // 10
        ship_x = DISPLAY_WIDTH / 2
        velocity = 0
        fps = 30
        slope = random.randint(1,6)
        BG = pygame.image.load(assets_space)
        ship_image = pygame.image.load(assets_ship)
        bang_image = pygame.image.load(assets_bang)
        holes = []
        for xpos in range(walls):
            holes.append(pygame.Rect(700, (xpos * 10), 800, 10))
        game_over = False
        start_flag = True
        is_left = False
        sound_space_bg.play(-1)
        while True:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sound_space_bg.stop()
                        pygame.mouse.set_visible(False)
                        avoid_wall_first_menu()
                    if event.key == pygame.K_LEFT:
                        is_left = True
                    if event.key == pygame.K_RIGHT:
                        is_left = False
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if x < ship_x:
                        print(f"x_left = {x}")
                        is_left = True
                    if x >= ship_x:
                        print(f"x_right = {x}")
                        is_left = False

            #캐릭터 이동
            if not game_over:
                score += 1
                if velocity >= 10:
                    velocity = 10
                elif velocity <= -10:
                    velocity = -10
                velocity += -0.5 if is_left else 0.5
                ship_x += velocity

                #동굴을 스크롤
                edge = holes[0].copy()
                test = edge.move(slope, 0)
                #전환점 test.left <= 50 or test.right >= DISPLAY_WIDTH - 50 or 
                if test.left <= random.randint(0, 400) or test.right >= DISPLAY_WIDTH - random.randint(0, 400):
                    slope = random.randint(3,15) * (-1 if slope > 0 else 1)
                    # edge.inflate_ip(-10, 0)
                edge.move_ip(slope, -10)
                holes.insert(0, edge)
                del holes[-1]
                holes = [x.move(0, 10) for x in holes]

                #충돌 검사
                if holes[-18].left > ship_x or holes[-18].right < ship_x + 50 or holes[-10].left > ship_x or holes[-10].right < ship_x + 50:
                    print(f"holes[-18] = {holes[-18]}")
                    print(f"ship_x = {ship_x}")
                    print(f"fps = {fps}")
                    game_over = True

            fps = (score // 500) + 30

            #그리기
            SCREEN.blit(BG, (0, 0))
            for hole in holes:
                pygame.draw.rect(SCREEN, ("#E0B88A"), hole)
            SCREEN.blit(ship_image, (ship_x, 900))
            score_image = get_font(36).render("score is {}".format(score), True, (0,255,0))
            speed_image = get_font(36).render(f"{fps}km/s", True, (0,255,0))
            SCREEN.blit(score_image, (DISPLAY_WIDTH-250, 20))
            SCREEN.blit(speed_image, (DISPLAY_WIDTH-165, 70))

            clock.tick(fps)
            pygame.display.update()

            # 시작 전 카운트다운
            if start_flag:
                start_flag = False
                for i in range(2, 0, -1):
                    if i == 1:
                        pygame.draw.rect(SCREEN, WHITE, (DISPLAY_WIDTH / 2 - 300, DISPLAY_HEIGHT / 2 - 120, count_image.get_width()+ 100, count_image.get_height()))
                        count_image = get_font(200).render("Start!", True, (0, 0, 255))
                        SCREEN.blit(count_image, (DISPLAY_WIDTH / 2 - 280, DISPLAY_HEIGHT / 2 - 120))
                        sound_space_start.play()
                    else:
                        sound_game_ready.play()
                        count_image = get_font(200).render("Let's", True, (255, 255, 255))
                        SCREEN.blit(count_image, (DISPLAY_WIDTH / 2 - 250, DISPLAY_HEIGHT / 2 - 120))
                    pygame.display.update()
                    pygame.time.delay(1000)
                    pygame.event.clear()

            if game_over:
                SCREEN.blit(bang_image, (ship_x-30, 900))
                sound_space_bg.stop()
                sound_space_bang.play()
                pygame.display.update()
                pygame.time.delay(1500)
                avoid_wall_result()

    def avoid_wall_result():
        run = True
        sound_space_end.play()
        pygame.event.clear()
        score_text = get_font(75).render(f"우주선이 간 거리 : {score}", True, (0, 0, 0))
        quit_text = get_font(50).render("화면을 눌러 종료하세요", True, (0, 0, 0))
        record_text = get_font(50).render("Record", True, (0, 0, 0))
        
        player_name = "spc"
        now_kst = datetime.datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("INSERT INTO AvoidRecord Values(?, ?, ?)", (player_name, score, now_kst))
        con.commit()
        while run:
            SCREEN.fill(WHITE)
            SCREEN.blit(score_text, (DISPLAY_WIDTH // 2 - score_text.get_width() // 2, 2.5 * DISPLAY_HEIGHT // 6))
            SCREEN.blit(quit_text, (DISPLAY_WIDTH // 2 - quit_text.get_width() // 2, 3.5 * DISPLAY_HEIGHT // 6))
            SCREEN.blit(record_text, (50, 50))
            
            cur.execute('Select DISTINCT Score From AvoidRecord Order By Score DESC Limit 15')
            for i, row in enumerate(cur):
                if score == row[0]:
                    record_time_text = get_font(35).render(f"{i+1}. {row[0]}", True, (0, 0, 255))
                else:
                    record_time_text = get_font(35).render(f"{i+1}. {row[0]}", True, (0, 0, 0))
                SCREEN.blit(record_time_text, (40, 120 + (i * 50)))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        main_menu()
                if event.type == pygame.MOUSEBUTTONUP:
                    main_menu()

    avoid_wall_first_menu()

# 시작 메뉴 페이지
def main_menu():
    BG = pygame.image.load(assets_background)
    pygame.mouse.set_visible(True)
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(125).render("MAIN MENU", True, "#00FF00")
        MENU_RECT = MENU_TEXT.get_rect(center=(DISPLAY_WIDTH/2, 100))
        SELECT1_BUTTON = Button(image=pygame.image.load(assets_select2), pos=(DISPLAY_WIDTH/2, 250), 
                            text_input="타일 기억하기", font=get_font(100), base_color="#d7fcd4", hovering_color="White")
        SELECT2_BUTTON = Button(image=pygame.image.load(assets_select2), pos=(DISPLAY_WIDTH/2, 425), 
                            text_input="반응속도 올리기", font=get_font(100), base_color="#d7fcd4", hovering_color="White")
        SELECT3_BUTTON = Button(image=pygame.image.load(assets_select2), pos=(DISPLAY_WIDTH/2, 600), 
                            text_input="벽 피하기", font=get_font(100), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load(assets_quit_rect), pos=(DISPLAY_WIDTH/2, 775), 
                            text_input="QUIT", font=get_font(100), base_color="#FFFFFF", hovering_color="#000000")
        
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [SELECT1_BUTTON, SELECT2_BUTTON, SELECT3_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if SELECT1_BUTTON.checkForInput(MENU_MOUSE_POS):
                    sound_main_touch.play()
                    remember_game()
                if SELECT2_BUTTON.checkForInput(MENU_MOUSE_POS):
                    sound_main_touch.play()
                    reaction_game()
                if SELECT3_BUTTON.checkForInput(MENU_MOUSE_POS):
                    sound_main_touch.play()
                    avoid_wall_game()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        clock.tick(60)
        pygame.display.update()

main_menu()

