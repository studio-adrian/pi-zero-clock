# pi-zero-clock

## setup a new pi
`sudo apt-get update  
`sudo apt-get install python3-pip  
`sudo apt-get install python3-pil  
`sudo apt-get install python3-numpy  

Turn on SPI
`sudo raspi-config  
Choose Interfacing Options -> SPI -> Yes Enable SPI interface

## download this repo
`mkdir sandbox  
`git clone  

## Download libs and test
`git clone https://github.com/waveshare/e-Paper.git  
`cd e-Paper/RaspberryPi_JetsonNano/  
`cd python/examples/  
`python3 epd_4in26_test.py  

## Test run
`cd ~/sandbox/pi-zero-clock/yearclock  
`python2 year.clock.py  

## run on reboot
run as a cron job on pi restart

`crontab -e  
@reboot /usr/bin/python3 /home/adrian/sandbox/pi-zero-clock/yearclock/year.clock.py

## references
https://www.waveshare.com/wiki/4.26inch_e-Paper_HAT
