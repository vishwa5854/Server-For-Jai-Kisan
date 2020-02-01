import socket
import requests


def restless():
    s = socket.socket()
    s.bind(('localhost', 5854))
    s.listen()
    c, addr = s.accept()

    while True:
        receivedData = c.recv(4096).decode()
        requestCode = receivedData[0]
        if requestCode == "1":
            print(receivedData[2:len(receivedData) - 1])
            n, p = receivedData[2:len(receivedData)].split(",")
            print(n)
            print(p)
            data = str(signIn(n, p))
            b = bytearray(str(len(data)) + data, 'utf-8')
            c.send(b)
            c.close()
            s.close()
        if requestCode == "2":
            n, p = receivedData[2:len(receivedData)].split(",")
            signUp(n, p)
            data = "successful"
            b = bytearray(str(len(data)) + data, 'utf-8')
            c.send(b)
            c.close()
            s.close()
        if requestCode == "3":
            # weather forecast
            weather_forecast()

        s = socket.socket()
        s.bind(('', 5854))
        s.listen()
        c, addr = s.accept()


def signIn(name, phone):
    a = open("userCredentials.txt", "r")
    names = []
    phones = []
    p = a.readlines()
    for i in p:
        n, p = i.split(",")
        names.append(n)
        phones.append(p)
    print(names)
    print(phones)
    a.close()
    return names.__contains__(name) and phones.__contains__(phone)


def weather_forecast():
    api = "f5313b63fb4204670924c86d2fd950c1"
    url = "http://api.openweathermap.org/data/2.5/weather?"
    city = input("Enter city name : ")
    complete_url = url + "appid=" + api + "&q=" + city
    response = requests.get(complete_url)
    print(complete_url)
    x = response.json()
    if x["cod"] != "404":
        print(x)

    else:
        print(" City Not Found ")


def signUp(name, phone):
    a = open("userCredentials.txt", "a")
    a.write("\n" + name + "," + phone)
    print('new user ' + name + ' successfully created')
    a.close()


try:
    restless()
except ConnectionResetError:
    restless()
