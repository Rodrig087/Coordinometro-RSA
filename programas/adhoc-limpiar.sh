#!/bin/bash

sudo ip link set wlan0 down
sudo ip addr flush dev wlan0
sudo ip route flush dev wlan0
sudo ip link set wlan0 up
