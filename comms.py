import requests, time
import numpy as np

token = "e1bb2f40e496aeb2fa5baf98d4671643"
user = "laughing123"

startingMoney = 1000

def main():
    coef = 1
    t = time.time()
    pairs =  requests.get("http://192.168.1.101:3000/getAllPairs")
    pairs = pairs.json()
    keys = list()
    for key, value in pairs.items():
        if "close_" in key:
            keys.append(key.split(",")[0][6:])
    
    keys = list(dict.fromkeys(keys))
    g = np.zeros((len(keys), len(keys)))
    volumes = np.zeros((len(keys), len(keys)))
    for i, (key, value) in enumerate(pairs.items()):
        x = key.split(",")[0][6:]
        y = key.split(",")[1]
        xi = keys.index(x)
        yi = keys.index(y)
        if "close_" in key:
            g[xi, yi] = value
        elif "volume_" in key:
            volumes[xi, yi] = value

    start = "USDT"
    startVolues = []
    for i, key in enumerate(keys):
        if volumes[keys.index(start), i] > 0:
            startVolues.append(tuple([volumes[keys.index(start), i], g[keys.index(start), i], keys[i]]))


    startVolues.sort(key=lambda x: x[0], reverse=True)

    considered = []
    middle = (len(startVolues) // 2) - 10
    for i in range(middle, middle + 20):
        considered.append(startVolues[i])

    
    for i in considered:
        money = 1000
        checkValues = []
        cof = i[1] / 10**8
        for j, key in enumerate(keys):
            if volumes[keys.index(i[2]), j] > 0:
                checkValues.append(tuple([volumes[keys.index(i[2]), j], g[keys.index(i[2]), j], keys[j]]))

        newValues = []
        for j in checkValues:
            cof *= j[1] / 10**8
            for k, key in enumerate(keys):
                if volumes[keys.index(j[2]), k] > 0:
                    newValues.append(tuple([volumes[keys.index(j[2]), k], g[keys.index(j[2]), k], keys[k]]))
            s = 0
            for k in newValues:
                if k[2] == start and j[2] != start:
                    cof *= k[1] / 10**8
                    s = cof
                    if s > 1:
                        print(i[2], i[1], i[0], j[2], j[1], j[0], k[2], k[1], k[0], s)
                        print("first price: ", (int(i[1]) / 10**8) * (int(i[0]) / 10 **8))
                        print("price: ", (int(i[1]) / 10**8) * (int(i[0]) / 10 **8) * (int(j[1]) / 10**8) * (int(j[0]) / 10 **8) * (int(k[1]) / 10**8) * (int(k[0]) / 10 **8))

                    break
            cof = i[1] / 10**8

        exit()

    print(time.time() - t)

    


def getPair():
    pass

def placeOrder(fr, to, amount):
    order = requests.get("http://192.168.1.101:3000/createOrders/" + user + "/" + token + "/" + fr + "," + to + "," + str(amount))
    print(order.json())


def getTime():
    pass



if __name__ == "__main__":
    main()