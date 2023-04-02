import grequests, time
import numpy as np

token = "98133b2b5fce90a2deacaadc513ea28b"
user = "laughing123"

startingMoney = 1000

def main():
    t = time.time()
    pairs =  requests.get("http://192.168.1.101:3000/getAllPairs").json()
    keys = list()
    for key, value in pairs.items():
        if "close_" in key:
            keys.append(key.split(",")[0][6:])
    keys = list(dict.fromkeys(keys))
    g = np.zeros((len(keys), len(keys)))
    volumes = np.zeros((len(keys), len(keys)))
    for i, (key, value) in enumerate(pairs.items()):
        y = key.split(",")[1]
        yi = keys.index(y)
        if "close_" in key:
            x = key.split(",")[0][6:]
            xi = keys.index(x)
            g[xi, yi] = value
        elif "volume_" in key:
            x = key.split(",")[0][7:]
            xi = keys.index(x)
            volumes[xi, yi] = value

    start = "USDT"
    startVolues = []
    for i, key in enumerate(keys):
        if volumes[keys.index(start), i] > 0:
            startVolues.append(tuple([volumes[keys.index(start), i], g[keys.index(start), i], keys[i]]))

    startVolues.sort(key=lambda x: x[0], reverse=True)
    considered = []
    mymodes = [107, 267]
    for i in (np.random.normal(0, 0.2, 20) * 107):
        considered.append(startVolues[mymodes[np.random.randint(0, 2)] + int(i)]) 

    mprices = []    
    for i in considered:
        checkValues = []
        coef = i[1]
        for j, key in enumerate(keys):
            if volumes[keys.index(i[2]), j] > 0:
                checkValues.append(tuple([volumes[keys.index(i[2]), j], g[keys.index(i[2]), j], keys[j]]))

        for j in checkValues:
            shopping = []
            shopping.append("USDT")
            coef *= j[1]
            for k, key in enumerate(keys):
                if volumes[keys.index(j[2]), k] > 0 and keys[k] == start:
                    shopping.append(i[2])
                    shopping.append(j[2])
                    shopping.append(keys[k])
                    endVolume = volumes[keys.index(j[2]), k]
                    endPrice = g[keys.index(j[2]), k]
                    break
            
            prices = []
            p = (10 * 10**8) // i[1]
            if p > i[0] // 10**8:
                p = i[0] // 10**8
            if len(shopping) > 1:
                d = ((p * 10**8) // j[1])
                if d > j[0] // 10**8:
                    d = j[0] // 10**8
                f = ((d * 10**8) // endPrice)
                if f > endVolume // 10**8:
                    f = endVolume // 10**8
                prices.append(int(p * 10 ** 8))
                prices.append(int(d * 0.9 * 10 ** 8))
                prices.append(int(f * 10 ** 8))
                for s in shopping:
                    prices.append(s)
                if(f > 50):
                    mprices.append(prices)
                coef *= endPrice
                if 0 not in prices and endPrice > 0:
                    placeOrder(shopping[0], shopping[1], int(p * 10 ** 8))

            coef = i[1] // 10**8
        
    print(time.time() - t)


def getPair(fr, to):
    pair = grequests.get("http://192.168.1.101:3000/getPairs/" + fr + "," + to)
    return pair.json()

def placeOrder(fr, to, amount):
    print(fr, to, amount)
    order = requests.get("http://192.168.1.101:3000/createOrders/" + user + "/" + token + "/" + fr + "," + to + "," + str(amount))
    print(order.json())

def fallSafe():
    r = requests.get("http://192.168.1.101:3000/balance/" + user).json()
    for i in r.keys():
        if i != "USDT" and r[i] > 0:
            placeOrder(i, "USDT", r[i])

def placeOrders(fr, amount):
    newfr = []
    for i in range(len(fr)):
        if i + 1 < len(fr):
            newfr.append(fr[i] + "," + fr[i + 1])
    s = ""
    for i in range(len(newfr)):
        k = newfr[i].split(",")[0]
        h = newfr[i].split(",")[1]
        s += k + "," + h + "," + str(amount[i]) + "|"

if __name__ == "__main__":
    while(True):
        r = requests.get("http://192.168.1.101:3000/getTime").json()
        fallSafe()