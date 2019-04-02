# homework_collector

本项目适用于MFRC522模块基于树莓派的读写操作，实现学生作业提交记录

先安装树莓派3B+的SPI接口支持库
------------------------------
事前update树莓派的库
>sudo apt-get update && sudo apt-get upgrade

这里的支持库分别是“Py-spidev”和“SPI-Py”，安装“Py-spidev”可以使用命令来安装：
>sudo apt-get install python-spidev  
>python3-spidev

这样“Py-spidev”就可以同时支持Python 2和Python 3了。虽然使用“py-spidev”可以驱动Python中的SPI接口，但是项目中我们使用了“SPI-Py”，可以通过以下命令来完成安装“SPI-Py”:
>cd ~  
>git clone https://github.com/lthiery/SPI-Py.git  
>cd SPI-Py  
>sudo python setup.py install  
>sudo python3 setup.py install

同样的“SPI-Py”也可以同时支持Python2和Python3了。

硬件接线图
----
看下树莓派引脚功能
>gpio readall
![raspi](https://cdn.raspberrytips.nl/wp-content/uploads/2016/08/RFID-RC522-raspberry-pi-3-600x301.png)

实现过程
----
>git clone https://github.com/ChanJeff123/homework_collector.git

代码下载后放在同一个目录下不然需要改import路径  
对每个芯片卡写处理:
>sudo python ezWrite.py

读一下试试，结果是写入的数字
>sudo python ezRead.py
