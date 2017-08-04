import glob
import os
import json
import sys

def parse_file(file_path, file_info_dict, routing_dict):
    with open(file_path) as f:
        file_dict = {}
        routes_ls = []
        package = '-package_not_found-'
        name = '-name_not_found-'
        # file_dict['length'] = len(f) # this has no len()
        for line in f:
            if 'import' in line:
                dependency = line.split(' ')[1].replace(';', '').strip()
                if('jda' in line or 'redprairie' in line):
                    ls = file_dict.get('local_imports',[])
                    ls.append(dependency)
                    file_dict['local_imports'] = ls
                else:
                    ls = file_dict.get('library_imports',[])
                    ls.append(dependency)
                    file_dict['library_imports'] = ls

            if 'package' in line:
                package = line.split(' ')[1].replace(';', '').strip()

            if 'public' in line and 'class' in line:
                ls = line.split(' ')
                n = ls.index('class')
                name = ls[n+1]
                # get exteds and implements

            if (('public' in line) and ('interface' in line)):
                ls = line.split(' ')
                n = ls.index('interface')
                name = ls[n+1]
                # get exteds

            if '@RequestMapping' in line:
                line = line.replace('@RequestMapping(', '')
                n = len(line)
                line = line[0:-1] # trim trailing ')' TODO: handle multi line annotations
                if len(line) + 1 != n:
                    print('ALERT')
                    print('ALERT')
                ls = line.split(',')
                # print(str(ls))
                d = {}
                for param in ls:
                    if 'method' in param:
                        d['method'] = param.split('=')[1].strip()
                    elif 'value' in param:
                        d['path'] = param.split('=')[1].replace('"','').strip() #TODO: handle string var/const as value
                routes_ls.append(d)

            for path_dict in routes_ls:
                path_dict['file_path'] = file_path
                path_dict['java_file'] = package + '.' + name

    file_id = package + '.' + name
    file_dict['id'] = file_id
    file_dict['path'] = file_path
    file_info_dict[file_id] = file_dict
    routing_dict[file_id] = routes_ls


def get_files_ls(base_path, file_extension, recur=True):
    if base_path[-1] != os.sep:
        base_path += os.sep
    if file_extension[0] != '.':
        file_extension = '.' + file_extension
    ls = glob.glob(base_path + '**/*' + file_extension, recursive=recur)
    return ls

def run_parser(base_path, files_out, routes_out, file_extension, recusion=True):
    files_ls = get_files_ls(base_path, file_extension, recusion)
    file_dict = {}
    routes_dict = {}

    for f in files_ls:
        # f = str(f)
        # f = repr(f)
        # f = f.replace('\\\\', os.sep)
        # f = f.replace('/', os.sep)
        if os.path.isdir(f):
            continue
        if 'TU_' in f:
            continue
        try:
            parse_file(f, file_dict, routes_dict)
        except Exception as e:
            print('ERROR: ' + repr(f) + '\n\t' + str(e))
    with open(files_out, 'w') as f_out:
        json.dump(file_dict, f_out)

    with open(routes_out, 'w') as f_out:
        json.dump(routes_dict, f_out)

if len(sys.argv) < 4:
    print('enter System arguments: <base path> <files info output path> <routes map output path>')
    exit(1)
base_path = sys.argv[1]
files_out_path = sys.argv[2]
routes_out_path = sys.argv[3]
file_extension = 'java' # sys.argv[4]
 
print(sys.argv)
print('running')
run_parser(base_path, files_out_path, routes_out_path, file_extension) # recursion
print('finsihed running')