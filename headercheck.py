import sys
from subprocess import Popen, PIPE
import yaml
import copy
from functions import *

if len(sys.argv) < 2:
    print("Please supply a valid FQDN (e.g. www.google.com)")
    sys.exit(1)
if(is_valid_fqdn(sys.argv[1])):
    fqdn = sys.argv[1]
else:
    print("Please supply a valid FQDN (e.g. www.google.com)")
    sys.exit(1)

p = Popen(['curl', '-I', "https://" + fqdn, "-m5"], stdin=PIPE, stdout=PIPE, stderr=PIPE) 
output, err = p.communicate(b"input data that is passed to subprocess' stdin")
rc = p.returncode

if rc > 0:
    print("https://" + fqdn + " was not reacheable. Timed out? non-200 response code? try curl-ing it manually with this command:")
    print('curl', '-I', "https://" + fqdn, "-m5")
    sys.exit(1)

found_headers_clean = get_headers_from_response(output.decode())
headers_not_in_spec = copy.deepcopy(found_headers_clean)

overall_score = 0
warning_messages = []
cheer_messages = []
info_messages = [] 


with open("presence_and_frequency.yaml", 'r') as stream:
    try:
         spec_dictionary = yaml.safe_load(stream)
         for spec_header in spec_dictionary.items():

            del headers_not_in_spec[spec_header[0].lower()]

            min_required_count = int(spec_header[1]["mincount"])
            max_allowed_count = int(spec_header[1]["maxcount"])
                
            #print("DEBUG : '", spec_header[0],"'" )
            #print("DEBUG : '",found_headers_clean.keys(),"'" )

            if spec_header[0].lower() not in found_headers_clean.keys():
                ## CAT 1 : not in response && in spec
                observed_count = 0
            else:
                ## CAT 2 : In response && in spec
                observed_count = int(found_headers_clean[spec_header[0].lower()])
                

            #print("DEBUG : " , observed_count )
            #print("DEBUG : " , min_required_count )
            #print("DEBUG : " , max_allowed_count )

            if observed_count < min_required_count:

                overall_score += int(spec_header[1]["undermin-penalty"])
                warning_messages.append('"' + spec_header[0] + '"' + ' : ' + spec_header[1]["undermin-message"] + "adding penalty: " + str(spec_header[1]["undermin-penalty"]))
            elif observed_count > max_allowed_count:
                overall_score += int(spec_header[1]["overmax-penalty"])
                warning_messages.append('"' + spec_header[0] + '"' + ' : ' + spec_header[1]["overmax-message"])
            else:
                cheer_messages.append('"' + spec_header[0] + '"' + " : Found! Well done!")

    except yaml.YAMLError as exc:
        print(exc)


## Test for CAT 3 : in response && not in spec
ignore_these_headers = get_headers_to_ignore()

for non_specced_header in headers_not_in_spec:
    if non_specced_header not in ignore_these_headers:
        info_messages.append('"' + non_specced_header + '"' + " : Not sure what this header does. Please review.")


print("Overall score : ", overall_score)
print("")
print("-----GOOD-----")
for m in cheer_messages:
    print(m)

print("")
print("-----NOT SO GOOD-----")
for m in warning_messages:
    print(m)

print("")
print("-----FYI-----")
for m in info_messages:
    print(m)

print("")
print("-----FULL HEADERS-----")
print(output.decode())
