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
        if "close_" in key:
            x = key.split(",")[0][6:]
            y = key.split(",")[1]
            xi = keys.index(x)
            yi = keys.index(y)
            g[xi, yi] = value
        elif "volume_" in key:
            x = key.split(",")[0][7:]
            y = key.split(",")[1]
            xi = keys.index(x)
            yi = keys.index(y)
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
        checkValues = []
        for j, key in enumerate(keys):
            if volumes[keys.index(i[2]), j] > 0:
                checkValues.append(tuple([volumes[keys.index(i[2]), j], g[keys.index(i[2]), j], keys[j]]))
        print(i[0] // 10**8, i[1] / 10**8, i[2])
        print("#")
        for j in checkValues:
            print(j[0] // 10**8, j[1] / 10**8, j[2])
        print("---")
        
    
    # sort by volume
    """ startVolues.sort(key=lambda x: x[0], reverse=True)

    inverseValues = []
    for i, key in enumerate(keys):
        if volumes[i, keys.index(start)] > 0:
            inverseValues.append(tuple([volumes[i, keys.index(start)], g[i, keys.index(start)], keys[i]]))
    
    inverseValues.sort(key=lambda x: x[0], reverse=True)

    firstValue = startVolues[len(startVolues) // 2]
    coef *= firstValue[1] / 10**8
    print(firstValue)

    checkValue = firstValue[2]
    print(checkValue)
    print(coef)
    checkValues = []
    for i, key in enumerate(keys):
        if volumes[keys.index(checkValue), i] > 0:
            checkValues.append(tuple([volumes[keys.index(checkValue), i], g[keys.index(checkValue), i], keys[i]]))

    checkValues.sort(key=lambda x: x[1], reverse=True)
    print(checkValues)
    marked = ""
    for i in checkValues:
        if i[2] != start:
            coef *= i[1] / 10**8
            marked = i[2]
            break

    print(marked)
    print(coef)
    finalVolues = []
    for i, key in enumerate(keys):
        if volumes[keys.index(marked), i] > 0:
            finalVolues.append(tuple([volumes[keys.index(marked), i], g[keys.index(marked), i], keys[i]]))

    finalVolues.sort(key=lambda x: x[0], reverse=True)
    for i in finalVolues:
        if i[2] == start:
            coef *= i[1] / 10**8
            break

    print(coef) """
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