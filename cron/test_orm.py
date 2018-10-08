#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import sys
import subprocess
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录
sys.path.append(BASE_DIR)

if __name__ == "__main__":
    # from AutoCmdb.settings import BASE_DIR
    # print(BASE_DIR)
    # exit()
    # 设置django环境
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoCmdb.settings")
    import django
    django.setup()

    from repository import models

    queryset = models.AnsibleGroup.objects.all()
    print(queryset)
