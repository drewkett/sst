#!/bin/sh

echo "Testing http://www.google.com http code"
code=`curl -s -o /dev/null -I -w "%{http_code}" http://www.google.com`
if [ $code -ne "200" ]; then
	echo "google.com http code != 200"
fi
