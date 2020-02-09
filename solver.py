while True:
    tents = 0
    slots = []
    trees = []
    confirmed = []

    # Initialize all about grid (including the number of tents required)
    print("Numbers on left")
    rows = [int(st) for st in input(">").split(" ")]
    print("Numbers on top")
    columns = [int(st) for st in input(">").split(" ")]
    print("Trees now")
    s = input(">")
    while s:
        trees += [[int(st) for st in s.split(" ")]]
        s = input(">")
    n = int(len(rows))
    rows_slots = [0 for _ in range(n)]
    columns_slots = [0 for _ in range(n)]
    for i in range(n):
        tents += rows[i]

    # Initialize all about slots and trees
    for tree in trees:
        for i in range(-1, 2, 2):
            if 0 <= tree[0] + i < n:
                if -1 < tree[0] + i < n and [tree[0] + i, tree[1]] not in [*trees, *slots]:
                    rows_slots[tree[1]] += 1
                    columns_slots[tree[0] + i] += 1
                    slots += [[tree[0] + i, tree[1]]]
            if 0 <= tree[1] + i < n:
                if -1 < tree[1] + i < n and [tree[0], tree[1] + i] not in [*trees, *slots]:
                    rows_slots[tree[1] + i] += 1
                    columns_slots[tree[0]] += 1
                    slots += [[tree[0], tree[1] + i]]

    # Don't you dare continue until it's solved bitch... please?
    while len(confirmed) != tents:
        change = False

        # Remove slots in 0 lines + Confirm slots in lines equal to number of slots
        for i in range(n):
            if rows[i] == 0 and rows_slots[i] != 0:
                change = True
                for slot in slots:
                    if slot[1] == i:
                        slots.remove(slot)
                        rows_slots[i] -= 1
                        columns_slots[slot[0]] -= 1
                        if rows_slots[i] == 0:
                            break
            if columns[i] == 0 and columns_slots[i] != 0:
                change = True
                for slot in slots:
                    if slot[0] == i:
                        slots.remove(slot)
                        columns_slots[i] -= 1
                        rows_slots[slot[1]] -= 1
                        if columns_slots[i] == 0:
                            break
            if rows[i] == rows_slots[i] != 0:
                change = True
                for slot in slots:
                    if slot[1] == i:
                        confirmed += [slot]
                        rows_slots[i] -= 1
                        columns_slots[slot[0]] -= 1
                        rows[i] -= 1
                        columns[slot[0]] -= 1
                        slots.remove(slot)
                        if rows_slots[i] == 0:
                            break
            if columns[i] == columns_slots[i] != 0:
                change = True
                for slot in slots:
                    if slot[0] == i:
                        confirmed += [slot]
                        columns_slots[i] -= 1
                        rows_slots[slot[1]] -= 1
                        columns[i] -= 1
                        rows[slot[1]] -= 1
                        slots.remove(slot)
                        if columns_slots[i] == 0:
                            break

        # Cleanup of slots and trees adjacent to confirmed locations
        for tnt in confirmed:
            for i in range(-1, 2, 2):
                for slot in slots:
                    if [tnt[0] + i, tnt[1]] == slot or [tnt[0], tnt[1] + i] == slot or \
                            [tnt[0] + i, tnt[1] + i] == slot or [tnt[0] + i, tnt[1] - i] == slot:
                        change = True
                        rows_slots[slot[1]] -= 1
                        columns_slots[slot[0]] -= 1
                        slots.remove(slot)
                for tree in trees:
                    if [tnt[0] + i, tnt[1]] == tree or [tnt[0], tnt[1] + i] == tree:
                        change = True
                        trees.remove(tree)

        # Cleanup of slots not adjacent to trees
        for slot in slots:
            for i in range(-1, 2, 2):
                for tree in trees:
                    if [slot[0] + i, slot[1]] == tree or [slot[0], slot[1] + i] == tree:
                        break
                else:
                    continue
                break
            else:
                change = True
                rows_slots[slot[1]] -= 1
                columns_slots[slot[0]] -= 1
                slots.remove(slot)

        # Check if all the remaining slots need to be filled to get the required number of tents
        if tents - len(confirmed) == len(slots):
            change = False
            for slot in slots:
                confirmed += [slot]
                slots.remove(slot)

        # a fail safe added to break out of infinite looping
        if not change:
            break

    # If we enter here, this means we'll have to go for trial and error
    if len(confirmed) != tents:
        # Sorry, but this isn't finished
        pass

    if len(confirmed) > 0:
        print("Confirmed locations:")
        print(confirmed)
    # Supposedly useless when it's complete but let's just leave it
    if len(confirmed) != tents:
        print("Unconfirmed locations:")
        print(slots)
