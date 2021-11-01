# 北工大健身房预约

**注：** 此脚本仅用于学习使用，不可进行不公平预约

## 致谢

致谢舍友前期抓包，直接拿url来使用

舍友用的springboot做的，只能部署在ecs上，花钱的事我是不会干的，所以编写云函数脚本，使用免费的阿里云函数

对于舍友的springboot版本，目前还没上传git，等上传将会在这贴出代码

## 文件说明

1. [order.py](https://github.com/Swenchao/gym_order/blob/main/order.py) : 原始脚本文件，可直接执行进行预约

2. [aliyun.py](https://github.com/Swenchao/gym_order/blob/main/aliyun.py) : 阿里云函数脚本，粘到云函数平台可进行执行学习

## 使用说明

1. 修改文件中个人信息（两种方式都是一样的）

    user_info：个人信息

    gym_time：预约时间

    openId：微信的openId（抓包预约界面，查看自己的是什么）

    server_key：server酱的sendKey，不填收不到通知

2. 执行脚本
