#importy 
from flask import Flask, jsonify, render_template
import socket
import speedtest

print('Witaj, jestem Turkuć Podjadek i lubię podjadać pakiety sieciowe...')
print('Za chwilę otrzymasz dostęp do panelu webowego')

#odczyt socketu - ip i hostname
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
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
        "hostname": hostname,
        "ip": ip,
        "ping": ping,
        "download": download,
        "upload": upload
    }
    return jsonify(data)


app.run(host="127.0.0.1", port=80)







