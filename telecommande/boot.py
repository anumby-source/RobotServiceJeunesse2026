# This file is executed on every boot (including wake-boot from deepsleep)
import machine
import sys, os

# mise a jour de sys.path
def update_path(path):
    if path not in sys.path:
        sys.path.append(path)
    for e in os.ilistdir(path):
        if e[1] == 0x4000:
            update_path(path + '/' + e[0])

update_path('')
# affiche le contenu de 'file'
def dispfile(file):
    n = 1
    for line in open(file,'r'):
        print('{:>3}'.format(n),line.strip('\r\n'))
        n += 1
#
def dirlist(dir=''):
    if dir == '': dir = os.getcwd()
    try:
        for e in os.ilistdir(dir):
            if e[1] == 0x8000:
                print('{:45}{:6d}'.format(e[0], os.stat(e[0])[6]))
            else:
                print('{:45}{:>6}'.format(e[0],'Rep'))
    except OSError:
        print('Directory {} empty'.format(dir))
#
def dire(module):
    l = dir(module)
    ncol = 4
    nlig = (len(l)-1)//ncol + 1
    for k in range(nlig):
        fmt = '{:25}'*(len(l[k::nlig]))
        print(fmt.format(*l[k::nlig]))
#
def spaceLeft():
    l = os.statvfs('')
    print('filesystem size: {} kB'.format((l[0]*l[2])//1024))
    print('free space     : {} kB'.format((l[0]*l[3])//1024))