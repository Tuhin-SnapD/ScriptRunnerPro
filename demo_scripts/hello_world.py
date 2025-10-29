# Demo Python script for Script Runner Pro
"""
Demo Python script for Script Runner Pro
"""

import sys
import time

print("Hello from Script Runner Pro!")
print(f"Python version: {sys.version}")
print(f"Platform: {sys.platform}")

for i in range(5):
    print(f"Countdown: {5-i}")
    time.sleep(1)

print("Script completed successfully!")
