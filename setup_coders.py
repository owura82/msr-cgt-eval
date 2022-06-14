import sys
import webbrowser
import os

def folder_name_from_link(link):
    # returns everything after '.com' in the input link and replaces / with - so it can be used as a folder name
    common = link.index('.com/')
    return link[common+5:-1].replace('/', '-')

def setup(link):
    folder = 'evals/'+folder_name_from_link(link)

    print('\nsetting up new link...\n'+folder+'\n')

    # create coders directory
    coder_folder = folder + '/coders'
    if not os.path.exists(coder_folder):
        os.mkdir(coder_folder)
        # create results file
        open(coder_folder+'/coder_results.txt', 'w').close()
    
    #open response file, coder folder and webpage with github link
    os.system('code '+folder+'/response')
    os.system('open '+coder_folder)
    webbrowser.open(link[:-1])


if len(sys.argv) == 2 and sys.argv[1] == 'start':
    print('\nstarting new session ...\n')
    with open('to_check.csv', 'r') as myfile:
        link = myfile.readline()
    
    setup(link)

else:
    with open('to_check.csv', 'r') as myfile:
        lines = myfile.readlines()
        first_line = lines[0]

    print("\nAdding sample to checked\n")
    with open('checked.csv', 'a') as myfile:
        myfile.write(first_line)
    
    if(len(lines) < 2):
        open('to_check.csv', 'w').close()
        print('nothing more to check')
        sys.exit()

    next_link = lines[1]

    with open('to_check.csv', 'w') as myfile:
        myfile.writelines(lines[1:])
    
    setup(next_link)
