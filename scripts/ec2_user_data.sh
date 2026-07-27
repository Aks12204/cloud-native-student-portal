#!/bin/bash
yum update -y
yum install httpd -y
systemctl start httpd
systemctl enable httpd
EC2_HOST=$(hostname -f)
echo "<html><body style='font-family:sans-serif; text-align:center; padding-top:50px;'>" > /var/www/html/index.html
echo "<h1>Welcome to Smart Student Portal Backend</h1>" >> /var/www/html/index.html
echo "<p>Handled by EC2 Instance: <strong>$EC2_HOST</strong></p>" >> /var/www/html/index.html
echo "</body></html>" >> /var/www/html/index.html