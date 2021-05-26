import time
import subprocess
import sqlite3 as sql
import psutil

def db_create():
    try:
        db_cur.execute("CREATE TABLE cpu (time INTEGER, cpu1 REAL, cpu5 REAL, cpu15 REAL, netRcv INTEGER, netSnt	INTEGER, ramT	INTEGER, ramU	INTEGER, ramF INTEGER, ramS INTEGER, ramC INTEGER, ramA INTEGER, swpT INTEGER, swpU INTEGER, swpF INTEGER, temp REAL);")

    except Exception:
        pass

def db_insert(table, columns, values):
    try:
        db_cur.execute("INSERT INTO {} ({}) VALUES {}".format(table, columns, str(tuple(values))))
        db_conn.commit()

    except Exception as err:
        print("SQlite error: ", err)

def terminal(cmd):
    if " " in cmd:
        cmd = cmd.split()
    
    out = subprocess.run(cmd, stdout=subprocess.PIPE)
    return out.stdout.decode("utf-8")

def get_cpu():
    out = terminal("uptime")
    values = []

    if "load average:" in out:
        a = out.find("load average:") + 14
        b = float(out[a:a+4].replace(',', '.')) * 100.0; a += 6
        c = float(out[a:a+4].replace(',', '.')) * 100.0; a += 6
        d = float(out[a:a+4].replace(',', '.')) * 100.0

        values.append(b)
        values.append(c)
        values.append(d)

    return values

def get_mem():
    out = terminal("free")
    out = " ".join(out.split()).split()
    values = []

    if "total" in out:
        values.append(out[7]) #RAM Total
        values.append(out[8]) #RAM Used
        values.append(out[9]) #RAM Free
        values.append(out[10])#RAM Shared
        values.append(out[11])#RAM Cache
        values.append(out[12])#RAM Available
        values.append(out[14])#Swap Total
        values.append(out[15])#Swap Used
        values.append(out[16])#Swap Free

    return values

def get_network(interface):
    values = []

    if (interface is None):
        values.append(psutil.net_io_counters().bytes_recv)
        values.append(psutil.net_io_counters().bytes_sent)
    else:
        x = psutil.net_io_counters(pernic=True)
        x = str(x.get(interface)).split(", ")
        tx = str(x[0]).split("=")[1]
        rx = str(x[1]).split("=")[1]

        values.append(rx)
        values.append(tx)
    
    return values

def get_temp(device):
    temp = -1

    if device is None:
        x = str(psutil.sensors_temperatures().get("coretemp")[0])
        x = x.split(", ")[1]
        x = x.split("=")[1]
        temp = x
    
    elif 'raspberry' in device:
        out = terminal('vcgencmd measure_temp').split("=")
        temp = out[1].split("'")[0]

    return temp



db_conn = sql.connect('/dev/shm/cpu_stats.db')
db_cur  = db_conn.cursor()
db_create()


while 1:
    data = [int(time.time())]
    data.extend(get_cpu())
    data.extend(get_network(None))#None for all interfaces or name (str) of specific interface, like 'eth0'
    data.extend(get_mem())
    data.append(get_temp(None))#None for common computers, 'raspberry' for any Raspberry PI.

    db_insert("cpu", "time, cpu1, cpu5, cpu15, netRcv, netSnt, ramT, ramU, ramF, ramS, ramC, ramA, swpT, swpU, swpF, temp", data)
    time.sleep(60)

