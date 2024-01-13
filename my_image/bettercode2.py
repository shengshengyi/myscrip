import os
import cv2
import numpy as np
import mss
import re
import logging
import time

class ImageProcessor:
    def __init__(self):
        self.scene_dict = {
            '1': '应天府',
            '2': '星秀村东',
            '3': '星秀村',
            '4': '汴京城',
            '5': '芒肠山路'
        }
        self.herbs_dict = {
            '1': '草药采集1',
            '2': '草药采集2',
            '3': '草药采集3'
        }
        self.pet_drinks_dict = {
            '1': '宠物饮料1',
        }
        self.initialize_paths()

    def initialize_paths(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.scene_path = os.path.join(script_dir, '..', 'pic', 'scene_flag')
        self.herbs_path = os.path.join(script_dir, '..', 'pic', 'herbs_flag')
        self.pet_drinks_path = os.path.join(script_dir, '..', 'pic', 'pet_drinks_flag')

    def get_matching_params(self, matching_para):
        if matching_para == "herbs":
            return self.herbs_flags, 0.65, self.herbs_dict, self.herbs_path
        elif matching_para == "pet_drinks":
            return self.pet_drinks_flags, 0.65, self.pet_drinks_dict, self.pet_drinks_path
        elif matching_para == "scene":
            return self.scene_flags, 0.85, self.scene_dict, self.scene_path
        else:
            raise ValueError(f"Unsupported matching parameter: {matching_para}")

    def identify_scene(self, scene_gray, matching_para):
        matching_data = self.get_matching_params(matching_para)
        flags, flag_similar, flag_dict, flag_path = matching_data
        for flag in flags:
            flag_scene = cv2.imread(os.path.join(flag_path, flag))
            if flag_scene is None:
                logging.error(f"Cannot load scene image: {flag}")
                continue
            flag_scene_gray = cv2.cvtColor(flag_scene, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(scene_gray, flag_scene_gray, cv2.TM_CCOEFF_NORMED)
            locations = np.where(result >= flag_similar)
            locations = list(zip(*locations[::-1]))
            if len(locations) > 0:
                match = re.match(r'(\d+)', flag)
                if match:
                    scene_number = match.group(1)
                    return flag_dict.get(scene_number, "未知场景2")
                else:
                    return None
        return f"未找到 {matching_para}"

    def capture_and_identify(self, left, top, width, height, matching_para):
        area = {"left": left, "top": top, "width": width, "height": height}
        with mss.mss() as sct:
            area_capture = sct.grab(area)
            area_capture = np.array(area_capture)
            screen_gray = cv2.cvtColor(area_capture, cv2.COLOR_BGR2GRAY)
            scene = self.identify_scene(screen_gray, matching_para)
            return scene

    def find_matching_position(self, scene_gray, matching_para):
        matching_data = self.get_matching_params(matching_para)
        _, _, _, flag_path = matching_data
        flags, flag_similar, _, _ = self.get_matching_params(matching_para)
        for flag in flags:
            flag_scene = cv2.imread(os.path.join(flag_path, flag))
            if flag_scene is None:
                logging.error(f"Cannot load scene image: {flag}")
                continue
            flag_scene_gray = cv2.cvtColor(flag_scene, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(scene_gray, flag_scene_gray, cv2.TM_CCOEFF_NORMED)
            locations = np.where(result >= flag_similar)
            locations = list(zip(*locations[::-1]))
            if len(locations) > 0:
                return locations[0]
        return (0, 0)

    def get_matching_position(self, left, top, width, height, matching_para):
        area = {"left": left, "top": top, "width": width, "height": height}
        with mss.mss() as sct:
            area_capture = sct.grab(area)
            area_capture = np.array(area_capture)
            screen_gray = cv2.cvtColor(area_capture, cv2.COLOR_BGR2GRAY)
            position = self.find_matching_position(screen_gray, matching_para)
            return (position[0] + left, position[1] + top)

if __name__ == "__main__":
    a = ImageProcessor()
    print(a.capture_and_identify(30, 30, 1000, 800, "herbs"))
    time.sleep(0.1)
    print(a.get_matching_position(30, 30, 1000, 800, "herbs"))
    time.sleep(0.1)

    print(a.capture_and_identify(30, 30, 1000, 800, "pet_drinks"))
    time.sleep(0.1)
    print(a.get_matching_position(30, 30, 1000, 800, "pet_drinks"))
    time.sleep(0.1)

    print(a.capture_and_identify(30, 30, 1000, 800, "scene"))
    time.sleep(0.1)
    print(a.get_matching_position(30, 30, 1000, 800, "scene"))
    time.sleep(0.1)