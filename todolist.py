to_do_lst = ['Do yoga',
             'Make a breakfast',
             'Learn the basics of SQL',
             'Learn about ORM']
print('Today:')
for number, task in enumerate(to_do_lst):
    print(f'{number + 1}) {task}')
