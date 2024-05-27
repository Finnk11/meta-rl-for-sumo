import json
import matplotlib.pyplot as plt
# To read data from file:
delays = json.load(open("../data/json/delays.json"))

print(len(delays))
print(type(delays[0]))


print('max:', max(delays))
print('min:', min(delays))


def greater_cnt(t):
    greater_cnt = 0
    for d in delays:
        if d > t:
            greater_cnt = greater_cnt+1
    return greater_cnt

print(greater_cnt(150))

xTimes = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180]

yProbs = []
for t in xTimes:
    gc = greater_cnt(t)
    yProbs.append(float(gc)/len(delays))

print(yProbs)



fig, ax = plt.subplots()
ax.plot(xTimes, yProbs, '-bo', linewidth=3.0)
ax.legend(['Fixed', 'Second List'], loc='upper right')
ax.set(xlabel='t(s)', ylabel='P(Delay>t)')

plt.suptitle('Delay tail distribution with dynamic arrival with peak=0.4.')

plt.show()