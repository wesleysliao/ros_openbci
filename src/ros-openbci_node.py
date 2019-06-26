#!/usr/bin/env python

from pyOpenBCI import OpenBCICyton
import rospy
from ros_openbci.msg import eeg_data
from geometry_msgs.msg import Vector3

class openbci:
    def __init__(self):
        self.pub = rospy.Publisher('openbci', eeg_data, queue_size=10)
        rospy.init_node('openbci_node', anonymous=True)
        self.board = OpenBCICyton(port='/dev/ttyUSB0', daisy=False)
        self.board.start_stream(self.print_raw)

    def print_raw(self, sample):
        print(sample.channels_data)
	accelmsg = Vector3(x=sample.aux_data[0], y=sample.aux_data[1], z=sample.aux_data[2])
        eegmsg = eeg_data(id=sample.id,
                          channels_data=sample.channels_data,
                          board_type=sample.board_type,
                          aux_data=accelmsg)
        self.pub.publish(eegmsg)


bci = openbci()

rospy.spin()



