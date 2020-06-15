#!/usr/bin/env python
# Centralise management of data paths

import os

_dataRoot = None


def dataRoot():
	global _dataRoot
	if _dataRoot == None:
		_dataRoot = os.getenv('DATA_ROOT', 'data')
	
	return _dataRoot

		
def dataFilePath(filename):
	"""Helper function to return the full path of a file in the data root"""
	return os.path.join(dataRoot(), filename)

