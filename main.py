from beehive import Bee


def main(args):
    
    b = Bee('Champ de pissenlits et de sauge des pres.xlsx')
    gen = b.generation(50)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
