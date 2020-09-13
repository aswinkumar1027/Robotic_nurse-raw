import tornado.ioloop
import tornado.web
import datetime
import gpiozero
import time
import serial
import RPi.GPIO as GPIO
import os
import fetch_data


robot = gpiozero.Robot(left=(11,25), right=(9,10))

leftend = gpiozero.DigitalInputDevice(17)
center = gpiozero.DigitalInputDevice(27)
rightend = gpiozero.DigitalInputDevice(22)
leftback = gpiozero.DigitalInputDevice(23)
rightback = gpiozero.DigitalInputDevice(19)

GPIO.setmode(GPIO.BCM)
GPIO.setup(6,GPIO.OUT) #temperature
GPIO.setup(5,GPIO.OUT) #pressure
GPIO.setup(26,GPIO.OUT) #spo2

GPIO.output(5,1)
GPIO.output(6,1)
GPIO.output(26,1)


rfid_dict ={'86EAF922\r\n': 'C47', '751F1120\r\n': 'C5', '75C27820\r\n': 'C8', '859C6120\r\n': 'C65', '75507F20\r\n': 'C59', '76353724\r\n': 'C21', '86257922\r\n': 'C34', '76B67222\r\n': 'C29', '66CB9524\r\n': 'C22', '96533322\r\n': 'C50', '8577D620\r\n': 'C58', '75847F20\r\n': 'C64', '8546FD20\r\n': 'C4', '767A4724\r\n': 'C24', '85159720\r\n': 'C57', '86BAFD22\r\n': 'C2', '858A0320\r\n': 'C32', '8504A820\r\n': 'C31', '757BA620\r\n': 'C35', '7586DF20\r\n': 'C56', '75AA0720\r\n': 'C3', '85B27D20\r\n': 'C38', '962C5922\r\n': 'C53', '85430420\r\n': 'C17', '86DD7822\r\n': 'C41', '753AF620\r\n': 'C6', '75F5F220\r\n': 'C9', '9623AD22\r\n': 'C46', '855BCB20\r\n': 'C39', '75C5D520\r\n': 'C42', '8676F722\r\n': 'C1', '8666DE22\r\n': 'C40', '85838F20\r\n': 'C60', '75172B20\r\n': 'C10', '8591E120\r\n': 'C45', '75B91320\r\n': 'C51', '76743A24\r\n': 'C23', '75F79320\r\n': 'C16', '7564E520\r\n': 'C27', '755AD520\r\n': 'C26', '85971B20\r\n': 'C66', '76F73022\r\n': 'C7', '75EEA420\r\n': 'C25', '85839620\r\n': 'C48', '757EBC20\r\n': 'C52', '8548EF20\r\n': 'C18', '960E0122\r\n': 'C49', '75ABA620\r\n': 'C19', '86FD7122\r\n': 'C36', '867DC122\r\n': 'C28', '8552FE20\r\n': 'C62', '8556A120\r\n': 'C15', '665FA624\r\n': 'C20', '754D2220\r\n': 'C54', '75AB3420\r\n': 'C44', '75A1F220\r\n': 'C43', '76F21722\r\n': 'C11', '868D1822\r\n': 'C13', '75942320\r\n': 'C14', '86E8FB22\r\n': 'C55', '75A9AD20\r\n': 'C12', '756B0F20\r\n': 'C37', '759B0D20\r\n': 'C30', '851C0020\r\n': 'C63', '8561A620\r\n': 'C33', '75817520\r\n': 'C61'}
active_beds = [ ]                                #fetch from main server
left_beds = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C37', 'C38', 'C39', 'C40', 'C41', 'C42', 'C49', 'C50', 'C51', 'C52', 'C53', 'C54', 'C61', 'C62', 'C63', 'C64', 'C65', 'C66']

active_beds_temp = fetch_data.get_active_bed_data()
print(active_beds_temp)
active_beds = active_beds_temp.get('beds')
print(active_beds)

ser=serial.Serial("/dev/ttyACM0",19200,timeout=0.8)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate = 19200


turn_left = False
line_follow_mode = False


def line_follow_config(fn):
    leftend.when_activated = fn
    rightend.when_activated = fn
    center.when_activated = fn
    leftback.when_activated = fn
    rightback.when_activated = fn


    leftend.when_deactivated = fn
    rightend.when_deactivated = fn
    center.when_deactivated = fn
    leftback.when_deactivated = fn
    rightback.when_deactivated = fn


def stop_line_follow():
    global line_follow_mode
    line_follow_mode = False

def active_fetch():
    active_beds_temp = fetch_data.get_active_bed_data()
    print(active_beds_temp)
    active_beds = active_beds_temp.get('beds')
    print(active_beds)


def rfid_read():
    global turn_left                                   #rfid taking and decisions
    print("RFID_READ")
    bed = rfid_dict[rfid_cpy]
    
    if (bed in active_beds):
        print("Active beds are detected")
        turn_left = bed in left_beds
        robot.stop()
        time.sleep(0.8)
        print("makin a turn for interaction")
        turn_robot()
    else:
        print("not in active beds list")
        print("not active_bed")
        # So that robot automatically moves on to next bed
        robot.forward()
        time.sleep(1)
        line_follow()

        
def turn_robot():

    robot.forward()
    time.sleep(0.3)
    if turn_left:                                  #interaction left turning
        print("turning_left")
        robot.left()
    else:
        print("turning_right")
        robot.right()
    time.sleep(1)
    robot.stop()
    robot.forward()
    time.sleep(0.3)
    robot.stop()
    print("turn is here")



def mod_turn_robot():
    robot.forward()
    time.sleep(0.1)
    if turn_left:                                  #interaction left turning
        print("turning_left")
        robot.left()
    else:
        print("turning_right")
        robot.right()
    print("turn is here")
    time.sleep(0.8)
    while True:
        if center.is_active:
           print("center_active")
           time.sleep(0.2)
           print("time_implemented")   #implement timne delay
           robot.stop()
           print("robot_stopped")
           break
    line_follow()




def rfid():
    global rfid_cpy
    ser.flushInput() # flushing out old data
    read_ser=ser.readline()
    print (read_ser)
    rfid_cpy = read_ser
    if read_ser in rfid_dict:
        stop_robot()
        print("detected and stopping robot")
        rfid_read()
    #else:
        #line_follow()


def check():
    

    if not line_follow_mode:
        return

    print(center.is_active , leftend.is_active , rightend.is_active)
    
    

    if center.is_active and rightend.is_active and leftend.is_active:
        print("cross_near")
        robot.forward()
        rfid()
        #return

    elif center.is_active and (not leftend.is_active) and (not rightend.is_active):
        print("forward")
        robot.forward()

    elif (not leftend.is_active) and rightend.is_active:
        robot.right()
        print("right")

    elif leftend.is_active and (not rightend.is_active):
        robot.left()
        print("left")
    
    elif (not leftend.is_active) and (not rightend.is_active) and (not center.is_active):
        stop_robot



def line_follow():
    print("line_follow")

    global line_follow_mode
    line_follow_mode = True
    check()
    line_follow_config(check)

def examine():
    global turn_left                                        #examination_finish and continue
    turn_left = not turn_left
    mod_turn_robot()


def stop_robot():
    robot.stop()
    stop_line_follow()


def take_pressure():                                      #pressure taking button
    GPIO.output(5,0)
    time.sleep(0.1)
    GPIO.output(5,1)

def take_temp():
    GPIO.output(6,0)
    time.sleep(0.4)
    GPIO.output(6,1)

def spox():
    GPIO.output(26,0)
    time.sleep(0.5)
    GPIO.output(26,1)
    

def fwd():
    robot.forward()

robo_actions = {
    "forward": fwd,
    "backward": robot.backward,
    "left": robot.left,
    "right": robot.right,
    "stop": stop_robot,
    "line": line_follow,
    "examine": examine,
    "take_pressure": take_pressure,
    "take_temp": take_temp,
    "spox": spox,
    "active_fetch": active_fetch
}


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html", bed_id = bed )

class CommandHandler(tornado.web.RequestHandler):
    def post(self):
        movement = self.get_body_argument("movement")
        robo_actions[movement]()
        self.write("You wrote " + movement)

settings = dict(
	template_path = os.path.join(os.path.dirname(__file__), "templates"),
	static_path = os.path.join(os.path.dirname(__file__), "static")
	)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/move", CommandHandler),
    ], **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
