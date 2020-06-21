from linkman import LinkMan
from link import Link


def test():
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
    test()
