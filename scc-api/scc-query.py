#!/usr/bin/env python3

import gzip
import httplib2
import json
import re
import sys
import xml.etree.ElementTree as ET
from getpass import getpass
 
def print_package_info(pkg_ele):
  #print(ET.dump(pkg_ele)) #Uncomment to print full package XML element
  name = pkg.find("./name")
  lic = pkg.find("./format/license")
  arch = pkg.find("./arch")
  version = pkg.find("./version") 
  checksum = pkg.find("./checksum")
  location = pkg.find("./location")
  print("Name: %s" % name.text)
  print("License: %s" % lic.text)
  print("Arch: %s" % arch.text)
  print("Version: %s-%s" % (version.attrib['ver'], version.attrib['rel']))
  print("Checksum: %s" % checksum.text)
  print("URL: %s%s%s\n" % (base, location.attrib['href'], token))

#Parse for pagination
def process_rels(response):
  links = response["link"].split(',')
  regex = re.compile(r'<(.*?)>; rel="(\w+)"')
  hash_refs = {}
  for link in links:
    href, name = regex.findall(link)[0]
    hash_refs[name] = href
  return hash_refs

#Strip XML namespaces to more easily parse
def strip_namespaces(xml_string):
  if isinstance(xml_string, bytes):
    xml_string = xml_string.decode("utf-8")
  xml_stripped = re.sub(' xmlns(:[a-zA-Z0-9]+)?="[^"]+"', '', xml_string)
  xml_stripped = re.sub('(<(\/?))[a-zA-Z0-9]+:', '\\1', xml_stripped)
  return xml_stripped

#Fetch and unpack gzipped XML
def parse_xml_gzip(element):
  href_ele = ele.find("./location")
  href = href_ele.attrib['href']
  url = "%s%s%s" % (base, href, token)
  xml_gzip = h.request(url, "GET")
  xml_dec = gzip.decompress(xml_gzip[1])
  xml = ET.fromstring(strip_namespaces(xml_dec))
  return xml

if __name__ == "__main__":
  h = httplib2.Http(".cache")
  #h.add_credentials(sys.argv[1], sys.argv[2])
  #request_url = sys.argv[3]
  
  username = input("Username: ")
  passwd = getpass("Password: ")
  h.add_credentials(username, passwd)

  request_url = input("URL: ")
   
  output = []

  (resp, content) = h.request(request_url, "GET")
  
  while True:
    output.extend(json.loads(content))
    rels = process_rels(resp)
    if not 'next' in rels:
      break
    (resp, content) = h.request(rels['next'], "GET")
  
  #Reversed content list to fetch newer products first
  for content in reversed(output):
      #print(content)
      if 'url' in content:
        curr = content['url']
        #Match URLs with an auth token
        regex = re.compile(r'(.*\/)(\?.*)')
        if regex.match(curr):
          #Split URL at token
          base, token = regex.findall(curr)[0]
          #Fetch repodata
          url = "%s%s%s" % (base, "repodata/repomd.xml", token)
          (resp, subcontent) = h.request(url, "GET")
          #Generate XML tree
          tree = ET.fromstring(strip_namespaces(subcontent))
          elems = tree.findall("./data[@type='primary']")

          for ele in elems:
            #print(ET.dump(ele))
            xml = parse_xml_gzip(ele)
            for pkg in xml.findall("./package[@type='rpm']"):
              print("Product: %s" % content['name']) 
              print("Product Description: %s" % content['description']) 
              if 'distro_target' in content:
                print("Distro Target: %s" % content['distro_target']) 
              print_package_info(pkg)