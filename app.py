from flask import Flask, render_template
import os
import _thread
import time
import datetime
import matplotlib.pyplot as plt
import gc

app = Flask(__name__)

a = []
res = []
flag = True

def hs(s):
    res = 0
    mod = 1000000007
    for c in s:
        res = (res * 233 + ord(c)) % mod
    return str(res)

def byStr(t):
    return t[1][0]

def square(a):
    return [i ** 0.5 for i in a]

def updateFigure():
    fig, ax = plt.subplots(1, figsize=(9, 4))

    tot = int(time.strftime('%d', time.localtime()))
    xt = []
    yt = []
    for i in range(tot + 1):
        yt += [0]
        xt += [i]
    for i in res:
        y = [0 for _ in range(tot + 1)]
        for itm in i[1]:
            t = int(time.strftime('%d', time.strptime(itm[0: 19], '%Y-%m-%d %H:%M:%S')))
            y[t] += 1
        y = square(y)
        for j in range(tot + 1):
            yt[j] += y[j]
        ax.fill_between(xt[1:], y[1:], 0,
                 facecolor="orange",
                 color='orange',
                 alpha=0.1)
    ax.plot(xt[1:], yt[1:], 'b-', label='Sum of Sqrt')
    ax.set_ylabel('Square Root of Commit Numbers')
    ax.set_xlabel('Date Number in July 2020')
    ax.set_title('Commit Statistics')
    ax.legend()

    fig.savefig('static/graph.png',dpi=800,format='png')

    del fig
    del ax

def update():
    global a, res, t, flag
    flag = True
    with open('urls.txt', 'r') as f:
        a = f.read().split('\n')
        a.remove('')
    _res = []
    for url in a:
        if url == '' or url[0] == '#':
            continue;
        h = hs(url)
        if not os.path.exists(h):
            os.system('mkdir ' + h + '; cd ' + h + '; git clone ' + url + r';')
        os.system('cd ' + h + r'/*; git fetch --all; git reset --hard origin/master; git pull; git log --pretty=format:"%ad: %s" --date=format:"%Y-%m-%d %H:%M:%S" > ../log.txt')
        with open(h + r'/log.txt', 'r') as f:
            _res.append((url, f.read().split('\n')))
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    res = sorted(_res, key=byStr)
    res.reverse()
    
    del _res

    updateFigure()
    gc.collect()

    flag = False
    time.sleep(600) # collect data every 10 minutes.

def backend():
    while True:
        update()

@app.route('/')
def root():
    if flag:
        return render_template('error.html')
    return render_template('index.html', res=res, time=t)

_thread.start_new_thread(backend, ())

if __name__ == '__main__':
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # app.run(host='0.0.0.0', port=5000)
    app.run()
