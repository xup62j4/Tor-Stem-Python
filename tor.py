import StringIO
import socket
import urllib
import urllib2
import random

import socks  # SocksiPy module
import stem.process

from stem.util import term

SOCKS_PORT = 7000

# Set socks proxy and wrap the urllib module

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
socket.socket = socks.socksocket

# Perform DNS resolution through the socket

def getaddrinfo(*args):
  return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

socket.getaddrinfo = getaddrinfo


def query(url):
  """
  Uses urllib to fetch a site using SocksiPy for Tor over the SOCKS_PORT.
  """

  try:
    user_agent_arr = ["Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36","Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)"]
    #user_agent = 'Mozilla/4.0 (JohnDoe)'
    values = {}
    headers = { 'User-Agent' : user_agent_arr[random.randint(0,2)] }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    return response.read()
    #return urllib.urlopen(url).read()

  except IOError as e:
    return "I/O error({0}): {1}".format(e.errno, e.strerror)


# Start an instance of Tor configured to only exit through Russia. This prints
# Tor's bootstrap information as it starts. Note that this likely will not
# work if you have another Tor instance running.

def print_bootstrap_lines(line):
  if "Bootstrapped " in line:
    print term.format(line, term.Color.BLUE)

print term.format("Starting Tor:\n", term.Attr.BOLD)

tor_process = stem.process.launch_tor_with_config(
  config = {
    'SocksPort': str(SOCKS_PORT),
    'ExitNodes': '{us}',
  },
  init_msg_handler = print_bootstrap_lines,
)

print term.format("\nChecking our endpoint:\n", term.Attr.BOLD)
print term.format(query("http://www.whatismyip.com.tw/"))

tor_process.kill()  # stops tor
