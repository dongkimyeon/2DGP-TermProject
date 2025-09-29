import os
from pico2d import *

# 설정
TILE_SIZE = 32
GRID_WIDTH = 20
GRID_HEIGHT = 15
WINDOW_WIDTH = TILE_SIZE * GRID_WIDTH + 200  # 오른쪽에 미리보기 패널을 위한 여유 공간
WINDOW_HEIGHT = TILE_SIZE * GRID_HEIGHT
TILE_FOLDER = os.path.join('resources', 'images', 'Map', 'StageMapTile')

# 타일 이미지 파일 목록
TILE_FILES = [
    'bottomTile0.png', 'bottomTile1.png', 'bottomTile2.png',
    'iceBottomTile0.png', 'iceBottomTile1.png', 'iceBottomTile2.png', 'iceFloorTile.png',
    'mapDecoObj0.png', 'mapDecoObj1.png', 'mapDecoObj2.png',
    'wallTile0.png', 'wallTile1.png', 'wallTile2.png', 'wallTile3.png', 'wallTile4.png',
    'wallTile5.png', 'wallTile6.png', 'wallTile7.png', 'wallTile8.png', 'backGroundTile.png'
]

# 초기화
open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)

tile_images = []
for file in TILE_FILES:
    path = os.path.join(TILE_FOLDER, file)
    try:
        tile_images.append(load_image(path))
    except IOError:
        print(f"타일 이미지 로드 실패: {path}")
        close_canvas()
        exit(1)

selected_tile = 0
map_data = [[-1 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
running = True

# 맵 저장 함수
def save_map(filename='map.txt'):
    try:
        with open(filename, 'w') as f:
            for row in map_data:
                f.write(' '.join(str(idx) for idx in row) + '\n')
        print(f"맵이 {filename}에 저장되었습니다")
    except Exception as e:
        print(f"맵 저장 실패: {e}")

# 맵 로드 함수
def load_map(filename='map.txt'):
    global map_data
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            for y, line in enumerate(lines):
                if y < GRID_HEIGHT:
                    row = [int(idx) for idx in line.strip().split()]
                    if len(row) == GRID_WIDTH:
                        map_data[y] = row
        print(f"{filename}에서 맵을 로드했습니다")
    except Exception as e:
        print(f"맵 로드 실패: {e}")

# 이벤트 처리 함수
def handle_events():
    global running, selected_tile
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            running = False
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                running = False
            elif e.key == SDLK_s:
                save_map()
            elif e.key == SDLK_l:
                load_map()
        elif e.type == SDL_MOUSEBUTTONDOWN:
            mx, my = e.x, WINDOW_HEIGHT - e.y  # pico2d는 y좌표가 아래에서 위로 증가
            # 맵 그리드 클릭 처리
            if e.button == SDL_BUTTON_LEFT and mx < GRID_WIDTH * TILE_SIZE:
                gx, gy = mx // TILE_SIZE, my // TILE_SIZE
                if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                    map_data[gy][gx] = selected_tile
                    print(f"타일 {TILE_FILES[selected_tile]}을 ({gx}, {gy})에 배치했습니다")
            elif e.button == SDL_BUTTON_RIGHT and mx < GRID_WIDTH * TILE_SIZE:
                gx, gy = mx // TILE_SIZE, my // TILE_SIZE
                if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                    map_data[gy][gx] = -1
                    print(f"({gx}, {gy})의 타일을 제거했습니다")
            # 미리보기 타일 클릭 처리
            elif e.button == SDL_BUTTON_LEFT and mx >= GRID_WIDTH * TILE_SIZE:
                for col in range(3):
                    preview_x = GRID_WIDTH * TILE_SIZE + 20 + col * (TILE_SIZE + 10)
                    num_tiles = 7 if col < 2 else 6  # 첫 두 열: 7개, 마지막 열: 6개
                    start_idx = 7 if col == 1 else 14 if col == 2 else 0
                    for i in range(num_tiles):
                        tile_idx = start_idx + i
                        if tile_idx >= len(tile_images):
                            break
                        tile_y = WINDOW_HEIGHT - (i + 1) * (TILE_SIZE + 10) + TILE_SIZE // 2
                        if preview_x <= mx < preview_x + TILE_SIZE and tile_y - TILE_SIZE // 2 <= my < tile_y + TILE_SIZE // 2:
                            selected_tile = tile_idx
                            print(f"선택된 타일: {TILE_FILES[selected_tile]}")


# 메인 루프
while running:
    clear_canvas()
    # 맵 그리기
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            idx = map_data[y][x]
            if idx >= 0 and idx < len(tile_images):
                tile_images[idx].draw(x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2, TILE_SIZE, TILE_SIZE)
    # 미리보기 타일 그리기 (3열로 배치)
    for col in range(3):
        preview_x = GRID_WIDTH * TILE_SIZE + 20 + col * (TILE_SIZE + 10)
        num_tiles = 7 if col < 2 else 6  # 첫 두 열: 7개, 마지막 열: 6개
        start_idx = 7 if col == 1 else 14 if col == 2 else 0
        for i in range(num_tiles):
            tile_idx = start_idx + i
            if tile_idx >= len(tile_images):
                break
            tile_y = WINDOW_HEIGHT - (i + 1) * (TILE_SIZE + 10)
            tile_images[tile_idx].draw(preview_x + TILE_SIZE // 2, tile_y + TILE_SIZE // 2, TILE_SIZE, TILE_SIZE)
    update_canvas()
    handle_events()

close_canvas()