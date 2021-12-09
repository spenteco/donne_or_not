#!/home/spenteco/anaconda2/envs/py3/bin/python

import subprocess

all_tcp_ids = []
all_catalog_data = []
author_totals = {}

DROP_THESE_TCP_IDS = ['A20628', 'A20648', 'A20624', 'A36301', 'A86259', 
                        'A74632', 'A43381', 'A43384', 'A69817', 'A80776', 
                        'A34930', 'A64745', 'A52134', 'A38630', 'A52138', 
                        'A52146', 'A52139', 'B05024', 'B09895', 'B05023', 
                        'A57489', 'A62195', 'A57504', 'A57503', 'A57501', 
                        'A57500', 'A57493', 'A34566', 'A57486', 'A26471', 
                        'A91914', 'A91911', 'A48048', 
                        'A20656', 'B12480', 'A20637', 'A20644', 'A33850']

def process_name(name):
    
    global all_tcp_ids
    global all_catalog_data
    
    cmd = 'egrep "[0-9]\\s' + name + '" ~/0/EEBO_metadata.tsv'
    
    data = subprocess.getoutput(cmd)
    
    tcp_ids = []
    
    for line in data.split('\n'):
        if line.strip() > '':
            
            c = line.split('\t')
            
            p_to_lines = '/home/spenteco/0/all_lines_reg/' + c[0] + '.txt'
            
            try:
            
                n_lines = 0
                
                for l in open(p_to_lines, 'r', encoding='utf-8').read().split('\n'):
                    if l.strip() > '':
                        n_lines += 1
                        
                if c[0] not in DROP_THESE_TCP_IDS:
                
                    all_catalog_data.append({'tcp_id': c[0], 
                                             'year': c[1], 
                                             'author': c[2], 
                                             'title': c[3],
                                             'n_lines': n_lines})
                    
                    tcp_ids.append(c[0])
                    
                    if name not in author_totals:
                        author_totals[name] = 0
                    author_totals[name] += n_lines
                
            except FileNotFoundError:
                #print('FileNotFoundError', p_to_lines)
                pass
            
    all_tcp_ids += tcp_ids
            
    print(name, len(tcp_ids))
    
# -------------------------------------------------

#process_name('Chaucer, Geoffrey')
#process_name('Skelton, John')
#process_name('Wyatt, Thomas')
#process_name('Surrey')
#process_name('Sidney, Philip')
#process_name('Spenser, Edmund')
#process_name('Raleigh, Walter, Sir')
#process_name('Marlowe')
#process_name('Shakespeare, William')
process_name('Donne, John')
#process_name('Jonson, Ben')
#process_name('Webster, John, 1580?')
process_name('Herrick, Robert')
process_name('Herbert, George, 1593')
process_name('Crashaw, Richard')
process_name('Vaughan, Henry')
process_name('Marvell, Andrew')
#process_name('Milton, John')
#process_name('Dryden, John')
process_name('Rochester, John')
    
# -------------------------------------------------

print(len(all_tcp_ids))
    
# -------------------------------------------------

import json
import pandas as pd

f = open('data/all_tcp_ids.js', 'w', encoding='utf-8')
f.write(json.dumps(all_tcp_ids, indent=4, ensure_ascii=False))
f.close()

df = pd.DataFrame(all_catalog_data)
df.to_csv('data/all_catalog_data.csv', index=False)
    
# -------------------------------------------------

temp = []

for k, v in author_totals.items():
    temp.append({'author': k, 'n_lines': v})

df = pd.DataFrame(temp)
df.to_csv('data/author_line_counts.csv', index=False)

print('ok')
    
    
