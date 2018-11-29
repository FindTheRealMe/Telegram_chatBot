#!/bin/sh
. /etc/init.d/functions
service="supervisord"
CMD="/usr/local/bin/supervisord"
proccesscnt=`ps -ef|grep $CMD|grep -v grep|wc -l`
supervisordpid=`ps -ef|grep "/usr/local/bin/supervisord"|grep -v grep|awk '{print $2}'`
#startcmd="$CMD -c /data/home/work/publicNumber/supervisord.conf"
startcmd="$CMD -c /data/home/work/supervisor/supervisord.conf"
stopcmd="kill $supervisordpid"

start_super(){
if  [ $proccesscnt -eq 0 ];then
    $startcmd
    sleep 1
     action "starting $service....." /bin/true || action "starting $service" /bin/false
 else
     echo "$service is running..."
fi 
}

stop_super(){
if  [ $proccesscnt -ne 0 ];then
    $stopcmd
    sleep 1
     action "shutdown $service....." /bin/true ||action "shutdown  $service" /bin/false
 else
    echo "supervisord is already shutdown"
fi
}

USAGE(){
echo "USAGE $0:You must input {start|stop|restart} "
}

case "$1" in
  start)
        start_super
        ;;
  stop)
        stop_super
        ;;
  restart)
        stop_super
        sleep 3
        start_super
        ;;
     *)
       USAGE
esac
