"""
ObjectLoader.py
텍스트 파일에서 오브젝트 좌표를 읽어와서 생성하는 모듈
"""

from Enemy_Skel import Skel
from Enemy_Ghost import Ghost
from Enemy_Bat import Bat
from Enemy_Banshee import Banshee


class ObjectLoader:
    """텍스트 파일에서 오브젝트를 로드하는 클래스"""

    @staticmethod
    def load_from_file(filename, map_manager=None):
        """
        텍스트 파일에서 오브젝트 좌표를 읽어와서 생성

        Args:
            filename (str): 좌표 파일 이름
            map_manager: 맵 매니저 참조 (옵션)

        Returns:
            list: 생성된 오브젝트 리스트
        """
        objects = []

        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:  # 빈 줄 건너뛰기
                        continue

                    parts = line.split()
                    if len(parts) != 3:
                        continue

                    obj_type = parts[0]
                    x = int(parts[1])
                    y = int(parts[2])

                    # 오브젝트 타입에 따라 생성
                    obj = ObjectLoader._create_object(obj_type, x, y, map_manager)
                    if obj:
                        objects.append(obj)

            print(f"[ObjectLoader] Loaded {len(objects)} objects from {filename}")

        except FileNotFoundError:
            print(f"[ObjectLoader] Warning: {filename} not found. No objects loaded.")
        except Exception as e:
            print(f"[ObjectLoader] Error loading objects: {e}")

        return objects

    @staticmethod
    def _create_object(obj_type, x, y, map_manager=None):
        """
        오브젝트 타입에 따라 적절한 오브젝트 생성

        Args:
            obj_type (str): 오브젝트 타입 (s, g, b, v)
            x (int): x 좌표
            y (int): y 좌표
            map_manager: 맵 매니저 참조 (옵션)

        Returns:
            생성된 오브젝트 또는 None
        """
        obj = None

        if obj_type == 's':  # Skel
            obj = Skel()
            obj.set_position(x, y)
            if map_manager:
                obj.set_map_manager(map_manager)

        elif obj_type == 'g':  # Ghost
            obj = Ghost()
            obj.set_position(x, y)
            if map_manager:
                obj.set_map_manager(map_manager)

        elif obj_type == 'b':  # Bat
            obj = Bat()
            obj.set_position(x, y)
            if map_manager:
                obj.set_map_manager(map_manager)

        elif obj_type == 'v':  # Banshee
            obj = Banshee()
            obj.set_position(x, y)
            if map_manager:
                obj.set_map_manager(map_manager)

        return obj

    @staticmethod
    def save_to_file(filename, objects):
        """
        오브젝트 리스트를 텍스트 파일로 저장

        Args:
            filename (str): 저장할 파일 이름
            objects (list): 저장할 오브젝트 리스트
        """
        try:
            with open(filename, 'w') as f:
                for obj in objects:
                    obj_type = ObjectLoader._get_object_type(obj)
                    if obj_type:
                        f.write(f"{obj_type} {int(obj.x)} {int(obj.y)}\n")

            print(f"[ObjectLoader] Saved {len(objects)} objects to {filename}")

        except Exception as e:
            print(f"[ObjectLoader] Error saving objects: {e}")

    @staticmethod
    def _get_object_type(obj):
        """
        오브젝트의 타입 문자 반환

        Args:
            obj: 오브젝트 인스턴스

        Returns:
            str: 타입 문자 (s, g, b, v) 또는 None
        """
        if isinstance(obj, Skel):
            return 's'
        elif isinstance(obj, Ghost):
            return 'g'
        elif isinstance(obj, Bat):
            return 'b'
        elif isinstance(obj, Banshee):
            return 'v'
        return None

