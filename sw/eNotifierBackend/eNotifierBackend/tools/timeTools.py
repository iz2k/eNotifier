import datetime
import subprocess
from datetime import datetime

import pytz
from babel.localtime import get_localzone

def getTimeZoneAwareNow(timezone):
    t_utc = datetime.utcnow()
    t_loc = pytz.timezone("UTC").localize(t_utc)
    t_norm = timezone.normalize(t_loc)
    return t_norm


def getNow():
    timezone = get_localzone()
    return getTimeZoneAwareNow(timezone)

def getDateTime():
    timezone = get_localzone()
    now = getTimeZoneAwareNow(timezone)
    return {'year': now.year,
            'month': now.month,
            'day': now.day,
            'hour': now.hour,
            'minute': now.minute,
            'second': now.second,
            'timezone': str(timezone)}

def setTimeZone(timezone):
    #cmd = 'sudo raspi-config nonint do_change_timezone ' + timezone
    cmd = 'sudo timedatectl set-timezone ' + timezone
    subprocess.run(cmd.split(), capture_output=True, text=True)
    print('Timezone set to: ' + str(timezone) + ' (' + str(getTimeZoneAwareNow(pytz.timezone(timezone))) + ')')
