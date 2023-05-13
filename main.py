from api import _singletonApp

if __name__ == "__main__":
	_singletonApp.go()

	while True:
		pass # Keep the main thread alive!