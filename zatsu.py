#!/usr/bin/env python
"""
This script launches a singleton instance of ZatsuDachi.

Usage: python zatsu.py
Setup: pip install colour flask flask_socketio tk requests userpaths

The _singletonApp module is responsible for ensuring that only one instance of the application is running.
The script runs an infinite loop to keep the main thread alive.
"""

from zatsu.api import _singletonApp

if __name__ == "__main__":
	_singletonApp.go() # Launches plugin threads
	while _singletonApp.is_running:
		_singletonApp.process_main_thread_tasks()
	_singletonApp.stop()
