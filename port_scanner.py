import socket
import re
import common_ports

# is hostname an ip? (must not be valid)
def check_is_ip(hostname):
    if re.search(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', hostname) is None:
        return False
    return True

# verbose: ausfuehrlich
def get_open_ports(target, port_range, verbose=False):
  """
  Usage examples:
  get_open_ports("209.216.230.240", [440, 445])
  get_open_ports("www.stackoverflow.com", [79, 82], True)

  return a list of open ports in the given range
  """
  open_ports = []

  try:
    # get ip by host
    IPaddress = socket.gethostbyname(target)
  except:
    # [Errno -2] Name or service not known > Host or IP is wrong
    if check_is_ip(target)==True:
      return "Error: Invalid IP address"
    return "Error: Invalid hostname"     

  if IPaddress != target:
      Hostname = target
  else:      
    try:
      # get host by ip
      Hostname, aliaslist, ipaddrlist = socket.gethostbyaddr(target)
    except:
      Hostname = None
    
  # check ports
  for port in range(port_range[0], port_range[1]+1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5) # terminate after 5 seconds
    err=s.connect_ex( (target, port) )
    if err:
      # error-code > port is closed
      # https://gist.github.com/gabrielfalcao/4216897
      # 11 = Resource temporarily unavailable
      #print(port, err)
      pass
    else:
      # no error-code > port is open
      open_ports.append(port)  
    s.close()

  # verbose-mode
  if verbose==True:
    if Hostname is None:
      t = f"Open ports for {IPaddress}\n"
    else:
      t = f"Open ports for {Hostname} ({IPaddress})\n"
    t += "PORT     SERVICE"
    for port in open_ports:
      service_name = '-'
      if port in common_ports.ports_and_services:
        service_name = common_ports.ports_and_services[port]
      p = str(port)
      t+= "\n"+p + ' '*(9-len(p)) + service_name
      open_ports = t

  return(open_ports)