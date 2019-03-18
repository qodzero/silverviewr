def aspect_ratio(val, lim):

    lower = [0, 1]
    upper = [1, 0]

    while True:
        mediant = [lower[0] + upper[0], lower[1] + upper[1]]

        if val * mediant[1] > mediant[0]:
            if lim < mediant[1]:
                return upper
            
            lower = mediant
        elif val * mediant[1] == mediant[0]:
            if lim >= mediant[1]:
                return mediant
            
            if lower[1] < upper[1]:
                return lower
            
            return upper;
        else:
            if (lim < mediant[1]):
                return lower
            upper = mediant

x = aspect_ratio((1920/1080),50)
print(x)
