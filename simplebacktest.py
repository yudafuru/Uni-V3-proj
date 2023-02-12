import math


def calc_tick(rp):
    # P = 1.0001 ^ i
    # sqrt(P) = 1.0001 ^ (i / 2)
    # i = log(sqrt(P)) * 2 / log(1.0001)
    return (math.log(rp) * 2) / math.log(1.0001)


def calc_sqrt_price(i):
    # sqrt(P) = 1.0001 ^ (i / 2)
    return math.pow(1.0001, i/2)


def swap(offered_y, x, y):
    delta_y = offered_y
    liquidity = math.sqrt(x * y)
    delta_sqrt_price = delta_y / liquidity
    sqrt_price = math.sqrt(y / x)
    tick_start = math.floor(calc_tick(sqrt_price))
    tick_finish = math.floor(calc_tick(sqrt_price + delta_sqrt_price))
    diff = tick_finish - tick_start
    delta_x = 0
    for tick in range(0, diff):
        # calculate the delta_sqrt_price
        tick_sqrt_price = calc_sqrt_price(tick_start + tick + 1)
        delta_sqrt_price = tick_sqrt_price - sqrt_price
        inverse_delta_sqrt_price = (1 / sqrt_price) - (1 / tick_sqrt_price)
        # check how much y is left to swap
        if delta_y - (delta_sqrt_price * liquidity) > 0:
            delta_y -= (delta_sqrt_price * liquidity)
            delta_x += (liquidity * inverse_delta_sqrt_price)
        else:
            # delta_y is exhausted for the integer value of tick
            break
    # apply the same logic for an exchange within adjacent tick
    if delta_y > 0:
        delta_sqrt_price = delta_y / liquidity
        fractional_tick = calc_tick(sqrt_price + delta_sqrt_price)
        tick_sqrt_price = calc_sqrt_price(fractional_tick)
        inverse_delta_sqrt_price = (1 / sqrt_price) - (1 / tick_sqrt_price)
        delta_x += (liquidity * inverse_delta_sqrt_price)
    return delta_x


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(swap(1, 10000000, 100000))
