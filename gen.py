import os
import sys
import webbrowser

#used to generate Copilot responses

def folder_name_from_link(link):
    common = link.index('.com/')
    return link[common+5:-1].replace('/', '-')

if len(sys.argv) == 2 and sys.argv[1] == 'start':
    print('\nstarting new session ...\n')
    line = ''
    with open('to_check.csv', 'r') as myfile:
        line = myfile.readline()
    folder = 'evals/'+folder_name_from_link(line)
    if line == '':
        print('nothing to check')
        sys.exit()
    if os.path.exists(folder):
        print('\n'+folder+'\n')
        #copy prompt file to response file if response is empty
        if open(folder+'/response', 'r').read() == '':
            os.system('cp '+folder+'/prompt '+folder+'/response')

        # os.system('atom '+folder+'/buggy '+folder+'/fixed')
        os.system('code '+folder+'/response')

        webbrowser.open(line[:-1])
    else:
        print('PROBLEM: '+folder+' does not exist')
else:
    lines = []
    first_line = ''
    next_line = ''
    with open('to_check.csv', 'r') as myfile:
        lines = myfile.readlines()
        first_line = lines[0]
    
    if(len(lines) < 2):
        print('nothing to check')
        # with open('to_check.csv', 'w') as myfile:
        #     myfile.writelines([''])
        open('to_check.csv', 'w').close()

        print("\nAdding sample to checked\n")
        with open('checked.csv', 'a') as myfile:
            myfile.write(first_line)
        sys.exit()

    next_line = lines[1]

    with open('to_check.csv', 'w') as myfile:
        myfile.writelines(lines[1:])

    print("\nAdding sample to checked\n")
    with open('checked.csv', 'a') as myfile:
        myfile.write(first_line)

    folder = 'evals/'+folder_name_from_link(next_line)
    if os.path.exists(folder):
        print('\n'+folder+'\n')
        #copy prompt file to response file if response is empty
        if open(folder+'/response', 'r').read() == '':
            os.system('cp '+folder+'/prompt '+folder+'/response')
       
        # os.system('atom '+folder+'/buggy '+folder+'/fixed')
        os.system('code '+folder+'/response')
        webbrowser.open(next_line[:-1])
    else:
        print('PROBLEM: '+folder+' does not exist')
