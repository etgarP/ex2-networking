s = get_server()
closed_connection = True
OK = 200
REDIRECT = 301
NOT_FOUND = 404
in_redirect = False
while(True):
    if (not in_redirect):
        path = get_input()
    in_redirect = False
    if (closed_connection)
        connect_to_server(sersver)
        closed_connection = False
    send_input(path)
    response = get_response(s)
    if (not response):
        closed_connection = True
        s.close()
        continue 
    parsed = parse_response(response)
    if (not parsed):
        closed_connection = True
        s.close()
        continue 
    (status, first_line, file, lines) = parsed
    print(first_line)
    if(status == OK):
        save_file(file)
        if (connection_closed(lines)):
            closed_connection = True
            s.close()
        continue
    elif(status == REDIRECT):
        path = getLocation(lines)
        in_redirect = True
    closed_connection = True
    s.close()    


        



