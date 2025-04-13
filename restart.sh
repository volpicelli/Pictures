systemctl stop pictures
pkill pictures
systemctl daemon-reload
systemctl start pictures
systemctl restart nginx
