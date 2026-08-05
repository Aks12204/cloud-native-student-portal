#!/bin/bash
# Update packages and install Apache HTTP server
yum update -y
yum install -y httpd

# Start and enable Apache service
systemctl start httpd
systemctl enable httpd

# Extract hostname and IP details
EC2_HOST=$(hostname -f)
AVAIL_ZONE=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)

# Create index page
cat <<EOF > /var/www/html/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EC2 Web Server - Student Portal</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .card { background: #1e293b; border-radius: 16px; padding: 40px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); text-align: center; max-width: 600px; width: 90%; border: 1px solid #334155; }
        h1 { color: #38bdf8; margin-top: 0; font-size: 1.8rem; }
        .badge { background: #0284c7; color: white; padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; display: inline-block; margin-bottom: 20px; }
        .info-box { background: #0f172a; padding: 15px; border-radius: 10px; text-align: left; font-family: monospace; font-size: 0.95rem; color: #a5f3fc; border: 1px solid #1e293b; margin-top: 20px; }
        p { color: #94a3b8; line-height: 1.6; }
    </style>
</head>
<body>
    <div class="card">
        <span class="badge">AWS EC2 Compute Tier</span>
        <h1>Cloud Student Portal Backend Instance</h1>
        <p>Auto-scaled compute node active behind Application Load Balancer (ALB).</p>
        <div class="info-box">
            <div><strong>Host Name:</strong> ${EC2_HOST}</div>
            <div><strong>Availability Zone:</strong> ${AVAIL_ZONE:-ap-south-1a}</div>
            <div><strong>Status:</strong> Healthy (200 OK)</div>
        </div>
    </div>
</body>
</html>
EOF

# Health check route
echo "OK" > /var/www/html/health