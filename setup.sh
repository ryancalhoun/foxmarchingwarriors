#!/bin/bash

BUCKET=$(dirname $(
  curl -H Metadata-Flavor:Google \
    http://metadata.google.internal/computeMetadata/v1/instance/attributes/startup-script-url)
)
PROJECT=$(curl -H Metadata-Flavor:Google \
  http://metadata.google.internal/computeMetadata/v1/project/project-id)

apt install -y nginx python3.11-venv

gcloud storage cp -R $BUCKET/web/api /var/www/
python3 -m venv /var/www/api/.venv
(cd /var/www/api && .venv/bin/pip install -r requirements.txt)
gcloud --project $PROJECT secrets versions access 1 --secret jwt-secret > /var/www/api/jwt.key

cat > /etc/systemd/system/www-api.service <<'EOF'
[Unit]
Description=WWW API Service
After=network.target
[Service]
WorkingDirectory=/var/www/api
ExecStart=/var/www/api/.venv/bin/flask --app api-server run
Restart=always
[Install]
WantedBy=multi-user.target
EOF

gcloud storage cp -R $BUCKET/web/dist /tmp
cp -Rf /tmp/dist/* /var/www/html/

cat > /etc/nginx/sites-enabled/default  <<'EOF'
server {
  listen 80;
  server_name _;

  root /var/www/html;
  error_page 404 /index.html;

  if ($http_x_forwarded_proto = "http") {
    return 301 https://$host$request_uri;
  }

  location ~ ^/api/(.*)$ {
    set $upstream http://127.0.0.1:5000;
    proxy_pass $upstream/$1$is_args$args;
  }

  location / {
    try_files $uri $uri/ /index.html;
  }
}
EOF

systemctl daemon-reload
systemctl restart www-api
systemctl restart nginx
