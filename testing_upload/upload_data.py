#!/usr/bin/env python

def build_url(action="write", domain="rhok1", key="punsOMMYMAI27tk"):
    """
    Action is write/note/person
    """
    url = "https://%s.googlepersonfinder.appspot.com/api/%s?key=%s" % (domain, action, key)
    return url

if __name__ == "__main__":
    domain = "rhok1"
    key = "punsOMMYMAI27tk"
    action = "write"
    print build_url("write")
