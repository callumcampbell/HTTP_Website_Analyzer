# HTTP_Webstie_Analyzer
Python program that analyzes a website's URI and extracts key HTTP request and response data

---About---
Webtester.py is a python program that accepts a website URI as input, prints out the various pieces of http requests and response,
then details the following:

    -Whether or not the website supports http/2
    -List of cookies on the website
    -Whether or not the website is password protected

---Input Format---
Webtester accepts a URI input in the following format:

    -https://hostname/filepath
    -http://hostname/filepath
    -hostname/filepath
    -hostname

where [hostname] and [filepath] are the fields intended to be varied by the user

--Examples---
The following are examples of 3 acceptable inputs for Webtester.py

    -https://www.uvic.ca/index.html
    -https://engr.docs.uvic.ca
    -uvic.ca

---Example outputs---
For the 1st example above, I will give the output of it running with Webtester.py:

GET / HTTP/1.1
Host: www.uvic.ca
Connection: Upgrade
Upgrade: h2c


---Request sent---


---Printing http response header---
HTTP/1.1 200 OK
Date: Thu, 26 Sep 2024 17:14:13 GMT
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Set-Cookie: PHPSESSID=295i378pplo3th77csfaeog9n0; path=/; secure; HttpOnly; SameSite=Lax
Set-Cookie: uvic_bar=deleted; expires=Thu, 01-Jan-1970 00:00:01 GMT; Max-Age=0; path=/; domain=.uvic.ca; secure; HttpOnly
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Vary: Accept-Encoding,User-Agent
Feature-Policy: accelerometer 'none'; camera 'none'; geolocation 'none'; gyroscope 'none'; magnetometer 'none'; microphone 'none'; payment 'none'; usb 'none'
Content-Type: text/html; charset=UTF-8
Set-Cookie: www_def=!EY/agJbz7JuPJ1R2WoCbqs3+3m8imx4tBO1iXNIecApUDrBvoXMqkANSabLQYuVb7hv1xq8TGfNfEoM=; path=/; Httponly; Secure
Strict-Transport-Security: max-age=16070400
Connection: close
Set-Cookie: TS018b3cbd=0183e075349890fae90fcfb1ada74fa0b301d64c04df541cf589b9648d233f225481b79cedd78f90ca
---done printing http header---


---Now printing website characterisics---
 
1. Supports http2? : No

2. Printing all cookies

Cookie name: PHPSESSID, 
Cookie name: uvic_bar, expires time: Thu, 01-Jan-1970 00:00:01 GMT, domain name: .uvic.ca
Cookie name: www_def, 
Cookie name: TS018b3cbd, 
Done Printing cookies

3. Password Protected?: No 
