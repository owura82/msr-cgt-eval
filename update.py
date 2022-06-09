import sys
import webbrowser
import os
import shutil

# used for selecting samples for evaluation

def folder_name_from_link(link):
    common = link.index('.com/')
    return link[common+5:-1].replace('/', '-')

def setup(link):
    # create folder for next commit
    new_folder = 'evals/'+folder_name_from_link(link)
    if not os.path.exists(new_folder):
        os.mkdir(new_folder)

    # create files
    buggy = open(new_folder+'/buggy', 'w').close()
    fixed = open(new_folder+'/fixed', 'w').close()
    prompt = open(new_folder+'/prompt', 'w').close()
    response = open(new_folder+'/response', 'w').close()

    os.system('atom '+new_folder+'/fixed '+new_folder+'/prompt '+new_folder+'/buggy')
    webbrowser.open(link[:-1])


if len(sys.argv) == 2 and sys.argv[1] == 'start':
    print('starting new session ...')
    line = ''
    with open('github_links_WORKING.csv', 'r') as myfile:
        line = myfile.readline()
    setup(line)

else:
    first_line = ''
    next_line = ''
    with open('github_links_WORKING.csv', 'r') as myfile:
        lines = myfile.readlines()
        first_line = lines[0]
        next_line = lines[1]

    with open('github_links_WORKING.csv', 'w') as myfile:
        # for i in range(1, len(lines)):
        #     myfile.write(lines[i])
        myfile.writelines(lines[1:])


    if len(sys.argv) < 2:
        print("\nREJECTING LINK\n")
        with open('github_links_REJECTED.csv', 'a') as myfile:
            myfile.write(first_line)

        # delete folder and files created by setup()
        shutil.rmtree('evals/'+folder_name_from_link(first_line))

    else:
        print("\SAVING LINK\n")
        with open('github_links_SELECTED.csv', 'a') as myfile:
            myfile.write(first_line)

    setup(next_line)
