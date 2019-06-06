import sys
import subprocess
import yaml

domain = sys.argv[1]
output = subprocess.check_output('hsecscan -u https://' + domain + ' -i', shell=True)
split_output = output.split("\n\n")
headers = split_output[0]

with open("headerspec.yml", 'r') as stream:
    try:
        spec_dictionary = yaml.safe_load(stream)
	for spec_headers in spec_dictionary.iteritems():
	    if spec_headers[1] == 'disallowed':
	    	print spec_headers[0] + ": nono!"
    except yaml.YAMLError as exc:
        print(exc)
