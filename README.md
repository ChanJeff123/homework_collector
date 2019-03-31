# homework_collector
homework_collector

先安装树莓派3B+的SPI接口支持库
------------------------------

这里的支持库分别是“Py-spidev”和“SPI-Py”，安装“Py-spidev”可以使用命令来安装：

sudo apt-get install python-spidev python3-spidev

这样“Py-spidev”就可以同时支持Python 2和Python 3了。虽然使用“py-spidev”可以驱动Python中的SPI接口，但是项目中我们使用了“SPI-Py”，可以通过以下命令来完成安装“SPI-Py”:

cd ~

git clone https://github.com/lthiery/SPI-Py.git

cd SPI-Py

sudo python setup.py install

sudo python3 setup.py install

同样的“SPI-Py”也可以同时支持Python2和Python3了。

