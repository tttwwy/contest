# coding=utf-8
# created by WangZhe on 2014/12/23
import importlib
import os
import sys
print sys.path
ENVIRONMENT_VARIABLE = 'CONTEST_SETTINGS_MODULE'
setting_name = os.environ[ENVIRONMENT_VARIABLE]

print setting_name
setting = importlib.import_module(setting_name)

if __name__ == "__main__":
    pass
