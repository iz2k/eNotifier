#!/bin/bash

function update_apt() {
  echo ">> Update APT"
  sudo apt-get update
}

function install_mariaDb() {
  echo ">> Install DB:"
  echo " -> Install Maria DB"
  sudo apt-get -y install mariadb-server
  echo " -> Create DB user"
cat <<EOF | sudo mysql -u root | grep donotshowanythinginbash
CREATE USER pi;
GRANT ALL PRIVILEGES ON *.* TO 'pi'@'%' IDENTIFIED BY 'raspberry' WITH GRANT OPTION;
EOF

echo " -> Open DB to remote connections"
sudo sed -i '/bind-address            = 127.0.0.1/c\bind-address            = 0.0.0.0' /etc/mysql/mariadb.conf.d/50-server.cnf

}

function install_webserver() {
  echo ">> Install WebServer:"
  echo " -> Install Apache"
  sudo apt-get -y install apache2
  echo " -> Enable rewrite module."
  sudo a2enmod rewrite
  echo " -> Disable default VirtualHost."
  sudo a2dissite 000-default.conf
  echo " -> Configure eNotifierFrontend site on Apache"
cat <<EOF | sudo tee /etc/apache2/sites-available/eNotifierFrontend-apache.conf | grep donotshowanythinginbash
<VirtualHost *:80>
		ServerAdmin webmaster@localhost
		DocumentRoot /usr/share/iz2k/eNotifierFrontend/public

		RewriteEngine On
		# If an existing asset or directory is requested go to it as it is
		RewriteCond %{DOCUMENT_ROOT}%{REQUEST_URI} -f [OR]
		RewriteCond %{DOCUMENT_ROOT}%{REQUEST_URI} -d
		RewriteRule ^ - [L]
		# If the requested resource doesn't exist, use index.html
		RewriteRule ^ /index.html

		ErrorLog ${APACHE_LOG_DIR}/error.log
		CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
EOF

  echo " -> Enable eNotifierFrontend VirtualHost."
  sudo a2ensite eNotifierFrontend-apache.conf
  echo " -> Restart Apache."
  sudo service apache2 restart
}

function install_tools() {
  echo ">> Install Tools:"
  echo " -> Install i2c tools"
  sudo apt-get -y install i2c-tools
  echo " -> Install system tools"
  sudo apt-get -y install mmv unzip
  echo " -> Install development tools"
  sudo apt-get -y install patch xsltproc gcc libreadline-dev python3-venv python3-pip python3-pil libopenjp2-7
}

function setup_hw() {
  echo " -> Enable I2C HW."
  sudo raspi-config nonint do_i2c 0

  echo " -> Enable SPI HW."
  sudo raspi-config nonint do_spi 0
}

function setup_hostname() {
  echo ">> Setup Hostname:"
  hostname=$1
  echo " -> Change hostname to: "$hostname
  sudo raspi-config nonint do_hostname $hostname

}

function setup_swap() {
  echo ">> Increase SWAP:"
  echo " -> Stop SWAP."
  sudo dphys-swapfile swapoff

  echo " -> Modify SWAP size in configuration file"
  sudo sed -i '/CONF_SWAPSIZE=100/c\CONF_SWAPSIZE=1024' /etc/dphys-swapfile

  echo " -> Regenerate SWAP."
  sudo dphys-swapfile setup

  echo " -> Restart SWAP."
  sudo dphys-swapfile swapon
}

function install_component() {
  component=$1
  echo ">> Install $component:"
  echo " -> Extract installer"
  unzip $component -d tmp
  cd tmp
  echo " -> Execute installer"
  source install.sh
  echo " -> Clean up"
  cd ..
  rm -rf tmp
}


#### SCRIPT EXECUTION STARTS HERE ####
echo "*********************************************"
echo "**** eNotifier SYSTEM BAREBONE INSTALLER ****"
echo "*********************************************"
echo "** This script will convert a clean image  **"
echo "** of Raspberry Pi OS Lite to a working    **"
echo "** eNotifier System. This includes setting **"
echo "** up hardware, firmware and software      **"
echo "** components.                             **"
echo "*********************************************"
echo "*********************************************"
echo "** The install is automated. All options   **"
echo "** needed for the process are requested    **"
echo "** in the beggining. A reboot is needed    **"
echo "** to finalize the process.                **"
echo "*********************************************"

read -p "Hostname will be changed in the end of the process. Select new hostname: " hostname  <&1

update_apt
install_mariaDb
install_webserver
install_tools
setup_hw
setup_swap
install_component eNotifierBackend_1.0.zip
install_component eNotifierFrontend_1.0.zip
setup_hostname $hostname

echo "********************************************"
echo "**** EXECUTOR SYSTEM BAREBONE INSTALLED ****"
echo "********************************************"
read -n1 -p "Do you want to reboot now? (y/N)" doit  <&1
echo ""
case $doit in
	y|Y) sudo reboot ;;
	*) echo "Manual system reboot required" ;;
esac