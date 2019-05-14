cd /home/pi/

#updating raspbian
sudo apt-get update -y

#installing pyqt5
sudo apt-get install -y qt5-default pyqt5-dev pyqt5-dev-tools

#installing RTKLIB 2.4.3
cd EasyGNSS/app
mkdir RTKLIB
cd RTKLIB
mkdir 2.4.3
cd 2.4.3
git clone -b rtklib_2.4.3 https://github.com/tomojitakasu/RTKLIB.git
cd RTKLIB/app/str2str/gcc
make
cd ../../rtkrcv/gcc
make
cd ../../convbin/gcc
make

#installing RTKLIB 2.4.2
cd ../../../../..
mkdir 2.4.2
cd 2.4.2 
git clone https://github.com/tomojitakasu/RTKLIB
cd RTKLIB/app/rnx2rtkp/gcc
make

#installing LCD Driver
#cd /home/pi
#wget http://www.waveshare.com/w/upload/0/00/LCD-show-170703.tar.gz
#tar xzvf LCD*.tar.gz
#cd ./LCD-show
#chmod +x LCD4-show
#./LCD4-show
