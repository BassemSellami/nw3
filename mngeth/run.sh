DIR=$(pwd)
chmod 700 prerun.sh
. prerun.sh
cd $DIR
python3 start.py
killall geth