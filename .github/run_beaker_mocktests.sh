#!/usr/bin/env bash
echo "Hello this is first attempt to run linchpin provisioning in github actions"


VERSION_ID=$(cat /etc/*release | grep ^VERSION_ID | tr -d 'VERSION_ID="')

echo $VERSION_ID

if [ $VERSION_ID = "7" ]
then
    echo "This is centos7";
    export LC_ALL="en_US";
    export LANG="en_US";
fi


linchpin --version;

mkdir /tmp/workspace/;

cd /tmp/workspace/;

echo $PWD;

locale -a;

echo $LC_ALL;
export $LANG;

echo "RUNNING beaker MOCK TESTS";

linchpin init beaker;
cd beaker;
linchpin -vvvv up;
if [ $? -ne 0 ]
then
    echo "Beaker tests failed on linchpin up"
    exit 1
else
    echo "Beaker tests succeed on linchpin up"
fi
linchpin -vvvv destroy;
if [ $? -ne 0 ]
then
    echo "Beaker tests failed on linchpin up"
    exit 1
else
    echo "Beaker tests succeed on linchpin up"
fi
cd ..;
