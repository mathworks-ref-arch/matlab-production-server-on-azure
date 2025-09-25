#! /bin/bash
#Put your extra commands here
LOG_DIR=/var/log/custom_script
LOG_FILE=$LOG_DIR/custom_script.log

# Create log directory and file
sudo mkdir -p $LOG_DIR
sudo touch $LOG_FILE
sudo chmod 666 $LOG_FILE

# Update package lists and log errors
sudo apt-get update 2>> $LOG_FILE
if [ $? -ne 0 ]; then
  echo "apt update failed. Check the log file at $LOG_FILE" | tee -a $LOG_FILE
fi

# Install openssh-server and log errors
sudo apt-get install -y openssh-server 2>> $LOG_FILE
if [ $? -ne 0 ]; then
  echo "apt install failed. Check the log file at $LOG_FILE" | tee -a $LOG_FILE
fi

ls