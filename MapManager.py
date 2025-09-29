import os
from pico2d import *
from ImageManager import ImageManager


class MapManager:
    # 타일 이미지 파일 목록 (맵 에디터와 동일)
    TILE_FILES = [
        'bottomTile0.png', 'bottomTile1.png', 'bottomTile2.png',
        'iceBottomTile0.png', 'iceBottomTile1.png', 'iceBottomTile2.png', 'iceFloorTile.png',
        'mapDecoObj0.png', 'mapDecoObj1.png', 'mapDecoObj2.png',
        'wallTile0.png', 'wallTile1.png', 'wallTile2.png', 'wallTile3.png', 'wallTile4.png',
        'wallTile5.png', 'wallTile6.png', 'wallTile7.png', 'wallTile8.png', 'backGroundTile.png'
    ]

    def __init__(self, grid_width=20, grid_height=15, tile_size=32, filename='map.txt'):
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

        # 타일 이미지 로드
        self.load_tiles()
        # 맵 데이터 로드
        self.load_map()

    def load_tiles(self):
        """ImageManager를 통해 타일 이미지를 로드"""
        for file in self.TILE_FILES:
            try:
                # 타일 이미지 경로를 resources/images/Map/StageMapTile에 맞게 설정
                path = os.path.join('resources', 'images', 'Map', 'StageMapTile', file)
                ImageManager.load_image(file, path, 1)  # 프레임 수는 1로 고정
                img, _, _, _ = ImageManager.get_image(file)
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

    def render(self):
        """맵 타일을 화면에 렌더링"""
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                idx = self.map_data[y][x]
                if idx >= 0 and idx < len(self.tile_images):
                    self.tile_images[idx].draw(
                        x * self.TILE_SIZE + self.TILE_SIZE // 2,
                        y * self.TILE_SIZE + self.TILE_SIZE // 2,
                        self.TILE_SIZE, self.TILE_SIZE
                    )

    def set_tile(self, x, y, tile_idx):
        """지정된 좌표에 타일 인덱스 설정"""
        if 0 <= x < self.GRID_WIDTH and 0 <= y < self.GRID_HEIGHT:
            self.map_data[y][x] = tile_idx
            print(f"타일 {self.TILE_FILES[tile_idx]}을 ({x}, {y})에 배치했습니다")
        else:
            print(f"잘못된 좌표: ({x}, {y})")

