# Generates a big dictionary of all left squashes up to max_exp.
# This table is used to speed up Nick2048 implementation.
# For example, the row [2, 2, 4, 4] squashes to [4, 8, 0, 0] with reward of 12.
# This appears as the following entry:
#
#     squash_lookup = {
#         ...
#         (2, 2, 4, 4): ((4, 8, 0, 0), 12),
#         ...
#    }
#
# Run `python etc/generate_squash_lookup.py` to regenerate the table at
# `improved-funicular/etc/squash_lookup_table.py`

max_exp = 15

v = [2 ** i for i in range(max_exp)]
v[0] = 0


def smush_left(row):
    new_row = [v for v in row if v != 0]
    reward = 0
    i = 0
    while i < len(new_row) - 1:
        if new_row[i] == new_row[i + 1]:
            val = new_row[i] * 2
            reward += val
            new_row[i] = val
            new_row.pop(i + 1)
        i += 1
    while len(new_row) < len(row):
        new_row.append(0)
    return tuple(new_row), reward


with open("etc/squash_lookup_table.py", "w") as fout:
    fout.write("squash_lookup = {\n")
    for i in v:
        for j in v:
            for k in v:
                for m in v:
                    row = (i, j, k, m)
                    new_row, reward = smush_left(row)
                    fout.write(f"    {row}: ({new_row}, {reward}),\n")
    fout.write("}\n")
