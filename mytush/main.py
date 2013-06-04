#!/usr/bin/env python

import email, imaplib, re, json
import urllib, urllib2
import settings


def main(): 
    user = settings.gmail_user
    pwd = settings.gmail_pass

    m = imaplib.IMAP4_SSL("imap.gmail.com")
    m.login(user,pwd)
    m.select("[Gmail]/All Mail") 

    resp, items = m.search(None, "ALL") 
    items = items[0].split() 

    if not items: 
        print "No new email."
        return

    for emailid in items:
        resp, data = m.fetch(emailid, "(RFC822)") 
        email_body = data[0][1]
        mail = email.message_from_string(email_body) 

        # check for attachments
        if mail.get_content_maintype() != 'multipart':
            continue

        print "["+mail["From"]+"] :" + mail["Subject"]

        for part in mail.walk():
            # multipart are just containers, so we skip them
            if part.get_content_maintype() == 'multipart':
                continue

            # is this part an attachment ?
            if part.get('Content-Disposition') is None:
                continue

            vcf = part.get_payload(decode=True)
            make_request(vcf)

    # delete all mailbox messages
    #m.store("1:*",'+X-GM-LABELS', '\\Trash')


def parse_vcf(vcf): 
    print vcf
    addr = re.findall(r"item[1-9]\.ADR.+?;.+?;;(.*);(.*);(.*);(.*);(.*)", vcf, re.M)[0]
    latlon = re.findall(r"item[1-9]\.URL.*sll=(.+?)\\,(.+?)&", vcf, re.M)[0]
    location = {}
    location['name'] = addr[0]
    location['street'] = addr[0]
    location['city'] = addr[1]
    location['state'] = addr[2]
    location['postalCode'] = addr[3]
    location['countryLong'] = 'United States'
    location['country'] = 'US'
    location['latLng'] = { 'lat': latlon[0], 'lon': latlon[1] }
    vcf_obj = { 'mobileNumber': settings.mobile_num, 
            'locations': [location,] } 
    return vcf_obj


def make_request(vcf): 
    vcf_dict = parse_vcf(vcf)
    url = 'https://www.mapquest.com/FordSyncServlet/submit'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    json_data = json.dumps(vcf_dict)
    print json_data
    request_object = urllib2.Request(url, json_data, headers)
    response = urllib2.urlopen(request_object)
    print response.read()

if __name__ == '__main__':
    main()
