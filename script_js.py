### pip install influxdb-client


import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

info = {
  "01": ("Rue Jules Ferry - Gare Saint-Roch","12","43.605366","3.881346"),
  "02": ("Comédie","24","43.608148","3.878778"),
  "03": ("Esplanade","32","43.609478","3.881293"),
  "04" : ("Hôtel de Ville","16","43.599088","3.894866"),
  "05" : ("Corum","12","43.613989","3.8816"),
  "06" : ("Place Albert 1er - St Charles","27","43.616768","3.873375"),
  "07" : ("Foch","8","43.610989","3.873345"),
  "08" : ("Halles Castellane","12","43.609935","3.877208"),
  "09" : ("Observatoire","8","43.606081","3.876931"),
  "10" : ("Rondelet","16","43.603038","3.875796"),
  "11" : ("Plan Cabanes","12","43.608491","3.868389"),
  "12" : ("Boutonnet","12","43.622629","3.868375"),
  "13" : ("Emile Combes","8","43.616742","3.87998"),
  "14" : ("Beaux-Arts","28","43.616698","3.884981"),
  "15" : ("Les Aubes","8","43.618692","3.893844"),
  "16" : ("Antigone centre","16","43.607942","3.890634"),
  "17" : ("Médiathèque Emile Zola","16","43.608218","3.89314"),
  "18" : ("Nombre d'Or","16","43.607859","3.886644"),
  "19" : ("Louis Blanc","16","43.614642","3.877648"),
  "20" : ("Gambetta","8","43.607106","3.870693"),
  "21" : ("Port Marianne","16","43.60032","3.89851"),
  "22" : ("Clemenceau","12","43.603539","3.872394"),
  "23" : ("Les Arceaux","16","43.611991","3.867157"),
  "24" : ("Cité Mion","8","43.601143","3.884373"),
  "25" : ("Nouveau Saint-Roch","8","43.599817","3.875757"),
  "26" : ("Renouvier","8","43.603553","3.867884"),
  "27" : ("Odysseum","8","43.603727","3.918979"),
  "28" : ("Saint-Denis","8","43.605021","3.875065"),
  "29" : ("Richter","16","43.603424","3.899263"),
  "30" : ("Charles Flahault","8","43.618762","3.865971"),
  "31" : ("Voltaire","8","43.603767","3.888659"),
  "32" : ("Prés d'Arènes","8","43.59048","3.884611"),
  "33" : ("Garcia Lorca","8","43.590757","3.890616"),
  "34" : ("Vert Bois","0","43.63458","3.86823"),
  "35" : ("Malbosc","8","43.633679","3.832861"),
  "36" : ("Occitanie","32","43.634242","3.849128"),
  "37" : ("FacdesSciences","24","43.631018","3.860697"),
  "38" : ("Fac de Lettres","16","43.630665","3.87023"),
  "39" : ("Aiguelongue","8","43.626163","3.882492"),
  "40" : ("Jeu de Mail des Abbés","8","43.619701","3.883831"),
  "41" : ("Euromédecine","8","43.639119","3.828199"),
  "42" : ("Marie Caizergues","8","43.619871","3.873812"),
  "43" : ("Sabines","8","43.584211","3.860031"),
  "44" : ("Celleneuve","8","43.61467","3.832624"),
  "45" : ("Jardin de la Lironde","8","43.60585","3.911576"),
  "46" : ("Père Soulas","8","43.621983","3.855603"),
  "47" : ("Place Viala","8","43.616812","3.855075"),
  "48" : ("Hôtel du Département","8","43.621682","3.83477"),
  "49" : ("Tonnelles","8","43.615155","3.839466"),
  "50" : ("Parvis Jules Ferry - Gare Saint-Roch","8","43.603889","3.879362"),
  "51" : ("Pont de Lattes - Gare Saint-Roch","12","43.606036","3.882393"),
  "53" : ("Deux Ponts - Gare Saint-Roch","8","43.604319","3.880916"),
  "54" : ("Providence - Ovalie","8","43.588239","3.853421"),
  "55" : ("Pérols Etang de l'Or","68","43.558351","3.963412"),
  "56" : ("Albert 1er - Cathédrale","12","43.614005","3.873218"),
  "57" : ("Saint-Guilhem - Courreau","8","43.608996","3.872752"),
  "59" : ("Sud De France","8","43.59562","3.9235"),
}


bucket = "SAE-12"
org = "iut-students"
token = "<INFLUX-TOKEN>"
# Store the URL of your InfluxDB instance
url = "http://188.166.151.235:8086/"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

write_api = client.write_api(write_options=SYNCHRONOUS)

velo = ["STATION_STATUS"]
j = 1

for parking in velo:
  print(f"Working on {parking}...", end=" ")
  with open(f"./in/stats/csv/{parking}.CSV", "rt", encoding="utf-8") as fin:
    print("Parsing, please wait...", end="")
    fin = fin.readlines()[1:]
    print("The current size of the file is:", len(fin), "lines.")
    for i in range(0, len(fin)):
      data = fin[i].strip().split(",")

      if len(data) > 1:
        ### CSV Header: name,date,export_date,opened,free_places,places
        ### CSV id,date,nbr_available,nbr_disabled,docks_available,is_installed,is_renting,is_returning
        ### CSV id,name,places,lat,lon
        db = {
          "id": data[0],
          "export_date": int(data[1]),
          "availability": int(data[2]),
          "nbr_disabled": bool(data[3]),
          "docks_available": int(data[4]),
          "is_installed" : int(data[5]),
          "is_renting" : int(data[6]),
          "is_returning" : int(data[7]),
        }

        velib_infos = info[f"{db['id'][1:]}"]
        p = influxdb_client.Point(db["id"])
        timestamp_to_date_time = datetime.datetime.fromtimestamp(db["export_date"]).strftime('%Y-%m-%dT%H:%M:%S,%f')

        p.field("name", velib_infos[0])
        p.field("lat", velib_infos[2])
        p.field("lon",velib_infos[3])
        p.field("export_date", db["export_date"])
        p.field("availability", db["availability"])
        p.field("nbr_disabled",db["nbr_disabled"])
        p.field("docks_available", db["docks_available"])
        p.field("is_installed",db["is_installed"])
        p.field("is_renting",db["is_renting"])
        p.field("is_returning", db["is_returning"])

        p.time(timestamp_to_date_time)
        write_api.write(bucket=bucket, org=org, record=p)

        print("ligne : ",i)
        j = j + 1
        if j == 60 : 
          j = 1