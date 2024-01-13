

import sys
import time

# 导入截屏模块
import mss
import cv2
import numpy as np #numpy 库,简单理解为将图片转换成数组的库,因为 opencv 无法直接处理 mss 的截图,需要用 numpy 转换成数组
import re
import logging
# 设置日志基本配置

def screen_whole_capture(self, name):
    """
    截取整个屏幕的图像，并将其保存为指定的图片文件。

    参数：
    name (str): 保存的图片文件的名称，不包括文件扩展名。

    返回：
    None

    异常：
    抛出 IOError 如果截图或文件保存失败。
    抛出 Exception 如果 mss 模块不可用或存在其他问题。
    """

    # 实例化 mss 对象，并重名为 sct，固定写法，记着就行
    with self.sct as sct:
        # 定义输出文件的路径，包括图像的扩展名 .png
        output_path = f'../pic/{name}.png'
        # shot 方法表示截屏，output 参数表示存放的文件名
        try:
            sct.shot(output=output_path)
            logging.info(f"全屏幕截图已保存为 {output_path}")
        except IOError as e:
            # 处理文件 I/O 错误
            logging.error(f"截图或文件保存失败： {e}")
            raise
        except Exception as e:
            # 处理其他可能的异常
            logging.error(f"发生错误： {e}")
            raise


def screen_area_capture(name, left, top, width, height):
    """
    截取屏幕指定区域的图像，并将其保存为指定的图片文件。
    参数：
    name (str): 保存的图片文件的名称，不包括文件扩展名。
    left (int): 截取区域的左上角 X 坐标。
    top (int): 截取区域的左上角 Y 坐标。
    width (int): 截取区域的宽度。
    height (int): 截取区域的高度。
    返回：
    None
    异常：
    抛出 IOError 如果截图或文件保存失败。
    抛出 Exception 如果 mss 模块不可用或存在其他问题。
    """
    area = {"left": left, "top": top, "width": width, "height": height}
    try:
        # 实例化 mss 对象,并重名为 sct,固定写法,记着就行
        with mss.mss() as sct:
            # 使用 sct 的 grab 方法截取屏幕中某个区域的画面
            screenshot = sct.grab(area)
            output_path = f'../pic/{name}.png'
            # 利用 mss.tools 模块的 to_png 方法,保存截图文件
            mss.tools.to_png(screenshot.rgb, screenshot.size,
                             output=output_path)
            logging.info(f"屏幕区域截图已保存为 {output_path}")
    except IOError as e:
        # 处理IO错误，例如文件无法保存
        logging.error(f"区域截图或文件保存失败： {e}")
        raise
    except Exception as e:
        # 处理其他可能的错误，例如mss模块不可用
        logging.error(f"发生错误： {e}")
        raise


def screen_area_display(self, left, top, width, height):
    """
    显示屏幕指定区域的截图,不保存到本地
    参数：
    left (int): 截取区域的左上角 X 坐标。
    top (int): 截取区域的左上角 Y 坐标。
    width (int): 截取区域的宽度。
    height (int): 截取区域的高度。
    返回：
    None
    异常：
    抛出 IOError 如果截图或显示图片时发生IO错误。
    抛出 Exception 如果 mss 模块不可用或存在其他问题。
    """
    area = {"left": left, "top": top, "width": width, "height": height}
    try:
        # 实例化 mss 对象,并重名为 sct,固定写法,记着就行
        with self.sct as sct:
            # 使用 sct 的 grab 方法截取屏幕中某个区域的画面
            screenshot = sct.grab(area)
        screenshot = np.array(screenshot)
        cv2.imshow("dnf", screenshot)  # 调用 opencv 的 imshow 方法显示图片
        logging.info(f"从坐标({left}, {top})截取长{width}宽{height}的区域")
        cv2.waitKey(0)  # 等待按键，然后关闭窗口, 如果没有这行,图片打开后直接退出
        cv2.destroyAllWindows()  # 关闭所有 opencv 窗口

    except IOError as e:
        logging.error(f"截图或显示图片时发生IO错误： {e}")
        # 这里可以添加更多的错误处理逻辑，例如重试或退出函数
        raise
    except Exception as e:
        logging.error(f"发生意外的错误： {e}")
        # 这里可以添加更多的错误处理逻辑，例如重试或退出函数
        raise


def screen_continuous_display(self, left, top, width, height):
    """
    持续显示屏幕指定区域的截图。
    参数：
    left: 区域的左边坐标
    top: 区域的上边坐标
    width: 区域的宽度
    height: 区域的高度
    """
    area = {"left": left, "top": top, "width": width, "height": height}

    try:
        # 实例化 mss 对象，并重名为 sct，固定写法，记着就行
        with self.sct as sct:
            while True:
                try:
                    # 捕获屏幕指定区域的截图
                    screenshot = sct.grab(area)
                    # 将截图转换为numpy数组
                    screenshot = np.array(screenshot)
                    # 显示截图
                    cv2.imshow("dnf", screenshot)
                    # 如果在5毫秒内按下'q'键，则退出循环
                    if cv2.waitKey(5) & 0xFF == ord("q"):
                        cv2.destroyAllWindows()
                        logging.info(f"退出视频流")
                        break
                except Exception as e:  # 捕获可能发生的任何异常
                    logging.error(f"发生异常： {e}")
                    cv2.destroyAllWindows()
                    break
    except Exception as e:  # 捕获可能发生的任何异常
        logging.error(f"发生异常： {e}")


def matching_scene(self, scene_gray):
    """
    匹配场景函数。
    参数：
    scene_gray：灰度化的场景图片，用于与预设的场景图片进行匹配。
    matching_param：匹配参数，用于指定使用哪种场景字典和路径进行匹配。
                    默认None为场景识别，"prop"为道具识别
    返回：
    返回匹配到的场景名称，如果匹配失败则返回"未知场景"。
    """

    flag = self.scene_flag
    flag_path = '../pic/scene_flag/'

    for i in flag:
        try:
            # 获取预设地图场景
            flag_scene = cv2.imread(flag_path + i)
            if flag_scene is None:
                logging.error(f"无法加载场景图片： {i}")
                return "未知场景"
            flag_scene_gray = cv2.cvtColor(flag_scene, cv2.COLOR_BGR2GRAY)
            # 在大图片中查找小图片
            result = cv2.matchTemplate(scene_gray, flag_scene_gray, cv2.TM_CCOEFF_NORMED)
            # 筛选结果
            locations = np.where(result >= 0.85)
            # 用 np 筛选一下结果高于 0.85的

            locations = list(zip(*locations[::-1]))
            # 将结果再次处理一下，仅保留坐标值
            if len(locations) > 0:
                match = re.match(r'(\d+)', i)
                if match:
                    scene_number = match.group(1)
                    # 根据匹配到的场景编号返回对应场景名称
                    return self.scene_dict.get(scene_number, "未知场景")
                else:
                    return None
        except Exception as e:
            logging.error(f"处理场景时发生异常： {e}")
            return "未知场景"
    return "未知场景"


# bug 黄泥岗识别成星秀村，应天府西识别成应天府
def get_scene(self, left, top, width, height):
    area = {"left": left, "top": top, "width": width, "height": height}
    with mss.mss() as sct:
        scene = '未知'
        # role_location = (0,0)
        # 获取大图片
        area_capture = sct.grab(area)  # 对屏幕 进行截图
        area_capture = np.array(area_capture)  # 调用 numpy 库将 mss 库的截屏转换一下,并赋值为变量 quyujieping
        screen_gray = cv2.cvtColor(area_capture, cv2.COLOR_BGR2GRAY)

        # 判断场景
        scene = self.matching_scene(screen_gray)
        print('当前画面在:', scene)

        if scene is not None:
            return scene
        else:
            return "未知地图"

        # cv2.imshow("DNF", area_capture)  # 调用 opencv 的 imshow 方法显示图片
        # if cv2.waitKey(5) & 0xFF == ord("q"):
        #     cv2.destroyAllWindows()
        #     break

if __name__ == "__main__":

    time.sleep(2)
    screen_area_capture("框1",152,370,1353,588)


