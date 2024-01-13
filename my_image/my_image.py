import sys
import time

# 导入截屏模块
import mss
import cv2
import numpy as np #numpy 库,简单理解为将图片转换成数组的库,因为 opencv 无法直接处理 mss 的截图,需要用 numpy 转换成数组
import re
import logging
# 设置日志基本配置
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='screen_capture.log',
                    filemode='a')
# 确保日志文件使用 UTF-8 编码
with open('screen_capture.log', 'a', encoding='utf-8') as file:
    logging.StreamHandler(file)

class my_image:

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
        self.scene_flag = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg']
        self.herbs_flag = ['1.jpg','2.jpg','3.jpg']
        self.pet_drinks_flag = ['1.jpg']

    def matching_prop(self,scene_gray,matching_para):
        """
        匹配场景函数。
        参数：
        scene_gray：灰度化的场景图片，用于与预设的场景图片进行匹配。
        matching_param：匹配参数，用于指定使用哪种场景字典和路径进行匹配。
                        默认None为场景识别，"prop"为道具识别
        返回：
        返回匹配到的场景名称，如果匹配失败则返回"未知场景"。
        """
        if matching_para == "herbs":
            flag = self.herbs_flag
            flag_similar = 0.65
            flag_dict = self.herbs_dict
            flag_path = '../pic/herbs_flag/'
        elif matching_para == "pet_drinks":
            flag = self.pet_drinks_flag
            flag_similar = 0.65
            flag_dict = self.pet_drinks_dict
            flag_path = '../pic/pet_drinks_flag/'
        elif matching_para == "scene":
            flag = self.scene_flag
            flag_similar = 0.85
            flag_dict = self.scene_dict
            flag_path = '../pic/scene_flag/'

        for i in flag:
            try:
                # 获取预设地图场景
                flag_scene = cv2.imread(flag_path+i)
                if flag_scene is None:
                    logging.error(f"无法加载场景图片： {i}")
                    return "未知场景1"
                flag_scene_gray = cv2.cvtColor(flag_scene, cv2.COLOR_BGR2GRAY)
                # 在大图片中查找小图片
                result = cv2.matchTemplate(scene_gray, flag_scene_gray, cv2.TM_CCOEFF_NORMED)
                # 筛选结果
                locations = np.where(result >= flag_similar)
                # 用 np 筛选一下结果高于 0.85的
                # print(locations)

                locations = list(zip(*locations[::-1]))
                # print("1",locations)
                # 将结果再次处理一下，仅保留坐标值
                if len(locations) > 0:
                    match = re.match(r'(\d+)', i)
                    if match:
                        scene_number = match.group(1)
                        # 根据匹配到的场景编号返回对应场景名称
                        return flag_dict.get(scene_number,"未知物品2")
                    else:
                        return None
            except Exception as e:
                logging.error(f"处理场景时发生异常： {e}")
                return "未知物品3"
        return "未找到" + matching_para

    def get_prop(self, left, top, width, height,matching_para):
        area = {"left": left, "top": top, "width": width, "height": height}
        with mss.mss() as sct:
            scene = '未知'
            #role_location = (0,0)
            #获取大图片
            area_capture = sct.grab(area)#对屏幕 进行截图
            area_capture = np.array(area_capture)#调用 numpy 库将 mss 库的截屏转换一下,并赋值为变量 quyujieping
            screen_gray = cv2.cvtColor(area_capture,cv2.COLOR_BGR2GRAY)

            # 判断场景
            scene = self.matching_prop(screen_gray,matching_para)
            # print('检测到1:', scene)
            return scene


            # cv2.imshow("DNF", area_capture)  # 调用 opencv 的 imshow 方法显示图片
            # if cv2.waitKey(5) & 0xFF == ord("q"):
            #     cv2.destroyAllWindows()
                #     break

    def matchaing_prop_location(self,scene_gray,matching_para):
        if matching_para == "herbs":
            flag = self.herbs_flag
            flag_similar = 0.65
            flag_dict = self.herbs_dict
            flag_path = '../pic/herbs_flag/'
        elif matching_para == "pet_drinks":
            flag = self.pet_drinks_flag
            flag_similar = 0.65
            flag_dict = self.pet_drinks_dict
            flag_path = '../pic/pet_drinks_flag/'
        elif matching_para == "scene":
            flag = self.scene_flag
            flag_similar = 0.85
            flag_dict = self.scene_dict
            flag_path = '../pic/scene_flag/'


        for i in flag:
            try:
                # 获取预设地图场景
                flag_scene = cv2.imread(flag_path+i)
                if flag_scene is None:
                    logging.error(f"无法加载场景图片： {i}")
                    return "未知场景1"
                flag_scene_gray = cv2.cvtColor(flag_scene, cv2.COLOR_BGR2GRAY)
                # 在大图片中查找小图片
                result = cv2.matchTemplate(scene_gray, flag_scene_gray, cv2.TM_CCOEFF_NORMED)
                # 筛选结果
                locations = np.where(result >= flag_similar)
                # 用 np 筛选一下结果高于 0.85的
                # print(locations)

                locations = list(zip(*locations[::-1]))
                # print('1',locations)
                # 将结果再次处理一下，仅保留坐标值
                if len(locations) > 0:
                    return (locations[0][0],locations[0][1])
                # return (0,0)
            except Exception as e:
                logging.error(f"处理场景时发生异常： {e}")
                return "未知物品坐标"
        return (0,0)
    def get_prop_location(self, left, top, width, height,matching_para):
        area = {"left": left, "top": top, "width": width, "height": height}
        with mss.mss() as sct:
            # scene = '未知'
            location = (0,0)
            #获取大图片
            area_capture = sct.grab(area)#对屏幕 进行截图
            area_capture = np.array(area_capture)#调用 numpy 库将 mss 库的截屏转换一下,并赋值为变量 quyujieping
            screen_gray = cv2.cvtColor(area_capture,cv2.COLOR_BGR2GRAY)

            location = self.matchaing_prop_location(screen_gray,matching_para)
            print(matching_para,'坐标为：')
            return (location[0],location[1])


if __name__ == "__main__":

    a = my_image()
    print(a.get_prop(30, 30, 1000, 800,"herbs"))
    time.sleep(0.1)

    print(a.get_prop_location(30, 30, 1000, 800,"herbs"))
    time.sleep(0.1)







