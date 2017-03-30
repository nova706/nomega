#!/usr/bin/env bash

function start_server
{
    echo "Starting Node processes"
    npm start

}   # end of start_server

function stop_server
{
    echo "Stopping Node processes"
    npm stop

}   # end of stop_server

if [ "$1" = "start" ]
then
    start_server
elif [ "$1" = "stop" ]
then
    stop_server
fi