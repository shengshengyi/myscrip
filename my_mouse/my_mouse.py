import pyautogui
import random
import math
import time

class Mouse:

    def __init__(self):
        # 初始化鼠标位置
        self.position = (1, 1)
        # 设置 pyautogui 的 FAILSAFE 和 PAUSE 参数
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.05

    import math
    import pyautogui
    import time

    def move(self, x, y, steps=10):
        try:
            # 获取鼠标当前位置
            x_pos, y_pos = self.get_position()

            # 计算目标位置与当前位置之间的水平距离
            dx = x - x_pos
            # 计算目标位置与当前位置之间的垂直距离
            dy = y - y_pos

            # 计算每次移动的步长
            step_size = math.sqrt(dx ** 2 + dy ** 2) / steps

            # 逐步移动鼠标
            for _ in range(steps):
                # 更新鼠标位置
                x_pos += dx / steps
                y_pos += dy / steps
                x_pos += random.uniform(-0.5, 0.5)
                y_pos += random.uniform(-0.5, 0.5)
                pyautogui.moveTo(x_pos, y_pos,0.01)
                self.position = (x_pos, y_pos)

        except Exception as e:
            print(f"Error moving mouse: {e}")

    def get_position(self):
        # 获取鼠标当前位置
        return self.position

    def set_position(self, x, y):
        # 设置鼠标位置
        self.move(x, y)

    def click(self, button='left'):
        try:
            # 模拟鼠标点击
            # 添加随机数以模拟更自然的点击
            x, y = self.get_position()
            x += random.uniform(-5, 5)
            y += random.uniform(-5, 5)
            pyautogui.click(x, y, button=button)
        except Exception as e:
            print(f"Error clicking mouse: {e}")

    def click_double(self, button='left',interval=0.2):
        try:
            # 模拟鼠标点击
            # 添加随机数以模拟更自然的点击
            x, y = self.get_position()
            x += random.uniform(-5, 5)
            y += random.uniform(-5, 5)
            pyautogui.doubleClick(x, y, button=button,interval=interval )
        except Exception as e:
            print(f"Error clicking mouse: {e}")


    def scroll(self, units, x, y):
        try:
            # 模拟鼠标滚轮滚动
            pyautogui.scroll(units, x, y)
        except Exception as e:
            print(f"Error scrolling mouse: {e}")


if __name__ == '__main__':

    # Usage
    mouse = Mouse()
    a=[500,400]
    b=[500,500]

    mouse.move(a[0],a[1],10)
    print('抵达a{}，{}'.format(a[0], a[1]))

    time.sleep(3)


    mouse.move(b[0],b[1],10)
    print('抵达b{}，{}'.format(b[0], b[1]))

    mouse.click_double()

    mouse.__init__()
    print(mouse.position)
