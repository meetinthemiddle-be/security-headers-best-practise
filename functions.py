
import re
from subprocess import Popen, PIPE


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


def get_headers_from_response(found_headers_raw):
    found_headers_raw = found_headers_raw.split("\r\n")
    found_headers_clean = {}

    skip_headers_that_start_with = ['HTTP/']

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