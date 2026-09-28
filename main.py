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

devices = []
status = []

def networkScan(ip):
    dott_position = ip.rfind(".")
    ip_end = ip[: dott_position + 1]
    print(ip_end)
    system = systemCheck()
    for i in range (1,255):
        ip = ip_end + str(i)
        print(ip)
        devices.append(ip)
        if system == "Windows":
            command = ["ping", "-n", "1", "-w", "1000", ip]
        else:
            command = ["ping", "-c", "1", "-W", "1", ip]
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )  
        if result.returncode == 0:
            devices.append('up')
            print("Urządzenie up")
        else:
            devices.append('down')
        print("run run")
        

networkScan(ip)
print(devices)
print(status)
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







