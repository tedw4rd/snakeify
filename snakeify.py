import os
import re
import sys
import argparse


word_with_cap_re = re.compile('(\s|\.|\(|\))([a-z]+(?:[A-Z]+[a-z]*)*)')
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def convert(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert camel-case code to snake-case.')
    parser.add_argument("file")
    parser.add_argument("-r", "--recursive",
                        action='store_const',
                        const=True, default=False)

    parser.add_argument("-a", "--allFiles",
                        action='store_const',
                        const=True, default=False)

    args = parser.parse_args()
    files_to_convert = []
    if args.recursive is False:
        files_to_convert.append(args.file)
    else:
        for (path, dirs, files) in os.walk(args.file):
            files = filter(lambda f: f.split('.')[0] != "", files)
            if args.allFiles is False:
                files = filter(lambda f: f.split('.')[1] == "py", files)
            all_files = map(lambda f: os.path.join(path, f), files)
            files_to_convert.extend(all_files)

    for f in files_to_convert:
        print "Converting " + f + " to camel-case"
        handle = open(f, "r")
        contents = handle.read()
        targets = word_with_cap_re.findall(contents)
        if targets is None:
            print "Nothing found.  Skipping..."
            continue
        for (c, target) in targets:
            print target
            contents = contents.replace(target, convert(target))
        handle.close()
        handle = open(f, "w")
        handle.write(contents)
        handle.close()
