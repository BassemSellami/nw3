install_java() {
    sudo add-apt-repository ppa:openjdk-r/ppa -y
    sudo apt-get update
    sudo apt-get install openjdk-8-jdk -y
}

install_basics() {
    sudo apt-get update && sudo apt-get upgrade -y
    sudo apt-get install -y build-essential linux-headers-$(uname -r)
    sudo apt-get install -y make git zip ant

}

install_cass() {
    cd
    git clone https://github.com/ZezhiWang/cassandra.git
#    cd cassandra && git checkout abdOpt && ant build && git status
    cd cassandra && git checkout abdOpt
#    cd
}

install_java
install_basics
#install_cass