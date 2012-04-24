import pyl
import random
import time


def main():
    pylab.ion()       # Turn on interactive mode.
    pylab.hold(False) # Clear the plot before adding new data.
    x = range(10)
    for i in range(10):
        y = random.sample(xrange(100), 10)
        pylab.plot(x, y)
        time.sleep(1)


if __name__ == '__main__':
    main()