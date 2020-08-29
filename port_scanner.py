import socket
import re

# checking hostname: there seems NOT to be a clean solution
# that is built in python, so here I take: 
#https://stackoverflow.com/questions/2532053/validate-a-hostname-string
# info: urllib does not work
# from urllib.parse import urlparse => http://asdasd -> valid!
def is_valid_hostname(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1]
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

# verbose: ausfuehrlich
def get_open_ports(target, port_range, verbose=False):
  """
  Usage examples:
  get_open_ports("209.216.230.240", [440, 445])
  get_open_ports("www.stackoverflow.com", [79, 82])

  return a list of open ports in the given range
  """
  open_ports = []
  

  # check valid hostname
  if is_valid_hostname(target)==False:
    # TODO CHECK IPADRESS
    # problem: if target is nonsense - which error should be displayed?
    # extra check: is it an IP, but probably a wrong one
    return "Error: Invalid IP address"

    # no url and no ip
    return "Error: Invalid hostname"
    

  # check ports
  for port in range(port_range[0], port_range[1]+1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5) # terminate after 5 seconds
    err=s.connect_ex( (target, port) )
    if err:
      # error-code > port is closed
      # https://gist.github.com/gabrielfalcao/4216897
      # 11 = Resource temporarily unavailable
      print(port, err)
      #pass
    else:
      # no error-code > port is open
      open_ports.append(port)  
    s.close()

    # TODO
    if verbose==True:
      IPaddress = 'TODO'
      t = f"Open ports for {target} ({IPaddress})"
      t+= "PORT     SERVICE"
      for port in open_ports:
        t+= "{port}   {service name}" # totdo service name
      open_ports = t

  return(open_ports)