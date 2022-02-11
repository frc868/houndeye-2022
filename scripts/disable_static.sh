cp /home/pi/dhcpcd/dhcpcd_disabled.conf /etc/dhcpcd.conf
systemctl restart networking
ifconfig eth0 down
ifconfig eth0 up
