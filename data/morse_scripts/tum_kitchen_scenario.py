import subprocess
from morse.builder import *

# basic PR2 robot to the scene
james = BasePR2()
james.add_interface('ros')  #necessary for having correct tf
james.translate(x=2.5, y=3.2, z=0.0)

# keyboard control to the robot
keyboard = Keyboard()
keyboard.name = 'keyboard_control'
james.append(keyboard)

# adding odometry sensor to the robot, with ros interface
odometry = Odometry()
james.append(odometry)
#odometry.add_interface('ros', topic="/odom")
odometry.add_stream('ros')

# laser scanner to the robot, with ros interface
sick = Sick()
sick.translate(x=0.275, z=0.252)
james.append(sick)
sick.properties(Visible_arc = False)
sick.properties(laser_range = 30.0)
sick.properties(resolution = 1.0)
sick.properties(scan_window = 180.0)
sick.create_laser_arc()
#sick.add_interface('ros', topic='/base_scan')
sick.add_stream('ros')

# motion controller to the robot, with ros interface
motion = MotionXYW()
james.append(motion)
motion.add_interface('ros', topic='/cmd_vel')

# adding human model
human = Human()
human.translate(x=6.0, y=0.7, z=0.0)
human.rotate(x=0.0, y=0.0, z=-3.0)
human.properties(WorldCamera = True)

# pose sensor for the human
pose = Pose()
human.append(pose)
pose.add_stream('socket')

# set the environment to tum_kitchen
morse_ros_dir = subprocess.check_output('rospack find morse_ros', shell=True,
                                        stderr=subprocess.STDOUT).decode("utf-8").strip('\n')
env = Environment(morse_ros_dir + "/data/blender_files/tum_kitchen")
#env = Environment('tum_kitchen/tum_kitchen')
env.place_camera([10.0, -10.0, 10.0])
env.aim_camera([1.0470, 0, 0.7854])
