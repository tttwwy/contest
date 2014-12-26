# coding=utf-8
# created by WangZhe on 2014/12/23
import importlib
import os

def init():
    ENVIRONMENT_VARIABLE = 'CONTEST_SETTINGS_MODULE'
    setting_name = os.environ[ENVIRONMENT_VARIABLE]
    setting = importlib.import_module(setting_name)
    return setting

try:
    setting = importlib.import_module('setting')
except Exception:
    pass





if __name__ == "__main__":
    pass
