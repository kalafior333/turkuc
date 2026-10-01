#importy 
from flask import Flask, jsonify, render_template
import socket
import speedtest
import time
import subprocess
import platform

print('Witaj, jestem Turkuć Podjadek i lubię podjadać pakiety sieciowe...')
print('Za chwilę otrzymasz dostęp do panelu webowego')

#odczyt socketu - ip i hostname
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

ip = s.getsockname()[0]

s.close()

def systemCheck():
    system = platform.system()
    return system

#funkcja poszukująca inne urządzenia w sieci wykorzystując ping i tablicę arp
def networkScan(ip):
    #szybkie liczenie sieci - 255 w ostatnim oktecie - do poprawy!!
    dott_position = ip.rfind(".")
    ip_end = ip[: dott_position + 1]
    print(ip_end)
    system = systemCheck()
    for i in range (1,255):
        ip = ip_end + str(i)
        print(ip)
        #najpierw pingujemy wszystkie devices żeby wykonał się wpis do
        if system == "Windows":
            command = ["ping", "-n", "1", "-w", "1000", ip]
        else:
            command = ["ping", "-c", "1", "-W", "1", ip]
        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    result = subprocess.run(
        ["arp", "-a"],
        capture_output=True,
        text=True
    )
    lines = result.stdout.splitlines()
    devices = []

    for line in lines:
        parts = line.split()

        if len(parts) == 3 and parts[2] == "dynamic":
            ip = parts[0]
            mac = parts[1]

            devices.append({
                "ip": ip,
                "mac": mac
            })

    print(devices)
    return devices
        

net_scan_result = networkScan(ip)
#speedtest
#st = speedtest.Speedtest()
#download = st.download() / 1000000
#download = download / 8
#download = round(download, 2)
#upload = st.upload() / 1000000
#upload = upload / 8
#upload = round(upload, 2)
#ping = st.results.ping
download = 1
upload = 1
ping = 1


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/network/status1")
def status1():
    data = {
        "hostname": "Huawei P8 Lite",
        "ip": ip,
        "ping": ping,
        "download": download,
        "upload": upload
    }
    return jsonify(data)

@app.route("/api/network/ping")
def network_ping():
    target = ("8.8.8.8", 53)
    start = time.perf_counter()

    try:
        with socket.create_connection(target, timeout=3):
            elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

        return jsonify({"ping": elapsed_ms})

    except OSError:
        return jsonify({"ping": None, "error": "Brak połączenia z 8.8.8.8:53"}), 503


app.run(host="127.0.0.1", port=5000)







