import os
import sys

def folder_name_from_link(link):
    common = link.index('.com/')
    return link[common+5:-1].replace('/', '-')


def setup(link):
    folder = 'evals/'+folder_name_from_link(link)
    os.system('code '+folder+'/response')
    os.system('code '+folder+'/buggy')
    os.system('code '+folder+'/fixed')

def remove():
    lines = []
    with open('to_check.csv', 'r') as myfile:
        lines = myfile.readlines()

    with open('to_check.csv', 'w') as myfile:
        myfile.writelines(lines[1:])

def save_result(cat, line):
    if cat == 'a':
        print('\nsaving to catetory A\n')
        with open('results/cat_A', 'a') as myfile:
            myfile.write(line)
    elif cat == 'b':
        print('\nsaving to catetory B\n')
        with open('results/cat_B', 'a') as myfile:
            myfile.write(line)
    else: #cat == 'c':
        print('\nsaving to catetory C\n')
        with open('results/cat_C', 'a') as myfile:
            myfile.write(line)

    with open('checked.csv', 'a') as myfile:
        myfile.write(line)


if len(sys.argv) == 2 and sys.argv[1] == 'start':
    print('starting new session ...')
    line = ''
    with open('to_check.csv', 'r') as myfile:
        line = myfile.readline()
    setup(line)


elif len(sys.argv) == 2:
    first = ''
    next_line = ''
    if sys.argv[1] == 'a' or sys.argv[1] == 'b' or sys.argv[1] == 'c':
        with open('to_check.csv', 'r') as myfile:
            first = myfile.readline()
            next_line = myfile.readline()
            remove()
            save_result(sys.argv[1], first)
            setup(next_line)
    else:
        print('did not get appropriate category')

else:
    print('Need two arguments: a, b, or c')

    