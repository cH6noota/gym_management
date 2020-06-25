from classes import Sesame
import time
import sys
args = sys.argv

time.sleep(30)
Sesame( args[1] ).lock()
