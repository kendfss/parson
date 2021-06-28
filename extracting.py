import os

from tqdm import tqdm

from m3ta import Directory, File, show, main, save, load, beeper, pop
from structures import Node, Agent

PARSON_PICKLE = File(os.path.join(os.getcwd(), 'memories', 'parson.pkl'))
unicodeErrors = os.path.join('erroneous corpora', 'unicode decode error')
unicodeErrors = Directory(unicodeErrors).create()
# print(unicodeErrors)
# print(type(unicodeErrors))
# print(d.path)
# show(d.gather(ext='txt'))
def study(path, ext='txt'):
    d = Directory(path)
    parson = Agent() if not PARSON_PICKLE.exists else load(PARSON_PICKLE.path)
    for i, article in enumerate(d.gather(ext='txt'), 1):
        f = File(article)
        try:
            text = f.open(scrape=True)
            # print(f"\t{parson.characteristic(text)}")
            parson.train(text)
            # help(f)
            # print(text)
            print(f"{i}\t{f.up.up.name}")
        except UnicodeDecodeError as e:
            newdir = Directory((unicodeErrors / f.up.up.up.name).path)
            newdir = newdir / f.up.up.name
            f.move(newdir.path)
    
    
    # save(parson, PARSON_PICKLE.path)
    beeper(7)
    return parson


if eval(main):
    path = r'E:\Projects\Monties\2020\tools\scrapes\parson_corpora\devlin\articles'
    parson = study(path)