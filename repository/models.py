from django.db import models


# Create your models here.
class Host(models.Model):  # 主机
    hostname = models.CharField(max_length=32, verbose_name="主机名")
    cpu = models.CharField(max_length=32, verbose_name="CPU")
    memory = models.CharField(max_length=32, verbose_name="内存")
    os = models.CharField(max_length=32, default="CentOS", verbose_name="操作系统")
    status = models.BooleanField(default=True, verbose_name="是否在线")
    host = models.ForeignKey(to='AnsibleHost', on_delete=models.CASCADE)


class HostInfo(models.Model):  # 主机详情
    cpu_info = models.CharField(max_length=32, verbose_name="CPU信息")
    kernel = models.CharField(max_length=32, verbose_name="内核名称")
    sn = models.CharField(max_length=128, verbose_name="序列号")
    os_version = models.CharField(max_length=32, verbose_name="操作系统版本")
    host = models.OneToOneField(to='Host', on_delete=models.CASCADE)
    message = models.TextField(max_length=255, null=True, blank=True, verbose_name="备注信息")


class Disk(models.Model):  # 磁盘
    device_name = models.CharField(max_length=32, verbose_name="设备名")
    disk_type = models.CharField(max_length=32, verbose_name="硬盘类型")
    disk_size = models.CharField(max_length=32, verbose_name="硬盘大小")
    host = models.ForeignKey(to='Host', on_delete=models.CASCADE)


class Network(models.Model):  # 网卡
    network_name = models.CharField(max_length=32, verbose_name="网卡名称")
    ipaddr = models.CharField(max_length=32, verbose_name="IP地址")
    netmask = models.CharField(max_length=64, verbose_name="子网掩码")
    network = models.CharField(max_length=32, verbose_name="网络地址")
    mac_addr = models.CharField(max_length=32, verbose_name="MAC地址")
    bandwidth = models.CharField(max_length=32, verbose_name="网卡速率", null=True, blank=True)
    active = models.BooleanField(default=False, verbose_name="是否激活")
    region = models.CharField(max_length=64, null=True, blank=True, verbose_name="机房/地区")
    host = models.ForeignKey(to='Host', on_delete=models.CASCADE)
    message = models.TextField(max_length=255, null=True, blank=True, verbose_name="备注信息")


class CpuMonit(models.Model):  # cpu监控
    # id自增,类型为bigint。设置为主键
    id = models.BigAutoField(primary_key=True)
    # 类型为decimal(10,2)，长度为10，小数点保留2位
    cpu = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="cpu使用率")
    # 类型为datetime
    create_time = models.DateTimeField(verbose_name="创建时间")
    # 由于毫秒的时间戳超过了timestamp的长度，所以只能设置bigint了。
    time_stamp = models.BigIntegerField(verbose_name="毫秒时间戳")
    host = models.ForeignKey(to='Host', on_delete=models.CASCADE)


class MemoryMonit(models.Model):  # 内存监控
    # id自增,类型为bigint。设置为主键
    id = models.BigAutoField(primary_key=True)
    # 类型为int(11)，11是默认长度
    cur_mem = models.IntegerField(verbose_name="当前使用内存")
    mem_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="内存使用率")
    mem_all = models.IntegerField(verbose_name="最大内存")
    # 类型为datetime
    create_time = models.DateTimeField(verbose_name="创建时间")
    # 由于毫秒的时间戳超过了timestamp的长度，所以只能设置bigint了。
    time_stamp = models.BigIntegerField(verbose_name="毫秒时间戳")
    host = models.ForeignKey(to='Host', on_delete=models.CASCADE)


class AnsibleGroup(models.Model):
    name = models.CharField(max_length=32, verbose_name="组名")


class AnsibleHost(models.Model):
    ip = models.CharField(max_length=32, verbose_name="主机名或ip")
    group = models.ForeignKey(to='AnsibleGroup', on_delete=models.CASCADE)
