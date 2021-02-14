from Repository import repo
import sqlite3
import os
import sys


def main(argv1, argv2, argv3):
    #os.remove("database.db")
    repo.create_tables()
    repo.parse_file(argv1)
    output = repo.operate_orders(argv2)
    index = len(output) - 1
    with open(argv3, "w") as output_file:
        for i in range(0, index):
            line = output[i] + "\n"
            output_file.write(line)
        line = output[index]
        output_file.write(line)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
