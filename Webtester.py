import socket
import sys
import re
import ssl

def main():

    #line accepts URI
    try:
        line = sys.argv[1]
    except IndexError:
        print("Error: no input URI was provided")
        sys.exit()

    begin(line)

#begin takes a URI as input, either user input URI, or location redirect
def begin(input_line):

    hostname, filepath = parse_input(input_line)
    http_only = False
    if hostname.endswith('/'):
        hostname = hostname[:-1]
    pas_protected = "No"
    #establish http connection

    try:
        conn, h2_wrk = https_connect(hostname, 443)
    except ssl.SSLCertVerificationError as e:
        #means website uses http
        conn = http_connect(hostname, 80)
        h2_wrk = False
        http_only = True
    except Exception as e2:
        print("Unable to establish TCP Connection\n"
                "Please ensure that Valid URI is provided\n"
               f"Error: {e2}"
            )
        
        sys.exit()

    #send http request
    if h2_wrk:
        h2_wrk = 'Yes'
    else:
        h2_wrk = 'No'

    request_h2 = f"GET {filepath} HTTP/1.1\r\nHost: {hostname}\r\nConnection: Upgrade\r\nUpgrade: h2c\r\n\r\n"
    request_http = f"GET {filepath} HTTP/1.0\n\n"
    
    #receive http response
    if http_only == False:
        
        http_header, http_body = send_http_req(conn, request_h2)
    else:
        http_header, http_body = send_http_req(conn, request_http)

    code = get_header_code(http_header)

    #analyze response code, if redirect needed: re-do with new location as input
    if code == '301' or code == '302':
        conn.close()
        new_line = get_new_inpline(http_header)
        begin(new_line)
        return

    #Print http or https request
    if http_only == False:
        print(request_h2)
    else:
        print(request_http)

    print('---Request sent---')
    print('\n')

    #If code is 401, then mark it as password protected
    if code == '401':
        pas_protected = 'Yes'
    new_http_header = http_header
    new_http_body = http_body
    
            
    #Printout response header   
    print("---Printing http response header---")
    print(new_http_header)
    print("---done printing http header---")
    print('\n')

    #If body exists, print it out
    if new_http_body:
        print("---printing http body---")
        print(new_http_body)
        print("---done printing http body---")
        print('\n')

    print("---Now printing website characterisics---\n ")
    print(f"1. Supports http2? : {h2_wrk}\n")

    print("2. Printing all cookies\n")
    print_cookies(new_http_header)
    print("Done Printing cookies\n")

    print(f"3. Password Protected?: {pas_protected} ")

    conn.close()

def http_connect(hostname, portnum):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname,portnum))
    return s

def get_new_inpline(head):
    sep_head = head.splitlines()
    #loc_line = sep_head[1]
    for line in sep_head:
        if re.match(r"(Location: )(.*)",line):
            new = re.match(r"(Location: )(.*)", line)
            new_inp = new.group(2)
            break
    return new_inp

def get_header_code(header):
    first_line = header.splitlines()[0]
    code = re.search(r'(\d\d\d)',first_line).group(1)
    return code

def print_cookies(header):
    sep_header = header.splitlines()
    for line in sep_header:
        if re.match(r'^(Set-Cookie:)', line):
            sep_line = re.search(r'^(Set-Cookie:) ([^\=]+).([^\;]+)', line)
            expr = re.search(r'(expires=)([^\;]+)', line)
            dmn = re.search(r'(domain=)([^\;]+)', line)
            name_str = f"Cookie name: {sep_line.group(2)}, "
            expr_str = ""
            dmn_str = ""
            if expr:
                expr_str = f"expires time: {expr.group(2)}, "
            if dmn:
                dmn_str = f"domain name: {dmn.group(2)}"
            print(name_str + expr_str + dmn_str)


def parse_input(line):

    #determine if protocol specified in URI
    protocol_exists = re.search(r'^(http|https)\:\/\/', line)

    #determine if filepath specified in URI
    filepath_exists = re.search(r'(?<=[a-zA-Z])\/(?=[a-zA-Z])', line)
    link_sep = None
    hostname = None 
    filepath = None
     
    if protocol_exists and filepath_exists:
        link_sep = re.search( r'^(http|https)\:\/\/([^\/]+)\/(.*)$', line )
        hostname = link_sep.group(2)
        filepath = '/' + link_sep.group(3)
 
    elif protocol_exists and not filepath_exists:
        link_sep = re.search( r'(?<=\:\/\/).*', line )
        hostname = link_sep.group(0)

    elif not protocol_exists and not filepath_exists:
        hostname = line

    else:
        link_sep = re.search(r'^([^\/]+)\/(.*)$', line)
        hostname = link_sep.group(1)
        filepath = "/" + link_sep.group(2)

    if filepath is None:
        filepath = '/'

    return hostname, filepath

def https_connect(hostname, port_num):

    h2_work = False
    context = ssl.create_default_context()
    context.set_alpn_protocols(['h2', 'http/1.1'])
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname= hostname)
    conn.connect((hostname, port_num))
    prot_used = conn.selected_alpn_protocol()

    if prot_used == 'h2':
        conn.close()
        new_context = ssl.create_default_context()
        new_context.set_alpn_protocols(['http/1.1'])
        new_conn = new_context.wrap_socket(socket.socket(socket.AF_INET), server_hostname= hostname)
        new_conn.connect((hostname, port_num))
        h2_work = True
        return new_conn, h2_work
    return conn, h2_work
    

def send_http_req(connection, req):

    try:
        connection.sendall(req.encode('utf-8'))
    except Exception as e:
        print("Unable to send http request\n"
              f"Error: {e}"
              )
        sys.exit()

    try:
        raw = (connection.recv(1024)).decode('utf-8')
    except Exception as e:
        print("Unable to receive http response\n"
              f"Error: {e}"
              )
        sys.exit()

    connection.close()
    
    try:
        headers, body = raw.split("\r\n\r\n", 1)
    except ValueError:
        # If there's no body, handle it by setting body to None
        headers = raw
        body = None
    
    return headers, body

if __name__ == "__main__":
    main()