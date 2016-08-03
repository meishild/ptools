# -*- coding:utf8 -*-

# author          :haiyang.song
# email           :meishild@gmail.com
# datetime        :16/7/24
# version         :1.0
# python_version  :2.7.7
# description     :
# ==============================================================================
import logging
import os
import inspect

logger = logging.getLogger('[PythonService]')

this_file = inspect.getfile(inspect.currentframe())
dirpath = os.path.abspath(os.path.dirname(this_file))
handler = logging.FileHandler(os.path.join(dirpath, "service.log"))

formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.setLevel(logging.INFO)


def get_logger():
    return logger
