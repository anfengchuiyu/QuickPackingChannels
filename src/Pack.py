import os
import shutil
import zipfile


#应用名字，用于生成apk后命名
APP_NAME = 'zhixinzaixian'

#原apk文件，应该是纯净的apk,在META-INF目录下不含有自己添加的空文件
ORIGIN_APK_FILE = '../input/app-release.apk'

#渠道列表文件
CHANNELS_FILE = '../input/channel_list.txt'

#输出apk文件目录
OUPUT_DIR = '../output'

#要写入的空文件
EMPTY_FILE = '../input/empty_file.txt'


def init():
    if not os.path.exists(ORIGIN_APK_FILE) :
        raise RuntimeError('You must set the origin apk file for packing!')

    if not os.path.exists(OUPUT_DIR):
        os.mkdir(OUPUT_DIR)
    else:
        shutil.rmtree(OUPUT_DIR, ignore_errors=True)
        os.mkdir(OUPUT_DIR)

    #没有的话创建
    f = open(EMPTY_FILE, 'w')
    f.close()

def pack():
    f = open(CHANNELS_FILE)
    channels = f.readlines()
    channel_list = [str.strip() for str in channels]

    for channel in channel_list:
        # 每打一次包，需要拷贝下原apk
        targetApkFile = '../output/' + APP_NAME + "-release-" + channel + ".apk"
        shutil.copy(ORIGIN_APK_FILE, targetApkFile)

        zipped = zipfile.ZipFile(targetApkFile, 'a', zipfile.ZIP_DEFLATED)
        empty_channel_file = "META-INF/zxchannel_{channel}".format(channel=channel)
        zipped.write(EMPTY_FILE, empty_channel_file)
        zipped.close()


init()
pack()