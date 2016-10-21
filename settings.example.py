import time

# output name of freewvs scan
IN_FILE = 'vulnscan.xml'
# output name of the csv we will parse the xml to
OUT_FILE = 'vulnscan_%s.csv' % time.strftime('%Y%m%d')

# name of parent dir where hostings are stored
HOSTING_DIR = 'vhosts'

# scan results are sent via email to subscribers
SUBSCRIBERS = [
    'root@example.com',
    'webmaster@example.com',
]
SMTP_HOST = 'localhost'
SMTP_PORT = None
SMTP_USER = 'no-reply@example.com'
SMTP_PASS = None
