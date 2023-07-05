#!/bin/bash

tar -zcf ../server-check.tar.gz ../server-check
scp ../server-check.tar.gz lyh102:/home/lyh/code/py/py-util/
ssh lyh102 "rm -rf /home/lyh/code/py/py-util/server-check/; tar -zxf /home/lyh/code/py/py-util/server-check.tar.gz -C /home/lyh/code/py/py-util/;"