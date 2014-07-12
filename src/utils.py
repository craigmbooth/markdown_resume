import os
from fa_list import fa_strings

def swap_extension(filename, new_extension):
    """Pass in a filename, return the filename with the extension replaced"""
    new_name = list(os.path.splitext(filename))
    new_name[-1] = "."+new_extension
    return "".join(new_name)


def replace_fa_strings(filename):
    with open(filename, "r") as fin:
        with open("test.html", "w") as fout:
            for line in fin.readlines():
                for fa_string in fa_strings:
                    if ":"+fa_string+":" in line:
                        line = line.replace(":"+fa_string+":",
                                     '<span class="fa '+fa_string+'"></span>')
                fout.write(line)
    os.rename("test.html", filename)
