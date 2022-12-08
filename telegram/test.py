def round_down(num, divisor=5):
    return num - (num%divisor)

def round_up(num, divisor=5):
    return num if num % divisor == 0 else num + divisor - (num % divisor)

print(round_up(-100))

max([1,2,3,4,None])