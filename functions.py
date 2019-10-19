import yaml
import re
from subprocess import Popen, PIPE
import inspect

def debugprint(txt):
    if (False):
        print("DEBUG::" + txt)

def line_nr():
    return "LINE--:" + str(inspect.currentframe().f_back.f_lineno)

def colorize(txt, clr):
    # TODO : Implement this; function is currently unused in headercheck.py
    if(clr == 'RED'):
        colorcode = '0;31'
    elif(clr == 'GREEN'):
        colorcode = '0;32'
    elif(clr == 'ORANGE'):
        colorcode = '0;33'
    else:
        print("Invalid color!!")
        sys.exit(1)
    prefix = '\033[' + colorcode
    suffix = '\033[0m'
    return (prefix + txt + suffix)

def is_valid_fqdn(hostname):
    if hostname[-1] == ".":
        # strip exactly one dot from the right, if present
        hostname = hostname[:-1]
    if len(hostname) > 253:
        return False

    labels = hostname.split(".")

    # the TLD must be not all-numeric
    if re.match(r"[0-9]+$", labels[-1]):
        return False

    allowed = re.compile(r"(?!-)[a-z0-9-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(label) for label in labels)


def has_valid_response_code(found_headers_raw):
    debugprint("FIRST RESP LINE" + found_headers_raw.split("\r\n")[0])
    respcode = found_headers_raw.split("\r\n")[0].split(' ')[1]
    resp_category = respcode[:1]
    if(resp_category == "2"):
        debugprint("GOOD::" + found_headers_raw.split("\r\n")[0])
        return True
    else:
        debugprint("BAD::" + found_headers_raw.split("\r\n")[0])
        return False

def get_headers_from_response(found_headers_raw):
    found_headers_raw = found_headers_raw.split("\r\n")
    found_headers_clean = {}

    skip_headers_that_start_with = ['HTTP/', 'http/']

    for found_header_raw in found_headers_raw:
        found_header_clean_parts = found_header_raw.split(":")
        found_header_clean = found_header_clean_parts[0].lower()

        skip = 0
        for skipthisheader in skip_headers_that_start_with:
            if( (skipthisheader in found_header_clean) or len(found_header_clean) < 3):
                skip=1

        if(skip == 0):

            if(found_header_clean in found_headers_clean.keys()):
                found_headers_clean[found_header_clean] += 1
            else:
                found_headers_clean[found_header_clean] = 1
        
    return(found_headers_clean)

def get_headers_to_ignore():
    ignore_these_headers = []
    with open("ignore-these-headers.yaml", 'r') as stream:
        try:
            spec_dictionary = yaml.safe_load(stream)
            for spec_header in spec_dictionary.items():
                ignore_these_headers.append(spec_header[0].lower())
            

        except yaml.YAMLError as exc:
            print(exc)
    return ignore_these_headers
