t = int(input())

for _ in range(t):
    n = int(input())
    m = n
    ans = 7
    previous_digit = -1
    down = ((n % 10) + 3) % 10
    ans = min(ans, down)
    digit = 0
    while (m > 0):
        up = (10 - ((m % 10) + 3) % 10) % 10
        down = 10
        drop = n % (10 ** digit)
        if (m % 10 == 8):
            down = drop + 1
        if (drop - up < 0): up += 1
        if (previous_digit == -1): up = 10
        ans = min(ans, min(up, down))
        previous_digit = m % 10
        m //= 10
        digit += 1
    
    print(ans)