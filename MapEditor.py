import os
from pico2d import *
import math

# 설정
TILE_SIZE = 16
GRID_WIDTH = 100
GRID_HEIGHT = 50
WINDOW_WIDTH = TILE_SIZE * GRID_WIDTH + 100  # 오른쪽에 미리보기 패널을 위한 여유 공간
WINDOW_HEIGHT = TILE_SIZE * GRID_HEIGHT
TILE_FOLDER = os.path.join('resources', 'images', 'Map', 'StageMapTile')

# 타일 이미지 파일 목록
TILE_FILES = [
    'bottomTile0.png', 'bottomTile1.png', 'bottomTile2.png',
    'iceBottomTile0.png', 'iceBottomTile1.png', 'iceBottomTile2.png', 'iceFloorTile.png',
    'mapDecoObj0.png', 'mapDecoObj1.png', 'mapDecoObj2.png',
    'wallTile0.png', 'wallTile1.png', 'wallTile2.png', 'wallTile3.png', 'wallTile4.png',
    'wallTile5.png', 'wallTile6.png', 'wallTile7.png', 'wallTile8.png', 'backGroundTile.png',
    'IceWallTile0.png', 'IceWallTile1.png', 'IceWallTile2.png', 'IceWallTile3.png', 'IceWallTile4.png',
    'IceWallTile5.png', 'IceWallTile6.png', 'IceWallTile7.png'
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
is_dragging = False  # 드래그 상태 추적
is_erasing = False   # 지우기 드래그 상태 추적
# 영역 선택 드래그
is_area_selecting = False
area_start = None  # (gx, gy)
area_end = None    # (gx, gy)
# 지우개 모드
eraser_mode = False

# 맵 저장 함수
def save_map(filename='map2.txt'):
    try:
        with open(filename, 'w') as f:
            for row in map_data:
                f.write(' '.join(str(idx) for idx in row) + '\n')
        print(f"맵이 {filename}에 저장되었습니다")
    except Exception as e:
        print(f"맵 저장 실패: {e}")

# 맵 로드 함수
def load_map(filename='map2.txt'):
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
    global running, selected_tile, is_dragging, is_erasing, is_area_selecting, area_start, area_end, eraser_mode
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
            elif e.key == SDLK_e:
                eraser_mode = not eraser_mode
                if eraser_mode:
                    print("지우개 모드 활성화")
                else:
                    print("지우개 모드 비활성화")
        elif e.type == SDL_MOUSEBUTTONDOWN:
            mx, my = e.x, WINDOW_HEIGHT - e.y

            # Shift 키를 누른 상태에서 좌클릭 - 영역 선택 모드
            if e.button == SDL_BUTTON_LEFT and mx < GRID_WIDTH * TILE_SIZE:
                gx, gy = mx // TILE_SIZE, my // TILE_SIZE
                if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                    # SDL_GetModState()로 Shift 키 확인
                    try:
                        import ctypes
                        SDL_GetModState = ctypes.CDLL('SDL2.dll').SDL_GetModState
                        KMOD_SHIFT = 0x0003
                        if SDL_GetModState() & KMOD_SHIFT:
                            # 영역 선택 모드
                            is_area_selecting = True
                            area_start = (gx, gy)
                            area_end = (gx, gy)
                            print(f"영역 선택 시작: ({gx}, {gy})")
                        else:
                            # 일반 드래그 모드
                            if eraser_mode:
                                map_data[gy][gx] = -1
                                print(f"({gx}, {gy})의 타일을 제거했습니다")
                            else:
                                map_data[gy][gx] = selected_tile
                                print(f"타일 {TILE_FILES[selected_tile]}을 ({gx}, {gy})에 배치했습니다")
                            is_dragging = True
                    except:
                        # SDL_GetModState 실패 시 일반 드래그로 처리
                        if eraser_mode:
                            map_data[gy][gx] = -1
                        else:
                            map_data[gy][gx] = selected_tile
                        is_dragging = True
            # 우클릭 - 타일 지우기
            elif e.button == SDL_BUTTON_RIGHT and mx < GRID_WIDTH * TILE_SIZE:
                gx, gy = mx // TILE_SIZE, my // TILE_SIZE
                if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                    map_data[gy][gx] = -1
                    is_erasing = True
                    print(f"({gx}, {gy})의 타일을 제거했습니다")
            # 미리보기 타일 클릭 처리
            elif e.button == SDL_BUTTON_LEFT and mx >= GRID_WIDTH * TILE_SIZE:
                total = len(tile_images)
                if total > 0:
                    per_col = math.ceil(total / 3)
                    for col in range(3):
                        preview_x = GRID_WIDTH * TILE_SIZE + 20 + col * (TILE_SIZE + 10)
                        start_idx = col * per_col
                        end_idx = min(total, (col + 1) * per_col)
                        for idx in range(start_idx, end_idx):
                            i = idx - start_idx
                            tile_center_y = WINDOW_HEIGHT - (i + 1) * (TILE_SIZE + 10) + TILE_SIZE // 2
                            if preview_x <= mx < preview_x + TILE_SIZE and tile_center_y - TILE_SIZE // 2 <= my < tile_center_y + TILE_SIZE // 2:
                                selected_tile = idx
                                eraser_mode = False  # 타일 선택 시 지우개 모드 자동 해제
                                print(f"선택된 타일: {TILE_FILES[selected_tile]}")
        elif e.type == SDL_MOUSEBUTTONUP:
            if e.button == SDL_BUTTON_LEFT:
                # 영역 선택 종료 - 영역 채우기
                if is_area_selecting and area_start and area_end:
                    ax1, ay1 = area_start
                    ax2, ay2 = area_end
                    for y in range(min(ay1, ay2), max(ay1, ay2) + 1):
                        for x in range(min(ax1, ax2), max(ax1, ax2) + 1):
                            if eraser_mode:
                                map_data[y][x] = -1
                            else:
                                map_data[y][x] = selected_tile
                    if eraser_mode:
                        print(f"영역 ({ax1}, {ay1})~({ax2}, {ay2})을 지웠습니다")
                    else:
                        print(f"영역 ({ax1}, {ay1})~({ax2}, {ay2})을 타일 {TILE_FILES[selected_tile]}로 채웠습니다")
                is_dragging = False
                is_area_selecting = False
                area_start = None
                area_end = None
            elif e.button == SDL_BUTTON_RIGHT:
                is_erasing = False
        elif e.type == SDL_MOUSEMOTION:
            mx, my = e.x, WINDOW_HEIGHT - e.y
            # 영역 선택 드래그 중 - 끝점 업데이트
            if is_area_selecting and mx < GRID_WIDTH * TILE_SIZE:
                gx, gy = mx // TILE_SIZE, my // TILE_SIZE
                if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                    area_end = (gx, gy)
            # 일반 드래그 중일 때 타일 배치 또는 지우기
            elif is_dragging and mx < GRID_WIDTH * TILE_SIZE:
                gx, gy = mx // TILE_SIZE, my // TILE_SIZE
                if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                    if eraser_mode:
                        if map_data[gy][gx] != -1:
                            map_data[gy][gx] = -1
                    else:
                        if map_data[gy][gx] != selected_tile:
                            map_data[gy][gx] = selected_tile
            # 우클릭 드래그 중일 때 타일 지우기
            elif is_erasing and mx < GRID_WIDTH * TILE_SIZE:
                gx, gy = mx // TILE_SIZE, my // TILE_SIZE
                if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                    if map_data[gy][gx] != -1:
                        map_data[gy][gx] = -1

# 메인 루프
while running:
    clear_canvas()

    # 맵 그리기
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            idx = map_data[y][x]
            if idx >= 0 and idx < len(tile_images):
                tile_images[idx].draw(x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2, TILE_SIZE, TILE_SIZE)

    # 영역 선택 중이면 선택 영역 표시
    if is_area_selecting and area_start and area_end:
        ax1, ay1 = area_start
        ax2, ay2 = area_end
        min_x = min(ax1, ax2) * TILE_SIZE
        max_x = (max(ax1, ax2) + 1) * TILE_SIZE
        min_y = min(ay1, ay2) * TILE_SIZE
        max_y = (max(ay1, ay2) + 1) * TILE_SIZE
        draw_rectangle(min_x, min_y, max_x, max_y)

    # 미리보기 타일 그리기 (3열로 배치)
    total = len(tile_images)
    if total > 0:
        per_col = math.ceil(total / 3)
        for col in range(3):
            preview_x = GRID_WIDTH * TILE_SIZE + 20 + col * (TILE_SIZE + 10)
            start_idx = col * per_col
            end_idx = min(total, (col + 1) * per_col)
            for idx in range(start_idx, end_idx):
                i = idx - start_idx
                tile_center_y = WINDOW_HEIGHT - (i + 1) * (TILE_SIZE + 10) + TILE_SIZE // 2
                tile_images[idx].draw(preview_x + TILE_SIZE // 2, tile_center_y, TILE_SIZE, TILE_SIZE)

    # 선택된 타일 주변에 테두리 그리기 (지우개 모드가 아닐 때만)
    if not eraser_mode and selected_tile < len(tile_images):
        total = len(tile_images)
        per_col = math.ceil(total / 3) if total > 0 else 1
        col_idx = selected_tile // per_col
        row_idx = selected_tile % per_col
        preview_x = GRID_WIDTH * TILE_SIZE + 20 + col_idx * (TILE_SIZE + 10)
        tile_y = WINDOW_HEIGHT - (row_idx + 1) * (TILE_SIZE + 10)
        draw_rectangle(preview_x, tile_y, preview_x + TILE_SIZE, tile_y + TILE_SIZE)

    update_canvas()
    handle_events()

close_canvas()
