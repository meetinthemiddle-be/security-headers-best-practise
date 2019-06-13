import sys
from subprocess import Popen, PIPE
import yaml
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
    print("https://" + fqdn + " was not reacheable. Timed out? non-200 response code? try curl-ing it manually:")
    print('curl', '-I', "https://" + fqdn, "-m5")
    sys.exit(1)

found_headers_clean = get_headers_from_response(output.decode())

overall_score = 0
warning_messages = [] 

with open("headerspec.yaml", 'r') as stream:
    try:
         spec_dictionary = yaml.safe_load(stream)
         for spec_header in spec_dictionary.items():
            min_required_count = int(spec_header[1]["mincount"])
            max_allowed_count = int(spec_header[1]["maxcount"])
                
            #print("DEBUG : '", spec_header[0],"'" )
            #print("DEBUG : '",found_headers_clean.keys(),"'" )

            if spec_header[0].lower() not in found_headers_clean.keys():
                ## CAT 1 : Off call && in spec
                observed_count = 0
            else:
                ## CAT 2 : In response && in spec
                observed_count = int(found_headers_clean[spec_header[0].lower()])
                

            #print("DEBUG : " , observed_count )
            #print("DEBUG : " , min_required_count )
            #print("DEBUG : " , max_allowed_count )

            if observed_count < min_required_count:
                overall_score += int(spec_header[1]["undermin-penalty"])
                warning_messages.append(spec_header[0] + " : "+ spec_header[1]["undermin-message"])
            elif observed_count > max_allowed_count:
                overall_score += int(spec_header[1]["overmax-penalty"])
                warning_messages.append(spec_header[0] + " : "+ spec_header[1]["overmax-message"])


    except yaml.YAMLError as exc:
        print(exc)

print("Overall score", overall_score)
print(warning_messages)
print("-----FULL HEADERS-----")
print(output.decode())
