#importy 
from flask import Flask, jsonify, render_template
import socket
import speedtest
import time

print('Witaj, jestem Turkuć Podjadek i lubię podjadać pakiety sieciowe...')
print('Za chwilę otrzymasz dostęp do panelu webowego')

#odczyt socketu - ip i hostname
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

ip = s.getsockname()[0]

s.close()

#speedtest
st = speedtest.Speedtest()
download = st.download() / 1000000
download = download / 8
download = round(download, 2)
upload = st.upload() / 1000000
upload = upload / 8
upload = round(upload, 2)
ping = st.results.ping



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







