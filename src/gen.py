import os
import shutil


def gen_func(here, target):
    if target == './public':
        shutil.rmtree(target)
        os.mkdir(target)
    elements = os.listdir(path=here)
    for e in elements:
        if os.path.isfile(here+'/'+e):
            file = here+'/'+e
            shutil.copy(file, target)
        elif os.path.isdir(here+'/'+e):
            direc = here+'/'+e
            new_tar = target+'/'+e
            os.mkdir(new_tar)
            gen_func(direc, new_tar)
    return None

