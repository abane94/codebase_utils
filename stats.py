import re

def parse_git_log(in_path):
    files_info_dict = {}

    with open(in_path) as f:
        commit_id= ''
        date = ''
        commit_msg = ''
        for line in f:
            m = None
            if 'commit' in line:
                m = re.match( r'^commit ([0-9a-f]{40})$', line, re.M|re.I)
                if m:
                    commit_id = m.group(1)
            if ('Date:' in line):
                date = line.replace('Date:', '').strip()
                next(f)
                line = next(f)
                commit_msg = line.strip()

            if ('.java' in line and '|' in line):
                file_name = line.split('|')[0].strip()
                if file_name in files_info_dict:
                    files_info_dict[file_name]['num'] = files_info_dict[file_name]['num'] +1
                else:
                    new_file = {'most recent commit id': commit_id,
                        'most_recent_commit_msg': commit_msg,
                        'most_recent_commit_date' : date,
                        'num': 1}
                    files_info_dict[file_name] = new_file

    return files_info_dict

def print_dict_to_csv(d, key_comlumn_name, out_path):
    with open(out_path, 'w') as f:
        ls = d[list(d.keys())[1]].keys()
        header = key_comlumn_name + ',' + ','.join(ls)
        f.write(header + '\n')
        for file_name, file_info in d.items():
            row = file_name
            for field in file_info.values():
                row = row + ',' + str(field)
            f.write(row + '\n')

print('running')
d = parse_git_log('C:\\Users\\abane_000\\Desktop\\Files\\Projects\\By Theme\\Tech\\projects stats\\git_log_v1\\git_log_v1.txt')
print(str(len(d)))
print_dict_to_csv(d, 'file name', 'C:\\Users\\abane_000\\Desktop\\Files\\Projects\\By Theme\\Tech\\projects stats\\git_log_v1.csv')
print('finsihed running')