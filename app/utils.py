"""
Module to function
"""


def find_element(iterable, condition):
    return [x for x in iterable if x["name"] == condition][0]
