import ui
import zarf

global rows
rows = 1

def _get(v, s, attr):
    for i in range(1, rows+1):
        yield getattr(v[f'{s}{i}'], attr)
        
def get_modes(view):
    yield from _get(view, 'sc', 'selected_index')

def get_input(view):
    yield from _get(view, 'tf', 'text')

@ui.in_background
def search(sender):
    modes = ['pab'[int(i)] for i in get_modes(v)]
    texts = [i.upper() for i in get_input(v)]
    res = zarf.multisearch(modes, texts, ret=True)
    v['tv'].text = res

def delete(sender):
    global rows
    
    r = int(sender.name[-1]) + 1
    for i in ['sc', 'tf']:
        v.remove_subview(v[f'{i}{r}'])
    for i in ['add', 'sub']:
        v.remove_subview(v[f'{i}{r-1}'])
    for i in range(r+1, rows+1):
        for j in ['sc', 'tf']:
            n = f'{j}{i}'
            v[n].y -= 42
            v[n].name = f'{j}{i-1}'
        for j in ['add', 'sub']:
            n = f'{j}{i-1}'
            v[n].y -= 42
            v[n].name = f'{j}{i-2}'
    v['tv'].y -= 42
    
    rows -= 1
    
def add(sender):
    global rows
    rows += 1
    y = 32*(rows-1)+10*rows
    
    sc = ui.SegmentedControl()
    sc.segments = 'PAB'
    sc.frame = (215, y, 69, 32)
    sc.flex = 'LR'
    sc.name = f'sc{rows}'
    sc.action = search
    v.add_subview(sc)
    
    tf = ui.TextField()
    tf.placeholder = 'search term'
    tf.frame = (6, y, 106, 32)
    tf.flex = 'TF'
    tf.name = f'tf{rows}'
    tf.action = search
    v.add_subview(tf)
    
    adb = ui.Button()
    adb.title = '+'
    adb.frame = (294, y, 37, 32)
    adb.flex = 'LB'
    adb.name = f'add{rows-1}'
    adb.action = add
    v.add_subview(adb)
    
    sub = ui.Button()
    sub.title = '-'
    sub.frame = (332, y, 37, 32)
    sub.flex = 'LB'
    sub.name = f'sub{rows-1}'
    sub.action = delete
    v.add_subview(sub)
    
    v['tv'].y += 42

    
v = ui.load_view()
v.present('sheet')
