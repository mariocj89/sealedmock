"""Sample code for the integration test"""
import urllib2


class SampleCodeClass(object):
    """This is sample code"""
    def calling_urlopen(self):
        return urllib2.urlopen("http://chooserandom.com")

    def calling_splithost(self):
        return urllib2.splithost("//host:port/path")
