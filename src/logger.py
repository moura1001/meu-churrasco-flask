import sys
import logging
import colorlog

mylogger = logging.getLogger("")
mylogger.setLevel(logging.DEBUG)
sh = logging.StreamHandler(sys.stdout)
#formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s", datefmt="%a, %d %b %Y %H:%M:%S")
sh.setFormatter(colorlog.ColoredFormatter("%(log_color)s [%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s", datefmt="%a, %d %b %Y %H:%M:%S"))
mylogger.addHandler(sh)

