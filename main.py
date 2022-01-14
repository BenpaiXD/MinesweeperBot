
if __name__ == '__main__':
    t1 = (1, 2)
    t2 = (3, 4)
    t3 = (5, 6)

    set1 = set()
    set1.add(t1)
    set1.add(t2)
    set1 = frozenset(set1)

    set2 = set()
    set2.add(t2)
    set2.add(t1)
    set2 = frozenset(set2)

    set3 = set()
    set3.add(t1)
    set3.add(t3)
    set3 = frozenset(set3)

    superset = set()
    superset.add(set1)
    superset.add(set2)
    superset.add(set3)

    print(superset)

    print(any((1, 2) in subset for subset in superset))


    # main()

