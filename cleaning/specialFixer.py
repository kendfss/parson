import os
from m3ta import nameSpacer

folder = os.path.split(__file__)[0]

hasnums = lambda x: True if any(i.isnumeric() for i in x) else False
for file in os.listdir(folder):
    path = os.path.join(folder,file)
    ext = os.path.splitext(file)[1]
    
    if hasnums(ext) or '_' in ext or ext=='.also':
        os.rename(path,nameSpacer(path+'.txt'))
        
    elif file.lower().startswith('notes'):
        os.rename(path,nameSpacer(os.path.join(r'E:\Projects\Monties\2019\resources\documents',file)))