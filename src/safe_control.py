import os 
import time

DEV_MODE_FILE = "/home/annaliesepintar/FaceBox/src/dev_mode"
COUNTDOWN_TIME = 10

def is_dev_mode():
	return os.path.exists(DEV_MODE_FILE)

def safe_shutdown():
	if is_dev_mode():
		print("Development mode active - system will not shutdown")
		return False
		
	print(f"PRODUCTION MODE: System will shut down in {COUNTDOWN_TIME} seconds")
	print("To cancel: Create a file at /home/annaliesepintar/FaceBox/src/dev_mode")
	print("(via SSH: touch /home/annaliesepintar/FaceBox/src/dev_mode)")
	
	for i in range(COUNTDOWN_TIME, 0, -1):
		print(f"Shutdown in {i}...")
		time.sleep(1)
		
		if is_dev_mode():
			print("Development mode activated during countdown - shutdown CANCELEDS")
			return False
			
	print("Shutting down now...")
	return True
	
if __name__ == "__main__":
	result = safe_shutdown()
	print(f"Shutdown authorized: {result}")
