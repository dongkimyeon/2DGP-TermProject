import os
from pico2d import *
from ResourceManager import ResourceManager


class MapManager:
    # 타일 이미지 파일 목록 (맵 에디터와 동일)
    TILE_FILES = [
        'bottomTile0.png', 'bottomTile1.png', 'bottomTile2.png',
        'iceBottomTile0.png', 'iceBottomTile1.png', 'iceBottomTile2.png', 'iceFloorTile.png',
        'mapDecoObj0.png', 'mapDecoObj1.png', 'mapDecoObj2.png',
        'wallTile0.png', 'wallTile1.png', 'wallTile2.png', 'wallTile3.png', 'wallTile4.png',
        'wallTile5.png', 'wallTile6.png', 'wallTile7.png', 'wallTile8.png', 'backGroundTile.png',
        'IceWallTile0.png', 'IceWallTile1.png', 'IceWallTile2.png', 'IceWallTile3.png', 'IceWallTile4.png',
        'IceWallTile5.png', 'IceWallTile6.png', 'IceWallTile7.png'
    ]

    def __init__(self, grid_width=100, grid_height=50, tile_size=16, filename='map.txt'):
        """
        초기화: 맵 크기, 타일 크기, 맵 파일 경로 설정
        :param grid_width: 맵의 가로 타일 수
        :param grid_height: 맵의 세로 타일 수
        :param tile_size: 타일의 픽셀 크기 (가로/세로)
        :param filename: 맵 데이터 파일 경로
        """
        self.TILE_SIZE = tile_size * 1.5
        self.GRID_WIDTH = grid_width
        self.GRID_HEIGHT = grid_height
        self.filename = filename
        self.tile_images = []
        self.map_data = [[-1 for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        self.collision_tiles = []  # 충돌 타일 정보 저장

        # 타일 이미지 로드
        self.load_tiles()
        # 맵 데이터 로드
        self.load_map()
        # 충돌 타일 생성
        self.build_collision_tiles()

    def load_tiles(self):
        """ResourceManager를 통해 타일 이미지를 로드"""
        for file in self.TILE_FILES:
            try:
                # 타일 이미지 경로를 resources/images/Map/StageMapTile에 맞게 설정
                path = os.path.join('resources', 'images', 'Map', 'StageMapTile', file)
                ResourceManager.load_image(file, path, 1)  # 프레임 수는 1로 고정
                img, _, _, _ = ResourceManager.get_image(file)
                if img:
                    self.tile_images.append(img)
                else:
                    print(f"타일 이미지 로드 실패: {file}")
            except Exception as e:
                print(f"타일 이미지 로드 실패: {file}, 오류: {e}")

    def load_map(self):
        """map.txt 파일에서 맵 데이터를 로드"""
        try:
            with open(self.filename, 'r') as f:
                lines = f.readlines()
                for y, line in enumerate(lines):
                    if y < self.GRID_HEIGHT:
                        row = [int(idx) for idx in line.strip().split()]
                        if len(row) == self.GRID_WIDTH:
                            self.map_data[y] = row
            print(f"{self.filename}에서 맵을 로드했습니다")
        except Exception as e:
            print(f"맵 로드 실패: {e}")

    def is_collision_tile(self, tile_idx):
        """충돌이 발생하는 타일인지 확인

        주의: 여기에서 build_collision_tiles()를 호출하면 build -> is_collision_tile -> build ... 식의
        무한 재귀가 발생하므로 절대 호출하지 않습니다.
        """
        if tile_idx < 0 or tile_idx >= len(self.TILE_FILES):
            return False

        tile_name = self.TILE_FILES[tile_idx].lower()
        # wallTile 또는 bottomTile 키워드가 포함된 타일은 충돌 타일
        # ice 관련 타일도 충돌로 처리
        return any(k in tile_name for k in ('walltile', 'bottomtile', 'icebottom', 'icefloortile', 'icewalltile'))

    def build_collision_tiles(self):
        """맵 데이터에서 충돌 타일 정보 추출"""
        self.collision_tiles = []
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                idx = self.map_data[y][x]
                if self.is_collision_tile(idx):
                    # 타일의 충돌 박스 정보 저장 (left, bottom, right, top)
                    tile_bb = {
                        'x': x * self.TILE_SIZE,
                        'y': y * self.TILE_SIZE,
                        'left': x * self.TILE_SIZE,
                        'bottom': y * self.TILE_SIZE,
                        'right': (x + 1) * self.TILE_SIZE,
                        'top': (y + 1) * self.TILE_SIZE
                    }
                    self.collision_tiles.append(tile_bb)

    def get_collision_tiles_in_range(self, left, bottom, right, top):
        """특정 영역 내의 충돌 타일 반환"""
        tiles = []
        for tile in self.collision_tiles:
            if not (tile['right'] < left or tile['left'] > right or
                   tile['top'] < bottom or tile['bottom'] > top):
                tiles.append(tile)
        return tiles

    def check_collision(self, obj_left, obj_bottom, obj_right, obj_top):
        """객체와 맵 타일 간의 충돌 검사"""
        return self.get_collision_tiles_in_range(obj_left, obj_bottom, obj_right, obj_top)

    def render(self, camera_x=0, camera_y=0, zoom=1.0, draw_collision_box=False):
        """맵 타일을 화면에 렌더링"""
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                idx = self.map_data[y][x]
                if idx >= 0 and idx < len(self.tile_images):
                    screen_x = (x * self.TILE_SIZE - camera_x) * zoom + int(self.TILE_SIZE // 2 * zoom)
                    screen_y = (y * self.TILE_SIZE - camera_y) * zoom + int(self.TILE_SIZE // 2 * zoom)


                    if idx >= 0 and idx < len(self.TILE_FILES):
                        tile_name = self.TILE_FILES[idx].lower()
                        if 'mapdeco' in tile_name:
                            screen_y -= 5 * zoom

                    self.tile_images[idx].draw(
                        screen_x,
                        screen_y,
                        int(self.TILE_SIZE * zoom), int(self.TILE_SIZE * zoom)
                    )

        # 충돌 박스 그리기
        if draw_collision_box:
            self.draw_collision_boxes(camera_x, camera_y, zoom)

    def draw_collision_boxes(self, camera_x=0, camera_y=0, zoom=1.0):
        """충돌 타일의 경계 박스 그리기"""
        for tile in self.collision_tiles:
            screen_left = (tile['left'] - camera_x) * zoom
            screen_bottom = (tile['bottom'] - camera_y) * zoom
            screen_right = (tile['right'] - camera_x) * zoom
            screen_top = (tile['top'] - camera_y) * zoom

            draw_rectangle(screen_left, screen_bottom, screen_right, screen_top)

    def set_tile(self, x, y, tile_idx):
        """지정된 좌표에 타일 인덱스 설정"""
        if 0 <= x < self.GRID_WIDTH and 0 <= y < self.GRID_HEIGHT:
            self.map_data[y][x] = tile_idx
            print(f"타일 {self.TILE_FILES[tile_idx]}을 ({x}, {y})에 배치했습니다")
        else:
            print(f"잘못된 좌표: ({x}, {y})")
