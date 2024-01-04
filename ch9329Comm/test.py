
import time
import serial
from ch9329Comm import keyboard
from ch9329Comm import mouse

serial.ser = serial.Serial('COM4', 115200)  # 开启串口



# （绝对）鼠标移动到屏幕的左上100*100的位置
dc = mouse.DataComm()
# dc.send_data_absolute(1500,500)
# print('绝对）鼠标移动到屏幕的左上1500*500的位置')

# （相对）鼠标右移100px 下移100px
time.sleep(3)
dc.click()
print('（相对）鼠标右移100px 下移100px')
dc.move_to(-200, -200,'LE')
#拖动后需要加释放鼠标动作

# print('单击')
# time.sleep(1)
# dc.click()
#
#
# print('双击')
# time.sleep(1)
# dc.click_double()

# 校验
# # dc2 = mouse.DataComm()
# dc.move_to(-230,-480)
# print('（相对）鼠标右移230px 下移480px')

# 键盘输出helloworld
# time.sleep(2)
# dc2 = keyboard.DataComm time.sleep(2)()
# # dc2.send_data('FFGGHHIIJJKKLL')  # 按下HELLO
# # dc2.release()  # 松开
# #
# #
# dc2.send_data('\T')  # 按下TBA
# dc2.release()  # 松开
#
# time.sleep(2)
# dc2.send_data('\T','L_ALT')  # 按下L_ALT+TBA
#
# dc2.release()  # 松开

serial.ser.close()  # 关闭串口
