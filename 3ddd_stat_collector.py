
import json
import time
import os
from datetime import datetime
from login import driver
    
try:
    import parse2
except Exception as exc:
    print(exc)
    driver.execute_script(
        f'console.log("{exc}")'
    )
    list_json = os.listdir(path='dates/')
   
    if(os.path.isfile(f'{datetime.now().strftime("%d.%m.%y")}.csv')):
        os.remove(f'{datetime.now().strftime("%d.%m.%y")}.csv')

time.sleep(2**20)
