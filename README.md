# Naive DNS Server

This is a naive dns server using Python dnslib.

```
# Note: Use SPACE character to split columns.
#       DO NOT use TAB character. It's not allowed.
#       DO NOT forget the dot at the end of hostname.
# hostname        TYPE   TTL    VALUE
example.com.       A     60   1.1.1.1
example.com.       A     60   1.0.0.1
example.com.       AAAA  60   2606:4700:30::681b:90e6
# TXT record: DO NOT add the double quote `""`.
example.com.       TXT   120  fuck you
example.com.       TXT   120  v=spf -all
example.com.       NS    120  l.example.com.
b.example.com.     A     60   2.2.2.2
l.example.com.     A     60   127.0.0.1
mail.example.com.  MX    300  5,b.example.com
mail.example.com.  MX    300  10,l.example.com
f.example.com.     CNAME 30   b.example.com

# wildcards
*.b.example.com.   A     60   114.114.114.114
*.b.example.com.   AAAA  60   ::1
?.example.com.     A     120  6.6.8.8
*.example.com.     A     60   8.8.8.8
*.com.             TXT   30   default txt reply for com
*                  PASS  PASS 8.8.8.8
```
