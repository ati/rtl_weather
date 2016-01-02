#!/usr/bin/python -u

import sys
import sqlite3
from MS5611 import MS5611

NEW_RECORD_TO=10 # min seconds between 2 consecutive records
ELEVATION=173 # meters above sea level

sensor = MS5611()
sensor.setElevation(ELEVATION)

conn = sqlite3.connect("weather.sqlite3")
conn.row_factory = sqlite3.Row
sql = conn.cursor()

# Weather Sensor THGR122N RC ae Channel 1 Temp: 24.4C  75.9F   Humidity: 41%
# Weather Sensor THGR122N RC ae Channel 1 Temp: 24.4C  75.9F   Humidity: 41%
#
def process_line(line):
  print line
  fields = line.split()
  if (len(fields) > 10 and fields[2] == "THGR122N"):
    res = sql.execute("SELECT CAST(strftime('%s', CURRENT_TIMESTAMP) as integer) - CAST(strftime('%s', created_at) as integer) AS age FROM oregons ORDER BY ID DESC LIMIT 1").fetchall()
    if (not res or res[0]['age'] > NEW_RECORD_TO):
      sensor.read()
      values = (int(fields[4], 16), int(fields[6]), float(fields[8][:-1]), float(fields[11][:-1]), float(sensor.getPressureAdj()))
      print "new record: ", values
      sql.execute("INSERT INTO oregons(battery, channel, temperature, humidity, pressure) VALUES(?,?,?,?,?)", values)
      conn.commit()

try:
  buff = ''
  while True:
    buff += sys.stdin.read(1)
    if buff.endswith('\n'):
      process_line(buff[:-1])
      buff = ''
except KeyboardInterrupt:
  sys.stdout.flush()
finally:
  conn.close()
