### pip install influxdb-client

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "parkings"
org = "iut-students"
token = "cr1JIiLzE1dHRU3f-cJIRMczkYKPNwDiZpu-Eni8wpPE4-Dzi1SXyJ5-E7vqlB4R50RXlNQp9e9jopqdf3S_Ow=="
# Store the URL of your InfluxDB instance
url = "http://188.166.151.235:8086/"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

write_api = client.write_api(write_options=SYNCHRONOUS)

parkings = [
  'FR_MTP_ANTI', 'FR_MTP_COME', 'FR_MTP_CORU', 'FR_MTP_EURO', 'FR_MTP_FOCH',
  'FR_MTP_GAMB', 'FR_MTP_GARE', 'FR_MTP_TRIA', 'FR_MTP_ARCT', 'FR_MTP_PITO',
  'FR_MTP_CIRC', 'FR_MTP_SABI', 'FR_MTP_GARC', 'FR_MTP_SABL', 'FR_MTP_MOSS',
  'FR_STJ_SJLC', 'FR_MTP_MEDC', 'FR_MTP_OCCI', 'FR_CAS_VICA', 'FR_MTP_GA109',
  'FR_MTP_GA250', 'FR_CAS_CDGA', 'FR_MTP_ARCE', 'FR_MTP_POLY'
]

for parking in parkings:
  print(f"Working on {parking}...", end=" ")
  with open(f"./out/csv/{parking}.csv", "rt", encoding="utf-8") as fin:
    print("Parsing, please wait...", end="")
    fin = fin.readlines()[1:]
    print("The current size of the file is:", len(fin), "lines.")
    for i in range(0, len(fin)):
      if fin[i] != "name,date,date,opened,free_places,places\n":
        data = fin[i].strip().split(",")

        if data[0] != "":
          if len(data) > 1:
              ### CSV Header: name,date,export_date,opened,free_places,places
              db = {
              "name": data[0],
              "export_date": data[1],
              "real_date": data[2],
              "is_opened": bool(data[3]),
              "availability": int(data[4]),
              "capacity": int(data[5])
              }

              p = influxdb_client.Point(db["name"])

              p.field("export_date", db["export_date"])
              p.field("real_date", db["real_date"])
              p.field("is_opened", db["is_opened"])
              p.field("availability", db["availability"])
              p.field("capacity", db["capacity"])
              p.time(db["real_date"])
              write_api.write(bucket=bucket, org=org, record=p)
