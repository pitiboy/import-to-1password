#!/usr/bin/env python

import os
import logging
import sys
import re

import ConfigParser
import argparse
from jinja2 import Environment, PackageLoader
from bs4 import BeautifulSoup

# Helper
def normalize(s):
  return '"%s"' % s.replace('"', '""') if s else ''

# Setup logging
script_name = os.path.splitext(os.path.basename(__file__))[0]
logging.basicConfig()
logger = logging.getLogger(script_name)
logger.setLevel(logging.DEBUG)

# Parse command line options
parser = argparse.ArgumentParser(
    description='Converts MacPass XML file to 1Password CSV')
parser.add_argument('--version', action='version', version='%(prog)s 0.2.0')
args = parser.parse_args()

# Read config file
config = ConfigParser.SafeConfigParser()
config.read(os.path.join('etc', 'settings.conf'))

passwords_xml = BeautifulSoup(open(config.get('General', 'input')), 'lxml')
logger.info('MacPass XML file is opened')

secrets = []

for entry in passwords_xml.find_all('entry'):
  if entry.find_parent('history'):
    continue

  matches = False
  folders = []
  parentGroups = entry.find_parents('group')
  for group in parentGroups:
    if not re.match(config.get('xml', 'regexExcludeFolder'), group.find('name').string):
      folders.append(group.find('name').string.lower())
    if group.find('name').string == config.get('xml', 'root'):
      matches = True

  if matches == False:
    continue

  secret = {}
  # collect fields
  fields = {}

  for tag in entry.find_all('string'):
    if not tag.find_parent('history'):
      fields[tag.key.string.lower()] = tag.value.string

  secret['title'] = normalize(fields['title'])
  secret['username'] = normalize(fields['username'])
  secret['password'] = normalize(fields['password'])
  secret['url'] = normalize(fields['url'].replace('http://', '')) if fields['url'] else ''
  secret['notes'] = normalize(fields['notes'])
  secret['tags'] = normalize(",".join(folders))

  secrets.append(secret)


# Prepare output file
env = Environment(loader=PackageLoader('__main__', 'templates'))
template = env.get_template('passwords.tmpl')
output = open(config.get('General', 'output')+'-'+config.get('xml', 'root')+config.get('General', 'outputExtension'), 'w')
output.write(template.render(passwords = secrets).encode('utf-8'))
output.close()

logger.info('1Password CSV file is written')
