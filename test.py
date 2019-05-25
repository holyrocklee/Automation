import base64
import glob
import _thread

from offer.projects.Automation.requestutil import requestutil

# 选取文件夹内的文件并排序
#from com.eason.util.util import copyfile, slice_list, movefile

total = 0
right = 0
jieduan=''


def choose_file(path):
    files = [x for x in glob.glob(path)]
    return files


def iscarimage(image):
    data = {'car_image': base64.b64encode(open(image, 'rb').read())}
    util = requestutil('http://118.25.180.178:5080/isCarImage', data)
    return util.request('post')

'''
def categoryData(path, count):
    tlist = []
    results = [0, 1, 2]
    for result in results:
        images = choose_file(path + str(result) + '/*')
        for image in images:
            temp = {image: result}
            tlist.append(temp)
    return slice_list(tlist, count)


def categoryTestThreads(path, count):
    testdatalist = categoryData(path, count)
    _len = len(testdatalist)
    print(_len)
    for l, data in zip(range(_len), testdatalist):
        print(data)
        print(l)
        _thread.start_new_thread(categoryTest, (data, 'thread_' + str(l)))
'''

def categoryTest(testlist, thread_name):
    global total
    global right
    for image in testlist:
        print(thread_name + str(image))
        total = total + 1
        print(iscarimage(list(image.keys())[0]))
        if str(iscarimage(list(image.keys())[0])['result']) == str(list(image.values())[0]):
            right = right + 1


def categoryTestOne(path):
    results = [0, 1, 2]
    for result in results:
        images = choose_file(path + '/' + str(result) + '/*')
        onecategory(images, str(result))


def onecategory(files, expect):
    global total
    global right
    global jieduan
    local_count = 0
    local_right = 0
    for image in files:
        local_count = local_count + 1
        total = total + 1
        pandin = iscarimage(image)['result']
        if str(pandin) == expect:
            local_right = local_right + 1
            right = right + 1
            print(str(right) + '/' + str(total))
    jieduan=jieduan+'\n'+expect + "：正确率" + str(round(local_right / local_count*100, 2)) + '%'
    print(jieduan)
    print('接口名称：isCarImage\n共测试：' + str(total) + '张照片\n判断正确：' + str(right) + '张\n' + '正确率：' + str(
        round(right / total * 100, 2)) + '%')

'''
def category(resultpath, json, image):
    if json['result'] == 0:
        resultpath = resultpath + '/0/'
    elif json['result'] == 1:
        resultpath = resultpath + '/1/'
    elif json['result'] == 2:
        resultpath = resultpath + '/2/'
    temp = resultpath + image.split('\\')[-1]
    movefile(image, temp)
'''

if __name__ == '__main__':
    # temp=categoryData('E:\\test data\汽车之家论坛\汽车之家\\',11)
    # print(len(temp))
    # for t in temp:
    #     print(t)
    #     print(len(t))
    categoryTestOne(r'E:\\projects\\Car_classify')
    # categoryTestThreads('E:\\test data\汽车之家论坛\汽车之家\\',10)
    # print(iscarimage(r'D:\Documents\WeChat Files\Eason_King\FileStorage\File\2019-05\iscaroutput\iscaroutput\0\halfcar30 (2).jpg'))
    # images = glob.glob('E:\\test data\che168\*.jpg', recursive=True)
    # onecategory(images,'1')
    # for image in images:
    #     category('E:\\test data\che168\\',iscarimage(image),image)
