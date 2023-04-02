import numpy as np
import grequests, requests, time

token = "19873d374f44debc235eda76d7cde231"
user = "laughing123"
money = 1000

visited = []

def trading():
    t = time.time()
    r =  requests.get("http://192.168.1.101:3000/getAllPairs")
    if r.status_code != 200:
        return
    pairs = r.json()
    keys = list()
    startingNode = "USDT"
    for key, value in pairs.items():
        if "close_" in key:
            keys.append(key.split(",")[0][6:])
    keys = list(dict.fromkeys(keys))
    prices = np.zeros((len(keys), len(keys)))
    volumes = np.zeros((len(keys), len(keys)))
    for i, (key, value) in enumerate(pairs.items()):
        y = keys.index(key.split(",")[1])
        x = keys.index(key.split(",")[0].split("_")[1])
        if "close_" in key:
            prices[x, y] = value
        elif "volume_" in key:
            volumes[x, y] = value

    startingVolumes = []
    for i, key in enumerate(keys):
        if volumes[keys.index(startingNode), i] > 0:
            startingVolumes.append(tuple([volumes[keys.index(startingNode), i], prices[keys.index(startingNode), i], keys[i]]))

    startingVolumes.sort(key=lambda x: x[2], reverse=True)
    
    considered = startingVolumes
    r = requests.get("http://192.168.1.101:3000/balance/" + user)
    if r.status_code != 200:
        return
    startingMoney = r.json()["USDT"]
    if startingMoney > 100:
        amountPerConsideration = int(startingMoney / len(considered))
        for i in considered:
            trade(startingNode, i[2], amountPerConsideration)
    else:
        r = requests.get("http://192.168.1.101:3000/balance/" + user)
        if r.status_code != 200:
            return
        bought = []
        for i in r.json():
            if r.json()[i] > 0:
                bought.append(tuple([i, r.json()[i]]))

        for i in bought:
            if i[0] != "USDT":
                findNext(i, i[1])
        

    print(time.time() - t)

def trade(parent, child, amount):
    s = parent + "," + child + "," + str(amount)
    r = requests.get("http://192.168.1.101:3000/createOrders/" + user + "/" + token + "/" + s)
    if r.status_code == 200:
        requests.get("http://192.168.1.101:3000/balance/" + user)
    return r

def findNext(data, amount):
    r =  requests.get("http://192.168.1.101:3000/getAllPairs")
    if r.status_code != 200:
        return
    pairs = r.json()
    keys = list()
    for key, value in pairs.items():
        if "close_" in key:
            keys.append(key.split(",")[0][6:])

    keys = list(dict.fromkeys(keys))
    prices = []
    volumes = []
    for i, (key, value) in enumerate(pairs.items()):
        y = keys.index(key.split(",")[1])
        x = keys.index(key.split(",")[0].split("_")[1])
        if "close_" in key:
            prices.append(tuple([keys[x], keys[y], value]))
        elif "volume_" in key:
            volumes.append(tuple([keys[x], keys[y], value]))

    considered = []
    for i in prices:
        if i[0] == data[0]:
            considered.append(i)

    considered.sort(key=lambda x: x[2], reverse=True)
    trade(data[0], considered[0][1], amount)

def findNext2(data, amount):
    r =  requests.get("http://192.168.1.101:3000/getAllPairs")
    if r.status_code != 200:
        return
    pairs = r.json()
    keys = list()
    for key, value in pairs.items():
        if "close_" in key:
            keys.append(key.split(",")[0][6:])
    keys = list(dict.fromkeys(keys))
    prices = np.zeros((len(keys), len(keys)))
    volumes = np.zeros((len(keys), len(keys)))
    for i, (key, value) in enumerate(pairs.items()):
        y = keys.index(key.split(",")[1])
        x = keys.index(key.split(",")[0].split("_")[1])
        if "close_" in key:
            prices[x, y] = value
        elif "volume_" in key:
            volumes[x, y] = value

    considered = []
    for i, key in enumerate(keys):
        if volumes[keys.index(data), i] > 0:
            if keys[i] == "USDT":
                s = data + "," + keys[i] + "," + str(amount * 10 ** 8)
                r = requests.get("http://192.168.1.101:3000/createOrders/" + user + "/" + token + "/" + s)
                if r.status_code == 200:
                    return
            considered.append(tuple([volumes[keys.index(data), i], prices[keys.index(data), i], keys[i]]))

    considered.sort(key=lambda x: x[2], reverse=True)
    for i in considered:
        if i[2] != "USDT" and i[2] not in visited:
            visited.append(i[2])
            s = data + "," + i[2] + "," + str(amount)
            r = requests.get("http://192.168.1.101:3000/createOrders/" + user + "/" + token + "/" + s)
            if r.status_code == 200:
                return

def fallSafe():
    r = requests.get("http://192.168.1.101:3000/balance/" + user).json()
    for i in r:
        if i != "USDT" and r[i] > 0:
            if trade(i, "USDT", r[i]) != 200:
                findNext2(i, r[i])
   
    

if __name__ == "__main__":

    while True:
        fallSafe()

    while True:
        trading()