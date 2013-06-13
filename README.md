Send web points directly to MyFord Touch / SYNC services.  First Level Header
====================

The intent of this utility is to make it easy to send web points from a phone to MyFord Touch (Sync). Currently they have a crappy app that is supposed to do this called Sync Destinations. But it sucks. The map data it uses is bad and they should feel bad. This allows me to use my native Maps application and just share the point. I email it to an email address, and this script checks that mail address at a regular interval. When it sees a new message, it grabs the map point (VCF file), parses it, then sends it to the web service. 

This utility: 
---------------------

1.  Checks email on the account
2.  Looks for emails containing a VCF file. 
3.  Parses the VCF file for geographical data. 
4.  Sends that data to the MyFord Touch web service. 
5.  Deletes ALL MAIL from the mailbox. 

WARNING: Use a dedicated gmail box for this. It WILL DELETE ALL DATA ON EACH PASS.

Feel free to contact me if you have any questions. Or just let me know it's useful - I'd appreciate it.

Contact me at http://www.bugben.com
