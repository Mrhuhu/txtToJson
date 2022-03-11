import os
import json

# 数据集字典
dataset = {
    'images':[],
    'annotations':[],
    'categories':[]
}

# 类别字典
category = {'0':'CV',   # 航母
            '1':'LHA',  # 两栖攻击舰
            '2':'LSD',  # 船坞登陆舰
            '3':'DD',   # 驱逐舰
            '4':'SS',   # 潜艇
            '5':'PC',   # 小型军舰
            '6':'PS',   # 非货船
            '7':'CS'}   # 货轮

# 读取txt文件路径及文件名
def readTxt(in_path):
    files = []
    file = {
        'fileName':'',
        'filePath':''
    }

    # 文件为 txt 类型
    filetype = '.txt'

    for parent,dirnames,filenames in os.walk(in_path):
        for filename in filenames:
            file['fileName'] = filename
            file['filePath'] = os.path.join(parent,filename)
            if file['filePath'].find(filetype) != -1:
                files.append(file)
    return files

# 读取txt文件中的内容
def readTxtContent(path,n):
    with open(path,'r',encoding='utf-8') as file_to_read:
        result = []
        lst = file_to_read.readline().split()

    # lst[0]:image_id   lst[1]:categories_id       lst[2]:cx              lst[3]:cy
    # lst[4]:w          lst[5]:h                   lst[6]:angle           lst[7]:image_width     lst[8]:image_height

    filename = lst[0] + '.bmp'
    height = float(lst[5]) * float(lst[8])
    weight = float(lst[4]) * float(lst[7])
    image_id = lst[0]

    dataset['images'].append({
        'filename':filename,
        'height':height,
        'weight':weight,
        'id':image_id
    })

    x1 = float(lst[2]) * float(lst[7]) - float(lst[4]) * float(lst[7]) / 2
    y1 = float(lst[3]) * float(lst[8]) - float(lst[5]) * float(lst[8]) / 2
    x2 = float(lst[2]) * float(lst[7]) + float(lst[4]) * float(lst[7]) / 2
    y2 = float(lst[3]) * float(lst[8]) + float(lst[5]) * float(lst[8]) / 2

    width = float(lst[4]) * float(lst[7])
    height = float(lst[5]) * float(lst[8])
    angle = float(lst[6])

    area = width * height

    # segmentation:描述框的4个点的坐标
    dataset['annotations'].append({
        'segmentation': [[
            x1,y1,
            x2,y1,
            x2,y2,
            x1,y2]],
        'area':area,
        'iscrowd':0,
        'image_id':lst[0],
        'bbox':[x1,y1,width,height,angle],
        'categories_id':lst[1],
        'id':n
    })

    cate_name = category[lst[1]]

    dataset['categories'].append({
        'id': lst[1],
        'name': cate_name
    })

    # 写出json的文件路径
    outpath = "C:\\Users\\MCCC\\Desktop\\OBBD\\hrsc2016\\labels\\txtJson\\" + str(n) + '.json'
    #outpath = "C:\\Users\\MCCC\\Desktop\\OBBD\\hrsc2016\\labels\\trainJson\\" + str(n) + '.json'
    with open(outpath,'w') as dump_f:
        json.dump(dataset,dump_f)

if __name__ == '__main__':

    # 读入txt的文件路径
    in_path = "C:\\Users\\MCCC\\Desktop\\OBBD\\HRSC2016TXT\\test"
    #in_path = "C:\\Users\\MCCC\\Desktop\\OBBD\\HRSC2016TXT\\train"
    fs = readTxt(in_path)
    for i in range(0,len(fs)):
        readTxtContent(fs[i]['filePath'],i)




