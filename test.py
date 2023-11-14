from datetime import datetime
from pytz import timezone
now=datetime.now()
if not now:
    now=datetime.now()
kr_timezone = timezone('Asia/Seoul')
now_kr = now.astimezone(kr_timezone)
print(now_kr)