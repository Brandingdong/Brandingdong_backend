daemon = False
chdir = '/srv/brandingdong/apps'
bind = 'unix:/run/brandingdong.sock'
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'
capture_output = True