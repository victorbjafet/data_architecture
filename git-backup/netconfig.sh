#!/bin/sh
sleep 30s
sudo route delete default gw 10.0.0.1 eth0
iptables -t nat -A POSTROUTING -o wlx2887ba8825d6 -j MASQUERADE
iptables -A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i eth0 -o wlx2887ba8825d6 -j ACCEPT
wall packet routing configured
