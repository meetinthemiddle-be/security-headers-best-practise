# HTTP security headers best practise (WORK IN PROGESS)
The core of this project is a Python 3 script that helps you check compliance against a baseline. The baseline is defined in code to make it easier to audit changes to them.

Secondary purpose of the project is this README. The table below serves as a best practise cheat sheet for HTTP response headers.


| Header                      |  Web            |  API  | Remark
|-----------------------------|-----------------|-------|------------
| `Strict-Transport-Security` | Add             | Add   | -
| `X-XSS-Protection`          | Add             | N/A   | Remark 1
| `X-Content-Type-Options`    | Add             | N/A   | If you're running a JSON API you should serve the responses with `Content-Type: application/json`. If you do that correctly there will be no need to add the nosniff directive.
| `X-Frame-Options`           | Add             | N/A   | Remark 1
| `Content-Security-Policy`   | Add             | N/A   | Remark 1, Remark 2
| `Server`                    | Remove          | Remove | Remark 3
| `X-Powered-By`              | Remove          | Remove | Remark 3


**Remark 1** : When serving an API that provides only JSON responses and doesn't serve active content, there's no benefit in adding this header.

**Remark 2** : Getting a CSP 'right' can be extremely difficult if you don't incorporate it in your project from the beginning and commit to doing it properly. Contrary to headers like `Strict-Transport-Security` which  apply across the board with one value for your entire site, having one single CSP for *every* page may open you up to a vulnerability which could've easily been mitigated by customizing it per page. In short: If a CSP is not designed to be 100% watertight, it can be bypassed by a skilled attacker.

**Remark 3** : These headers, whose purpose is to advertise details about the technology stack on the server side, don't serve any other good purpose. The information that they show can only ever serve as useful for someone who is looking for vulnerable technologies when preparing an attack. Malicious hackers perform mass scans of public domains or IP addresses to identify easy targets based on the version information that is displayed here.

### Acknowledgements / Sources
- https://scotthelme.co.uk/hardening-your-http-response-headers/
- https://security.stackexchange.com/questions/147554/security-headers-for-a-web-api
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers#Security
- https://pentest-tools.com/blog/essential-http-security-headers/
