import cv2
import time
import os
from PIL import Image,ImageFont,ImageDraw
from cv2 import VideoWriter,VideoWriter_fourcc,imread,resize
import re
import subprocess
Image.MAX_IMAGE_PIXELS = None
class V2Char:

    fontSize = 100
    fontSizes = [200,106,72,52,42]
    #strChar = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'."
    strChar = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]-_+~<>i!lI;:,^`'"
    dic = {
           "$":"江湖风波恶\n人间行路难\n世人皆负我\n举世皆可杀\n君子死知己",
           "@":"花间一壶酒\n独酌无相亲\n七窍三秋钉\n三载赴幽冥\n凭酒寄红颜",
           "B":"我不知道你\n什么时候来\n山怎么来河\n但我知道令\n你一定会来",
           "%":"山河不足重\n重在遇知己\n你身上有光\n我抓来看看\n山河令山河",
           "8":"但度无所苦\n我自迎接汝\n世上本无事\n庸人自扰之\n山河令山河",
           "&":"传男不传女\n传媳不传婿\n四季花常在\n九州事尽知\n山河令山河",
           "W":"翩翩君子\n温润如玉\n八面玲珑\n和气生财",
           "M":"天涯孤鸿\n无根行客\n执子之手\n坐看云舒",
           "#":"风雨如晦\n鸡鸣不已\n既见君子\n云胡不喜",
           "*":"倾盖如故\n白首如新\n高山流水\n知音难觅",
           "o":"地狱不空\n誓不成佛\n知己既去\n何若玉碎",
           "a":"一入鬼谷\n阴阳两个\n一入红尘\n便生因果",
           "h":"人生得意\n须尽欢莫\n使金樽空\n对月山河",
           "k":"花开早山\n天知晓河\n天莫笑令\n天已老山",
           "b":"周而不比\n身若飞絮\n得君为友\n不枉此生",
           "d":"飘飘兮\n若流风\n之回雪",
           "p":"仿佛兮\n若轻云\n之蔽月",
           "q":"心地向\n善便不\n算恶人",
           "w":"岂不闻\n烈女怕\n缠郎山",
           "m":"腰细腿\n长嘴硬\n心软河",
           "Z":"今晚的\n夜色很\n美哦令",
           "O":"幸得君\n心山似\n我心河",
           "0":"今晚的\n夜色很\n美哦令",
           "Q":"三生石\n上旧精\n魂山河",
           "L":"周相公\n山可怜\n则个吧",
           "C":"唯君河\n与吾令\n足以山",
           "J":"五湖水\n天下汇\n你不配",
           "U":"世事\n蹉跎",
           "Y":"死生\n契阔",
           "X":"情场\n得意",
           "z":"战场\n失意",
           "c":"凉雨\n知秋",
           "v":"青梧\n老死",
           "u":"天涯\n浪客",
           "n":"省省\n吧你",
           "x":"温周\n之恋",
           "r":"阿絮\n阿絮",
           "j":"四季\n山庄",
           "f":"千山\n暮雪",
           "t":"老温\n老温",
           "/":"六合\n心法",
           "|":"尊重\n爱情",
           "(":"美吗\n完美",
           ")":"娘了\n个腿",
           "1":"不合\n时宜",
           "{":"一荣\n俱荣",
           "}":"一损\n俱损",
           "[":"甄",
           "]":"衍",
           "-":"阿",
           "_":"絮",
           "+":"温",
           "~":"客",
           "<":"行",
           ">":"周",
           "i":"子",
           "!":"舒",
           "l":"知",
           "I":"己",
           ";":"山",
           ":":"河",
           ",":"令",
           "^":"天",
           "`":"涯",
           "'":"客"
           }
    size = ()
    path = ''
    fps = 0
    splitTag = 'e'
    pixelRate = 7

    def __init__(self, path, size = ()):
        self.path = path
        self.size = size

    def pixel2Char(self, luminance):
        gray = int(0.2126 * luminance[0] + 0.7152 * luminance[1] + 0.0722 * luminance[2])
        return self.strChar[int((gray / 256) * len(self.strChar))]

    def image2Char(self, imgPixels):
        #if self.size != () and (imgPixels.shape[0] > self.size[1] or imgPixels.shape[1] > self.size[0]):
            #imgPixels = cv2.resize(imgPixels, self.size, interpolation=cv2.INTER_NEAREST)
        if self.size == ():
            self.size = (int(imgPixels.shape[1]/self.pixelRate), int(imgPixels.shape[0]/self.pixelRate))
        imgPixels = cv2.resize(imgPixels, self.size, interpolation=cv2.INTER_NEAREST)
        imgPixelsChar = ''
        color = []
        #blank = ' ' * (self.size[0] - imgPixels.shape[1]) + '\n'
        blank = self.splitTag
        for i in range(imgPixels.shape[0]):
            for j in range(imgPixels.shape[1]):
                temp = imgPixels[i, j]
                imgPixelsChar += self.pixel2Char(temp)
                color.append((temp[0], temp[1], temp[2]))
            if i < imgPixels.shape[0] - 1:
                imgPixelsChar += blank
        return (imgPixelsChar, color)

    def video2Char(self):
        videoChar = []
        colors = []
        cap = cv2.VideoCapture(self.path)
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        nf = int(cap.get(7))
        for i in range(nf):
            raw = cap.read()
            if not raw[0]:
                continue
            rawFrame = cv2.cvtColor(raw[1], cv2.COLOR_BGR2RGB)
            imgPixelsChar, color = self.image2Char(rawFrame)
            videoChar.append(imgPixelsChar)
            colors.append(color)
        cap.release()
        return (videoChar, colors)

    def image2Char2image(self, videoChar, colors):
        catalog = self.path.split('.')[0]
        self.mkdir(catalog)
        font = ImageFont.truetype(os.path.join("fonts", "STXINGKA.TTF"), self.fontSize)
        leWidth=self.maxWidth()
        lineHeight=font.getsize("我")[1]*2

        col, row = self.size
        imageWidth = leWidth * col
        imageHeight = lineHeight * row
        for p_id,imageChar in enumerate(videoChar):
            imageCharLines = imageChar.split(self.splitTag)
            im = Image.new("RGB", (imageWidth, imageHeight), (255, 255, 255))
            dr = ImageDraw.Draw(im)
            for line,imageCharLine in enumerate(imageCharLines):
                for column in range(len(imageCharLine)):
                    content = self.dic[imageCharLine[column]]
                    font = ImageFont.truetype(os.path.join("fonts", "STXINGKA.TTF"), self.fontSizes[content.count('\n')])
                    dr.text((column*leWidth,line*lineHeight), content,
                            font=font, fill=colors[p_id][int(line*self.size[0]+column)])
            im.save(catalog+r'\pic_{}.jpg'.format(p_id))
            del dr

    def image2Video(self):
        catalog=self.path.split('.')[0]
        images=os.listdir(catalog + '-zip')
        images.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))
        im=Image.open(catalog+'-zip\\'+images[0])
        fourcc = VideoWriter_fourcc(*"MJPG")
        vw = VideoWriter(catalog + '.avi', fourcc, self.fps, im.size)
        for image in images:
            frame=cv2.imread(catalog+'-zip\\'+image)
            vw.write(frame)
        vw.release()
            


    def mkdir(self,catalog):
        isExists = os.path.exists(catalog)
        if not isExists:
            os.makedirs(catalog)
            return True
        else:
            return False

    def removeDir(self, catalog):
        if os.path.exists(catalog):
            if os.path.isdir(catalog):
                dirs = os.listdir(catalog)
                for d in dirs:
                    self.removeDir(catalog+'/'+d)
                os.rmdir(catalog)
                return
            elif os.path.isfile(catalog):
                os.remove(catalog)
            return


    def maxWidth(self):
        
        font = ImageFont.truetype(os.path.join("fonts", "STXINGKA.TTF"), self.fontSize)
        return font.getsize("我我")[0]
        
        #font = ImageFont.truetype(os.path.join("fonts", "STXINGKA.TTF"), 14)
        #fontSize=[]
        #for i in self.strChar:
            #fontSize.append(font.getsize(i)[0])
        #return max(fontSize)

    def videoAddMusic(self):
        catalog=self.path.split('.')[0]
        videoPath=catalog + '.avi'
        musicPath=catalog + '.mp3'
        outfileName = catalog+'-char.mp4'
        #ffmpeg -i D:\charvideo\video1.avi -i D:\charvideo\video1.mp3 -strict -2 -f mp4 D:\charvideo\video1-char.mp4
        addCommand='"C:\\Users\\茯苓\\Downloads\\ffmpegwin\\ffmpeg\\ffmpeg-20180605-b748772-win64-static\\bin\\ffmpeg.exe" -i "{}" -i "{}" -strict -2 -f mp4 "{}"'.format(videoPath,musicPath,outfileName)
        aa = subprocess.call(addCommand,shell = True)

    def zipImages(self):
        catalog = self.path.split('.')[0] + '-zip'
        self.mkdir(catalog)
        catalog2=self.path.split('.')[0]
        images=os.listdir(catalog2)
        for image in images:
            zipCommand = '"C:\\Users\\茯苓\\Downloads\\ffmpegwin\\ffmpeg\\ffmpeg-20180605-b748772-win64-static\\bin\\ffmpeg.exe" -i "{0}" -vf scale=iw/14:ih/14 -lossless 0 -quality 75 "{1}"'.format(catalog2 + '\\'+image,catalog + '\\'+image)
            subprocess.call(zipCommand, shell = True)

if __name__ == '__main__':
    v2char = V2Char(r'D:\charvideo\wz.mp4')
    #v2char.fps = 25
    print('video2Char ing')
    videoChar, colors = v2char.video2Char()
    print('video2Char Finished')
    print('image2Char2image ing')
    v2char.image2Char2image(videoChar, colors)
    print('image2Char2image Finished')
    print('zipImages ing')
    v2char.zipImages()
    #v2char.removeDir(v2char.path.split('.')[0])
    print('zipImages Finished')
    print('image2Video ing')
    v2char.image2Video()
    print('image2Video Finished')
    print('videoAddMusic ing')
    v2char.videoAddMusic()
    print('videoAddMusic Finished')
    print('removeDir ing')
    #v2char.removeDir(v2char.path.split('.')[0] + '-zip')
    #v2char.removeDir(v2char.path.split('.')[0] + '.mp3')
    #v2char.removeDir(v2char.path.split('.')[0] + '.avi')
    print('removeDir Finished')
    print('Finished')
    
            
        
        
