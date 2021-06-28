import os
from m3ta import nameSpacer

src = r"E:\Resources\dataSets\Language\spell checker\scowl-2018.04.16\r"
src = r'E:\Resources\dataSets\Language\spell checker\scowl-2018.04.16\l'
src = r'E:\Resources\dataSets\Language\spell checker\scowl-2018.04.16\misc'
src = r'E:\Resources\dataSets\Language\spell checker\scowl-2018.04.16\final'
dst = r"E:\Projects\Monties\2019\resources\documents"
dst = r"E:\Projects\Monties\2019\resources\words"

def gather(source):
    for root, folders, files in os.walk(source):
        for file in files:
            if os.path.exists((f := os.path.join(root,file))):
                yield f

def execute(source):
    print(source)
    for path in gather(source):
        name = os.path.split(path)[-1]
        folder = os.path.split(os.path.split(path)[0])[1]
        print(folder,name,sep='\n',end='\n\n')
        if os.path.splitext(path)[1]=='' or os.path.splitext(path)[1][1:].isnumeric():
            os.rename(path,(p:= path+'.txt'))
        # os.rename(path,p:=nameSpacer(os.path.join(dst,name)))
        # if 'readme' in path.lower():
            # os.rename(path,p:=nameSpacer(os.path.join(dst,name)))
        # if os.path.splitext(path)[1]=='.doc':
        #     try:
        #         os.renames(path,(p:=nameSpacer(os.path.join(dst,'windowsfiles',name))))
        #     except FileNotFoundError:
        #         pass
        # print(p)
if __name__ == '__main__':
    execute(src)
