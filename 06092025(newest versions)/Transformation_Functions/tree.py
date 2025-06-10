from collections import Counter
import numpy as np
import csv

class Tree():
    def __init__(self, name, up=None, down=[], contents=[]):
        self.name = name
        self.up = up
        self.down = down
        self.contents = contents
        self.folder = None
        self.file = None
        self.down_set = []
        self.value =[]

    def read(self):
        if self.down != []:
            return None
        with open(self.file, 'r') as f:
            data = f.readlines()
        dic = Counter(data)
        if dic['\n'] != 1:
            subset_name = []
            subset_num = []
            subset_name_name = []
            subset_name_value = []
            for i in range(1, len(data)):  # i代表行数
                if data[i] == '\n':
                    subset_name += [data[i+1].replace('\n', '')]
                    subset_num += [i+1]
            subset_num += [len(data)+1]
            for j in range(0, len(subset_name)):  # j代表subset数
                name = []
                name_value = []
                for i in range(subset_num[j]+1, subset_num[j+1]-1):
                    value = []
                    sm = data[i].replace('\n', '')
                    sm = sm.split(' ')
                    name += [sm[0]]
                    for i in range(1, len(sm)):
                        v = sm[i].split('-')
                        if len(v) == 1:
                            value += [int(v[0])]
                        else:
                            for i in range(int(v[0]), int(v[1])+1):
                                value += [i]
                    name_value += [value]
                subset_name_value += [name_value]
                subset_name_name += [name]
            for i in range(len(subset_name)):
                globals()[subset_name[i]] = Tree(subset_name[i], self)
                for j in range(len(subset_name_name[i])):
                    globals()[subset_name_name[i][j]] = Tree(subset_name_name[i][j], up=globals()[
                        subset_name[i]], contents=subset_name_value[i][j])
                    globals()[subset_name[i]].down = globals()[
                        subset_name[i]].down + [globals()[subset_name_name[i][j]]]
                self.down = self.down + [globals()[subset_name[i]]]
        else:
            name = []
            name_value = []
            for i in range(2, len(data)):
                value = []
                sm = data[i].replace('\n', '')
                sm = sm.split(' ')
                name += [sm[0]]
                for i in range(1, len(sm)):
                    v = sm[i].split('-')
                    if len(v) == 1:
                        value += [int(v[0])]
                    else:
                        for i in range(int(v[0]), int(v[1])+1):
                            value += [i]
                name_value += [value]
            for i in range(len(name)):
                globals()[name[i]] = Tree(
                    name[i], self, contents=name_value[i])
                self.down = self.down + [globals()[name[i]]]

    def upload(self):
        m = self
        while m.up != None:
            m = m.up
            m.down_set += [self]

    def download(self):
        for i in self.down_set:
            self.contents = self.contents + i.contents

    def get_value(self,value):
        self.value = self.value + [value]


brain = Tree('brain')

CEREBRUM = Tree('CEREBRUM', brain)
BRAIN_STEM = Tree('BRAIN_STEM', brain)
CEREBELLUM = Tree('CEREBELLUM', brain)
fiber_tracts_and_ventricular = Tree('fiber_tracts_and_ventricular', brain)

CTX = Tree('CTX', CEREBRUM)
CNU = Tree('CNU', CEREBRUM)

INTERBRAIN = Tree('INTERBRAIN', BRAIN_STEM)
MIDBRAIN = Tree('MIDBRAIN', BRAIN_STEM)
HINDBRAIN = Tree('HINDBRAIN', BRAIN_STEM)

CBN = Tree('CBN', CEREBELLUM)
CBX = Tree('CBX', CEREBELLUM)

CTXpl = Tree('CTXpl', CTX)
CTXsp = Tree('CTXsp', CTX)

PAL = Tree('PAL', CNU)
STR = Tree('STR', CNU)

HY = Tree('HY', INTERBRAIN)
TH = Tree('TH', INTERBRAIN)

MBmot = Tree('MBmot', MIDBRAIN)
MBsen = Tree('MBsen', MIDBRAIN)
MBsta = Tree('MBsta', MIDBRAIN)

MEDULLA = Tree('MEDULLA', HINDBRAIN)
PONS = Tree('PONS', HINDBRAIN)

fiber_tracts = Tree('fiber_tracts',fiber_tracts_and_ventricular)
ventricles = Tree('ventricles', fiber_tracts_and_ventricular)

set = [brain, CEREBRUM, BRAIN_STEM, CEREBELLUM, CTX, CNU, INTERBRAIN, MIDBRAIN,HINDBRAIN, CBN, CBX, CTXpl, CTXsp, PAL, STR, HY, TH, MBmot, MBsen, MBsta, MEDULLA, PONS, fiber_tracts_and_ventricular, fiber_tracts, ventricles]


def updown(set):
    for c in set:
        if c.up != None:
            a = c.up
            a.down = a.down + [c]

# annotation

def fold(set):
    for c in set:
        if c.up == None:
            c.folder = '/Users/stepviewmaifu/RESEARCH/Fu lab/3D test data/tree/annotation'
        elif c.up != None and c.down != []:
            c.folder = c.up.folder + '/' + c.name + '/'
        else:
            c.file = c.up.folder + c.name + '.txt'
        c.read()

def upload():
    for c in globals().values():
        try:
            if c.contents != None:
                c.upload()
        except AttributeError:
            pass
        except TypeError:
            pass

def download():
    for c in globals().values():
        try:
            if c.contents != None:
                c.download()
        except AttributeError:
            pass
        except TypeError:
            pass

def addsome():
    PONS.contents += [590]
    HINDBRAIN.contents += [590]
    BRAIN_STEM.contents += [590, 358, 932, 448]
    brain.contents += [590, 358, 932, 602, 906,448]
    HY.contents += [358]
    TH.contents += [932]
    INTERBRAIN.contents += [358, 932]
    PAL.contents += [602]
    STR.contents += [906]
    CNU.contents += [602, 906]
    CEREBRUM.contents += [602, 906]
    MIDBRAIN.contents += [448]
    fiber_tracts_and_ventricular.contents += [1181]


# 树的初始化
updown(set)
fold(set)
upload()
download()   
addsome()

level1 = [CEREBRUM, CEREBELLUM, INTERBRAIN, MIDBRAIN, HINDBRAIN
#, fiber_tracts_and_ventricular
]

level2 = []
for i in level1:
    if i != MIDBRAIN and i != CEREBRUM and i != CEREBELLUM:
        level2 += i.down
    else:
        level2 += [i]

level3 = []
for i in level2:
    if i.up == INTERBRAIN or i.up == fiber_tracts or i.up ==ventricles:
        level3 += [i]
    else:
        level3 += i.down

def find_next_level(level):
    level_next = []
    for i in level:
        if i.down == []:
            level_next += [i]
        else:
            level_next += i.down
    return level_next

level4 = level3
while level4 != find_next_level(level4):
    level4 = find_next_level(level4)


#for i in final_level:
#    print(i.name)


# 判断函数
def search_level(number,level=level2):
    dic = {}
    for i in level:
        for j in i.contents:
            dic[j] = i
    return dic[number]          #返回一个类

#for level in [level1, level2, level3, level4]:
#    print(search_level(641,level).name)



# 计数器函数
def t(data,level):
    s = []
    for i in range(len(data)):    #为什么要len
        ###data[i][0]###value
        ###data[i][4]###number(对应不同区域的number)
        try:
            search_level(data[i][4],level).get_value(data[i][0])
        except KeyError:
                s = s + [data[i]]
            
    return s



input_file_path = "/Users/stepviewmaifu/RESEARCH/Fu lab/3D test data/output folder/FAM/test/DMPAG_coordinate0526.npy"
coordinate = np.load(input_file_path)
mask = coordinate[..., 0] > 0
indices = np.array(np.nonzero(mask)).T  # (N, 3), 包含 x, y, z
data = []
for x, y, z in indices:
    value = coordinate[x, y, z, 0]
    region_id = coordinate[x, y, z, 1]
    data.append([value, x, y, z, region_id])

level = [1, 2, 3, 4]
for lvl in level:
    if lvl == 1:
        ll = level1
        unmatched = t(data,level1)
    elif lvl == 2:
        ll = level2
        unmatched = t(data,level2)
    elif lvl == 3:
        ll = level3
        unmatched = t(data,level3)
    else:
        ll = level4
        unmatched = t(data, level4)
    
    output_dir = "/Users/stepviewmaifu/RESEARCH/Fu lab/3D test data/output folder/FAM/"
    # 保存计数数据
    summary_path = f"{output_dir}/DMPAG_FAM_summary_level_{lvl}.csv"
    with open(summary_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Region', 'Mean', 'Count'])
        for region in ll:
            if region.value:
                writer.writerow([region.name, np.mean(region.value), len(region.value)])
    print(f"Level {lvl} summary saved to {summary_path}")

    # 保存 unmatched 数据
    unmatched_path = f"{output_dir}/DMPAG_FAM_unmatched_level_{lvl}.csv"
    unmatched = np.array(unmatched)
    if len(unmatched) > 0:
        with open(unmatched_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Value', 'X', 'Y', 'Z', 'Region_ID'])
            writer.writerows(unmatched)
        print(f"Level {lvl} unmatched entries saved to {unmatched_path}")