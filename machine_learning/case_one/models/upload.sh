#!/bin/bash

# ==== Configuration ====
LOCAL_DIR="/home/yrd/documents/git_clone_code/code/learning_project/machine_learning/case_one/"           
REMOTE_USER="root"
REMOTE_HOST="region-46.seetacloud.com"
REMOTE_PORT="49306"
REMOTE_DIR="/root/autodl-tmp"               # Default temp folder on AutoDL

# ==== Upload with rsync ====
echo "Uploading $LOCAL_DIR to $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR ..."

rsync -avz --progress \
  -e "ssh -p $REMOTE_PORT" \
  "$LOCAL_DIR/" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR"

echo "✅ Upload complete!"

