# coding=utf-8
# created by WangZhe on 2014/12/23
import importlib
import os
import sys

def set_config_path(path=''):
    ENVIRONMENT_VARIABLE = 'RECSYS_SETTINGS_MODULE'
    if not path:
        setting_path = os.path.splitext(os.environ[ENVIRONMENT_VARIABLE])[0]
    else:
        setting_path = os.path.splitext(path)[0]

    dirname = os.path.dirname(setting_path)
    basename = os.path.basename(setting_path)
    if not basename:
        basename = 'setting'
    sys.path.insert(0,dirname)
    setting = importlib.import_module(basename)
    return setting

setting = set_config_path()



if __name__ == "__main__":
    pass
