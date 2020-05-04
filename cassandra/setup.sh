# for developers: enables root ssh on a local VM
# sudo su
# (enter the default password)
# passwd root
# (change the root password)
# vim /etc/ssh/sshd_config
# PermitRootLogin yes
# service sshd restart

install_java() {
  sudo add-apt-repository ppa:openjdk-r/ppa -y
  sudo apt-get update
  sudo apt-get install openjdk-8-jdk -y
}

install_basics() {
  install_java
  sudo apt-get update && sudo apt-get upgrade -y
  sudo apt-get install -y build-essential linux-headers-$(uname -r)
  sudo apt-get install -y make git zip ant python3-pip
}

install_cassandra() {
  cd
  git clone https://github.com/Dariusrussellkish/cassandra.git
  cd cassandra && git checkout bsr && ant build -f ~/nw3/cassandra/build2.xml && git status
}

install_ycsb() {
  cd
  curl -O --location https://github.com/brianfrankcooper/YCSB/releases/download/0.15.0/ycsb-0.15.0.tar.gz
  tar xfvz ycsb-0.15.0.tar.gz
  rm -rf ycsb-0.15.0.tar.gz
}

install_mininet() {
  cd
  mkdir mininet
  cd mininet
  git clone git://github.com/mininet/mininet
  cd mininet
  git checkout -b 2.2.2
  cd ..
  mininet/util/install.sh -a
  sudo mn --test pingall
}

#install_basics
#install_ycsb
install_mininet
#install_cassandra