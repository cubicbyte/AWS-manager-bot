def get_whitelist():
    file = open('whitelist.txt')
    whitelist = file.read().splitlines()
    file.close()

    return whitelist