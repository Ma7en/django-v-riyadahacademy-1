# 
from django.test import TestCase




# 
import requests
import threading





# Create your tests here.
# ******************************************************************************
# ==============================================================================
def send_request():
    response = requests.get('http://127.0.0.1:8000/api/v1/admin-dashboard-stats/')
    print(response.status_code)

threads = []
for i in range(1000):
    thread = threading.Thread(target=send_request)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()