# HTTP security headers best practise (WORK IN PROGESS)
The README for this repo contains a best practise cheat sheet for HTTP security headers
The core of the project is a Python3 script to check compliance against a set of YAML-based spec sheets which you can adapt/adjust for your specific project needs.


| Header                      |  Web            |  API  | Remark
|-----------------------------|-----------------|-------|------------
| `Strict-Transport-Security` | Add             | Add   | -
| `X-XSS-Protection`          | Add             | N/A   | Remark 1
| `X-Content-Type-Options`    | Add             | N/A   | If you're running a JSON API you should serve the responses with `Content-Type: application/json`. If you do that correctly there will be no need to add the nosniff directive.
| `X-Frame-Options`           | Add             | N/A   | Remark 1
| `Content-Security-Policy`   | Add             | N/A   | Remark 1
| `Server`                    | Remove          | Remove | No good can come of adding this header. Ever.
| `X-Powered-By`              | Remove          | Remove | No good can come of adding this header. Ever.


Remark 1 : When serving an API that provides only JSON responses and doesn't serve active content, there's no benefit in adding this header.

### acknowledgements / Sources
- https://scotthelme.co.uk/hardening-your-http-response-headers/
- https://security.stackexchange.com/questions/147554/security-headers-for-a-web-api
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers#Security
- https://pentest-tools.com/blog/essential-http-security-headers/
