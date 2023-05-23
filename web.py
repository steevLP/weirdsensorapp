# downloads all required data from target server
import os
import requests


def fetchData(date, sensor, dir):
    # 404 Data response
    empty = '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">'

    # downloads files from sensor.community
    if not os.path.exists("./data/" + str(date) + "-3659.csv"):

        # send request to server
        r = requests.get("https://archive.sensor.community/" + str(date) + "/" + str(date) + "_sds011_sensor_"+sensor+".csv", allow_redirects=False)

        # read the first line of incoming data to determin if it is invalid or not
        if r.content.decode("utf-8").split("\n")[0] != empty:
            # write data to file
            open(dir + str(date) + "-"+sensor+".csv", 'wb').write(r.content)