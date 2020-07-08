
class Player:
    def __init__(self):
        self.stats_bubbles = 123
        self.stats_explosions = 456
        self.playername = ''
        self.score = 10000
        self.stats_maxmultiplier = 25

def highscore_test():
    import bubblebuster.highscores as hs
    h = hs.HighScores()
    h.load_all()
    p = Player()
    h.write(p)
    print('wrote player %s to bank file' % p.playername)
    with open('data/bank.bub') as f:
        for line in f.readlines():
            print(''.join(line))


def test():
    from linkman import LinkMan
    from link import Link
    LinkMan.create()

    a = Link('a')
    b = Link('b')
    c = Link('c')
    d = Link('d')

    LinkMan.add(d)
    LinkMan.add(c)
    LinkMan.add(b)
    LinkMan.add(a)

    LinkMan.print()

    LinkMan.remove(d)
    print()
    LinkMan.print()

    LinkMan.remove(b)
    print()
    LinkMan.print()

    LinkMan.remove(a)
    print()
    LinkMan.print()

    LinkMan.remove(c)
    print()
    LinkMan.print()

if __name__ == '__main__':
    #test()
    highscore_test()
