#!/bin/sh

BACKGROUND_FOLDER=$1

#SETUP CONSTANTS
LOGIN_BACKGROUND_FILE="/Library/Caches/com.apple.desktop.admin.png"
MAX_RANDOM_NUM=32767

#Find all the files in backgrounds folder which are PNG
FILES=($BACKGROUND_FOLDER/*png)
NUM_FILES=${#FILES[@]}
RANDOM_DIVIDER=`expr $MAX_RANDOM_NUM / $NUM_FILES`

#Get a random number via RANDOM cmd
RANDOM_NUM=`expr $RANDOM / $RANDOM_DIVIDER`

echo $NUM_FILES
echo $MAX_RANDOM_NUM
echo $MODULUS_DIVIDER
echo $RANDOM_NUM

echo $RANDOM_FILE

#Select random file
RANDOM_FILE=${FILES[$RANDOM_NUM]}

#Replace/overwrite the file for login background screen
cp $RANDOM_FILE $LOGIN_BACKGROUND_FILE

#(OPTIONAL) Notify the user?
osascript -e 'display notification "'$RANDOM_FILE'" with title "Login Screen Change" sound name "Basso"'
