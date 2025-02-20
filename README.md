# pi-zero-clock

# setup a new pi
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy

Turn on SPI
sudo raspi-config
Choose Interfacing Options -> SPI -> Yes Enable SPI interface

# Download libs and test
git clone https://github.com/waveshare/e-Paper.git
cd e-Paper/RaspberryPi_JetsonNano/
cd python/examples/
python3 epd_4in26_test.py

# download this repo


# run on reboot
run as a cron job on pi restart

@reboot /usr/bin/python3 /home/adrian/sandbox/pi-zero-clock/yearclock/year.clock.py
