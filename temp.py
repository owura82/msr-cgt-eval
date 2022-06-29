import enum
from getopt import gnu_getopt
import os

#Code to create response files with prompts
# count = 0
# for folder in os.listdir('evals'):
#     # print(folder)
#     if os.path.isdir(os.path.join('evals', folder)):
#         prompt_file = os.path.join('evals', folder, 'prompt')
#         response_file = os.path.join('evals', folder, 'response')
            
#         content = []
#         with open(prompt_file, 'r') as f:
#             content = f.readlines()
#         with open(response_file, 'w') as f:
#             f.writelines(content)
#         count += 1

# print(count)

#code to create buggy file with file extensions for codeql analysis
    # deletes other files not required for codeql analysis
    #be careful about executing this seciton of code more than once, will need to reinitialize the code_ql_evals folder after each execution

# count = 0
# c_count = 0
# cpp_count = 0
# for folder in os.listdir('code_ql_evals'):
#     if os.path.isdir(os.path.join('code_ql_evals', folder)):
#         folder_path = os.path.join('code_ql_evals', folder)
#         buggy = os.path.join(folder_path, 'buggy')
#         print(buggy)

#         response = os.path.join(folder_path, 'response')
#         fixed = os.path.join(folder_path, 'fixed')
#         prompt = os.path.join(folder_path, 'prompt')

#         os.system('rm '+response)
#         os.system('rm '+fixed)
#         os.system('rm '+prompt)

#         with open(buggy, 'r') as f:
#             line = f.readline()
#             if 'cpp' in line.lower():
#                 cpp_count += 1
#                 os.system('mv '+buggy+' '+folder_path+'/file.cpp')

#             else: 
#                 c_count += 1
#                 os.system('mv '+buggy+' '+folder_path+'/file.c')
#             count += 1
# print(count, cpp_count, c_count)

# create latex table for dates of selected projects
# open('latex_table.txt', 'w').close()
# with open('first_hundred_with_date.csv', 'r') as f:
#     lines = f.readlines()
#     for i,line in enumerate(lines):
#         if i > 51:
#             line_arr = line.split(',')
#             to_write = str(i-51) + ' & '+ line_arr[0] + ' & '+ line_arr[1][:-1] + ' \\\\ \n\\hline\n'
#             with open('latex_table.txt', 'a') as g:
#                 g.write(to_write)
        


# create csv file of folder names of category c samples 
def folder_name_from_link(link):
    common = link.index('.com/')
    return link[common+5:-1].replace('/', '-')

with open('all_catC_samples.txt', 'r') as f:
    links = f.readlines()

with open('initialize_result_table.csv', 'w') as f:
    for i,link in enumerate(links):
        folder = folder_name_from_link(link)
        pos = str(i+1)
        to_write = pos+','+folder+',C'
        if i < 86:
            to_write += '\n'
        f.write(to_write)