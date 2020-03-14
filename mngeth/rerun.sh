#!/usr/bin/env bash

cd
rm -rf $DDR1 $DDR2 $DDR3 boot.key nohup*
mkdir -p ethData1/keystore
mkdir -p ethData2/keystore
mkdir -p ethData3/keystore
source ~/.bashrc
cp ~/nw3/mngeth/UTC--2020-03-07T23-25-18.301273092Z--67e37abe6fb7bb2b0d61b9c6f53c71623ae65551 ethData1/keystore
cp ~/nw3/mngeth/UTC--2020-03-07T23-27-12.170957487Z--2dec65f7f6fecef9088afed7ab41ad0f1173ddb4 ethData2/keystore
cp ~/nw3/mngeth/UTC--2020-03-07T23-27-53.050585459Z--0213af577d12cf11a5baf5a869e0b1305684ca0a ethData3/keystore
geth init --datadir ethData1 ~/nw3/mngeth/genesis.json
geth init --datadir ethData2 ~/nw3/mngeth/genesis.json
geth init --datadir ethData3 ~/nw3/mngeth/genesis.json
