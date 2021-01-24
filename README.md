# HTTP security headers best practise (WORK IN PROGESS)
The core of this project is a Python 3 script that helps you check compliance against a baseline. The baseline is defined in code to make it easier to audit changes to them.

Secondary purpose of the project is this README. The  table below a best practise cheat sheet for HTTP security headers.


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

### Acknowledgements / Sources
- https://scotthelme.co.uk/hardening-your-http-response-headers/
- https://security.stackexchange.com/questions/147554/security-headers-for-a-web-api
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers#Security
- https://pentest-tools.com/blog/essential-http-security-headers/
