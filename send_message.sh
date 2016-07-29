#!/bin/bash
export PATH=/usr/local/bin:$PATH
# to be called minutely
DATE="`date +%Y%m%d`"
TIME="`date +%Y%m%d%H%M%S`"
ROOT_DIR="web"
#ROOT_DIR="`pwd`"
LOG_DIR="$ROOT_DIR/../log/services/$DATE"
mkdir -p $LOG_DIR

LOG="$LOG_DIR/minute_$TIME.log"
echo "called time: $TIME" > $LOG
echo "LOG_DIR=$LOG_DIR"

echo "ROOT_DIR=$ROOT_DIR"
cd $ROOT_DIR
echo "========================================================" >> $LOG


echo ">> calling 'send_message_by_supplier'"
echo "--------------------------------------------------------" >> $LOG
python manage.py send_message_by_supplier

