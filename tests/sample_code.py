"""Sample code for the integration test"""
import os


class SampleCodeClass(object):
    """This is sample code"""
    def calling_rm(self):
        return os.rm("/secret_path")

    def calling_pardir(self):
        return os.pardir
