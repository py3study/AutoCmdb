#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
无密码登录目标主机
第一步:收集主机公钥，写入known_hosts,避免出现Are you sure you want to continue connecting (yes/no)?
    使用命令： ssh-keyscan
第一步:把本地主机的公钥复制到远程主机的authorized_keys文件上
    #先确保本机已经执行了ssh-keygen
    再使用命令： ssh-copy-id
"""
import os
import time
import subprocess
from api.utils.response import BaseResponse

class LoginLinux(object):
    def __init__(self,host,port,version,user,pwd):
        self.host = host
        self.port = port
        self.version = version
        self.user = user
        self.pwd = pwd
        self.res = BaseResponse()

    def execute_linux(self,cmd,timeout=1,skip=False):
        """
        执行linux命令
        :param cmd: linux命令
        :param timeout: 超时时间
        :param skip: 是否跳过超时
        :return:
        """
        p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
        # print(p)
        # timeout = 1  # 超时时间
        t_beginning = time.time()  # 开始时间
        seconds_passed = 0  # 执行时间
        while True:
            if p.poll() is not None:
                break
            seconds_passed = time.time() - t_beginning
            if timeout and seconds_passed > timeout:
                p.terminate()
                # raise TimeoutError(cmd, timeout)
                if not skip:
                    self.res.code = 500
                    self.res.error = '命令: {},执行超时!'.format(cmd)
                    return self.res.__dict__

        result = p.stdout.read().decode('utf-8').strip()  # 命令运行结果
        # print(result)
        self.res.data = result
        return self.res.__dict__

    def has_id_rsa(self):
        # 判断本机的id_rsa是否存在
        ret = self.execute_linux('ls ~/.ssh/id_rsa')
        if "ls:" in ret.get('data'):  # 判断结果是否含有"ls:"
            # print('no')
            # 文件不存在时,生成rsa证书
            # 无交互生成ssh rsa免秘证书
            # 注意:必须要指定-f参数才行,否则会有交互提示
            cmd = "ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa"
            # print(cmd)
            ret1 = self.execute_linux(cmd)
            # print(res)
            if "fingerprint" not in ret1.get("data"):  # 判断结果不包含指纹时
                self.res.code = 500
                self.res.error = '命令: {},执行失败!'.format(cmd)
                return self.res.__dict__

        return self.res.__dict__


    def keyscan(self):  # 收集主机公钥
        has_res = self.has_id_rsa()
        if has_res.get('error'):  # 判断是否包含错误
            return has_res

        if self.version == '6':
            # 收集主机公钥，写入known_hosts,避免出现Are you sure you want to continue connecting (yes/no)?
            # centos 6.x必须使用rsa
            cmd = "ssh-keyscan -H -t rsa -p {} {} >> ~/.ssh/known_hosts".format(self.port,self.host)
        else:
            cmd = "ssh-keyscan -H -t ecdsa -p {} {} >> ~/.ssh/known_hosts".format(self.port,self.host)

        ret = self.execute_linux(cmd)
        # print(ret)
        # 判断执行结果
        if "no hostkey" in ret.get('data'):
            self.res.code = 500
            self.res.error = "无效的主机秘钥,请确认密码或者系统是否正确"
            return self.res.__dict__

        return self.res.__dict__

    def copy_id(self):  # 复制公钥到远程主机
        key_res = self.keyscan()
        if key_res.get('error'):  # 判断是否包含错误
            return key_res

        # 由于ssh-copy-id无法指定密码参数,必须手动输入密码才行
        # 这里使用expect来完成输入密码的过程
        # 要先安装expect
        # yum install -y expect
        # 判断是否安装
        "rpm -qa | grep expect"
        has_yum = self.execute_linux("rpm -qa | grep expect",2)

        if not has_yum.get("data"):
            # 安装expect
            yum = self.execute_linux("yum install -y expect",10)
            # print(yum,"安装了yum")
            if "完毕" not in yum.get("data"):
                self.res.code = 500
                self.res.error = "安装expect失败!"
                return self.res.__dict__

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录
        # print(BASE_DIR)
        shell_file = os.path.join(BASE_DIR,'ansible','remotExect.sh')
        cmd = "expect {} {} {} {} {}".format(shell_file,self.port,self.user,self.pwd,self.host)
        # expect remotExect.sh 22 root 123456 192.168.142.131
        # print(cmd)
        # 此命令必须执行2次才能成功,第一次必然失败,需要跳过超时报错
        self.execute_linux(cmd,3,True)
        # 第二次就ok了!
        ret = self.execute_linux(cmd,5)

        if "Permission" in ret.get("data"):
            self.res.code = 500
            self.res.error = "执行remotExect.sh失败!用户名和密码错误"
            return self.res.__dict__

        return self.res.__dict__




