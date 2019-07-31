import urllib.request
import requests         
import os
import ctypes
from PIL import ImageFilter
from PIL import Image
def data():
    x = 1
    y = 1
    w = 1918
    h = 1078
    meng_url = "https://raw.githubusercontent.com/falacuijiahua/picgo/master/meng.png"#蒙版图片地址
    bing_url = "https://api.xygeng.cn/bing/1920.php"#bing图片api
    base = os.path.abspath(".")
    dir_name = os.path.join(base,"src")#图片存放目录
    return x, y, w, h, meng_url, bing_url, base, dir_name    
def set_img_as_wallpaper(finalpath):# 设置图片绝对路径 filepath 所指向的图片为壁纸
    ctypes.windll.user32.SystemParametersInfoW(20, 0, finalpath, 0)
    print("success!")
def save_images(src_url,meng_url,dirname):#储存图片到src目录中
    try:
        if not os.path.exists(dirname):
            print ('文件夹',dirname,'不存在，重新建立')
            #os.mkdir(dirname)
            os.makedirs(dirname)
        #获得图片文件名，包括后缀
        basename = "bingImage.jpg"
        mengname = "mengImage.jpg"
        #拼接目录与文件名，得到图片路径
        filepath_bing = os.path.join(dirname, basename)
        filepath_meng = os.path.join(dirname,mengname)
        #下载图片，并保存到文件夹中
        urllib.request.urlretrieve(src_url,filepath_bing)
        urllib.request.urlretrieve(meng_url,filepath_meng)
    except IOError as e:
        print ('文件操作失败',e)
    except Exception as e:
        print ('错误 ：',e)
    return filepath_bing , filepath_meng
def blend_two_images(meng_path,bing_path):
    img1 = Image.open(meng_path)
    img1 = img1.convert('RGBA')
    img2 = Image.open(bing_path)
    img2 = img2.convert('RGBA')   
    img = Image.blend(img1, img2, 0.3)
    img.save( "src/winpic.png")
def main():
    x, y, w, h, meng_url, bing_url, base, dir_name = data()#获取基础数据
    filepath_bing ,file_meng= save_images(bing_url,meng_url,dir_name)
    pic = Image.open(filepath_bing)
    finalpath = os.path.join(base,"src/winpic.jpg")
    modes = input("轮廓滤镜(0)\n浮雕滤镜(1)\n边界滤镜(2)\n灰暗滤镜(3)\n原图(任意键)\n请选择处理模式")
    if modes == "0":  
        piced = pic.filter(ImageFilter.CONTOUR ) #选择滤镜
        region = piced.crop((x, y, x+w, y+h))
        region.save("./src/winpic.jpg")
        print("你选择了轮廓滤镜")
        set_img_as_wallpaper(finalpath)    
    elif modes == "1":
        piced = pic.filter(ImageFilter.EMBOSS ) #选择滤镜
        region = piced.crop((x, y, x+w, y+h))
        region.save("./src/winpic.jpg") 
        print("你选择了浮雕滤镜")
        set_img_as_wallpaper(finalpath)  
    elif modes == "2":
        piced = pic.filter(ImageFilter.FIND_EDGES ) #选择滤镜
        region = piced.crop((x, y, x+w, y+h))
        region.save("./src/winpic.jpg") 
        print("你选择了边界滤镜")  
        set_img_as_wallpaper(finalpath)
    elif modes == "3":
        blend_two_images(file_meng,filepath_bing)   
        finalpath = os.path.join(base,"src/winpic.png")
        print("你选择了灰暗滤镜")
        set_img_as_wallpaper(finalpath)  
    else:
        finalpath = filepath_bing
        set_img_as_wallpaper(finalpath)
main()
# ImageFilter.BLUR 模糊滤镜
# ImageFilter.CONTOUR 轮廓
# ImageFilter.EDGE_ENHANCE 边界加强
# ImageFilter.EDGE_ENHANCE_MORE 边界加强(阀值更大)
# ImageFilter.EMBOSS 浮雕滤镜
# ImageFilter.FIND_EDGES 边界滤镜
# ImageFilter.SMOOTH 平滑滤镜
# ImageFilter.SMOOTH_MORE 平滑滤镜(阀值更大)
# ImageFilter.SHARPEN 锐化滤镜
# DETAIL 细节滤波