# process freewvs results
#
# Parses the resulting xml into csv and sends it via email to subscribers.
# All settings are in settings.py module.
#
# Usage:
# ./freewvs -x path/to/hostings > vulnscan.xml && python processResults.py
#
# I recommand updating the freewvsdb/ dir or it won't work too long. You can
# pass the output from `svn up` to this script as the first arg and it will be
# included in the mail.
#
# Example:
# update="$(svn up $install_dir/freewvsdb)"
# python ./processResults.py "${update}"
#
# Please note this script is not trying to win a beauty contest, it was written
# specifically to deal with the freewvs results.
import pprint
import csv
import time
import os
import settings
import sys
import re
from lxml import etree


def parse_script_path(path, split):
    # make sure split keyword ends with a slash or the following split
    # won't make sense
    if (not split.endswith('/')):
        split += '/'
    parts = path.partition(split)
    return parts[2].split('/', 1)


def parse_result_xml(in_file, out_file):
    """Parse freewvs result xml into csv"""
    with open(out_file, 'w') as f:
        header = (
            'appname', 'version', 'hosting', 'path', 'safeversion', 'vulninfo')
        writer = csv.writer(f)
        writer.writerow(header)
        root = etree.parse(in_file)
        for app in root.iter('app'):
            # split directory into hosting name and relative path to script
            # directory
            hosting, path = parse_script_path(
                app.find('directory').text,
                settings.HOSTING_DIR
                )

            appname = app.find('appname').text
            version = app.find('version').text
            hosting = hosting
            path = path
            safeversion = app.find('safeversion').text
            vulninfo = app.find('vulninfo').text

            row = appname, version, hosting, path, safeversion, vulninfo
            writer.writerow(row)


def email_results(recipients, attachments, text_addon):
    """Send an email with attachment(s)"""
    from smtplib import SMTP
    from email.mime.text import MIMEText
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEBase import MIMEBase
    from email import Encoders
    import socket

    # scan results from <datetime> on <hostname>
    text = ("Web vulnerability scan results from %s on %s."
    % (time.strftime('%d.%m.%Y %H:%M'), socket.gethostname()))
    if (text_addon):
        text += '\n\n' + text_addon
    text += '\n\nPowered by freewvs and Adfinis SyGroup AG.'
    text += '\nhttps://wiki.adfinis-sygroup.ch/adsy/index.php/Freewvs'

    # build message
    msg = MIMEMultipart()
    msg['Subject'] = 'Vulnerability scan results %s' % time.strftime('%Y%m%d')
    msg['From'] = settings.SMTP_USER
    msg['To'] = ', '.join(recipients)
    msg.attach(MIMEText(text))

    for f in attachments:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(f, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
            % os.path.basename(f))
        msg.attach(part)

    # send mail
    smtp = SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
    smtp.starttls()
    if (settings.SMTP_PASS):
        smtp.login(settings.SMTP_USER, settings.SMTP_PASS)
    smtp.sendmail(msg['From'], recipients, msg.as_string())
    smtp.quit()


# get output from `svn up`
try:
    update_output = sys.argv[1]

    # get revision from update message
    match = re.search('revision (\d+)?', update_output)
    db_version = match.groups()[0]

    # there was an update
    if (update_output.lower().find('updated') >= 0):
        update_msg = 'freewvsdb was automatically updated to revision %s' % db_version
    # no update
    else:
        update_msg = 'freewvsdb is up-to-date at revision %s' % db_version
except:
    update_msg = 'Notice: freewvsdb updater is not working. This should be fixed!'


# parse freewvs xml to csv
parse_result_xml(settings.IN_FILE, settings.OUT_FILE)

# notify subscribers and send csv as attachment
email_results(
    recipients=settings.SUBSCRIBERS,
    attachments=[settings.OUT_FILE],
    text_addon=update_msg
)

# log some infos
print("\n[%s] Vulnerability scan complete. Sent email." % time.strftime('%Y-%m-%d-%H:%M'))
print("Purged generated file %s" % settings.OUT_FILE)
print(update_msg)
print('Output from `svn update freewvsdb`:')
print(update_output)
os.remove(settings.OUT_FILE)

