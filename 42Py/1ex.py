import time
from datetime import datetime

Present_time=datetime.now()
epoch_time = time.time()
print(f"Seconds since Janurary 1, 1970: {epoch_time:,.4f}or {epoch_time:.2e} in scientific notation")
print(Present_time.strftime("%b %d %Y"))