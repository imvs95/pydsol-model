"""
Created on: 25-6-2021 14:43

@author: IvS
"""
import logging
import sys

__all__ = ["get_module_logger"]

def get_module_logger(mod_name, level=logging.INFO):
    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler(stream=sys.stdout)
    msg_format = '%(asctime)s [%(levelname)s] %(message)s (%(name)s - %(filename)s: line %(lineno)s)'
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(fmt=msg_format, datefmt=date_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    return logger
