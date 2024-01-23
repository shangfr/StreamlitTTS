# -*- coding: utf-8 -*-
"""
Created on Tue May  9 15:31:28 2023

@author: shangfr
"""
import numpy as np
from PIL import Image
from pathlib import Path
from moviepy import editor
from moviepy.video.tools.subtitles import SubtitlesClip

'''
Creating class MP3ToMP4 which contains methods to convert
an audio to a video using a list of images.
'''

def file_to_subtitles(filename):
    import webvtt
    """ Converts a srt file into subtitles.

    The returned list is of the form ``[((ta,tb),'some text'),...]``
    and can be fed to SubtitlesClip.

    Only works for '.srt' format for the moment.
    """
    times_texts = []
    current_times = None
    current_text = ""
    
    subtitles = webvtt.read(filename)

    for subtitle in subtitles:
        current_times = [subtitle.start_in_seconds,subtitle.end_in_seconds]
        current_text = subtitle.text.strip('\n')
        times_texts.append((current_times, current_text))

        
    return times_texts

class MP324:

    def __init__(self,img_list,title, output_folder_path):
        """
        :param folder_path: contains the path of the root folder.
        :param audio_path: contains the path of the audio (mp3 file).
        :param video_path_name: contains the path where the created
                                video will be saved along with the
                                name of the created video.
        """
        self.title = title
        self.folder_path = output_folder_path+'/images'
        self.audio_path = output_folder_path+'/audio.mp3'
        self.video_path_name = output_folder_path+'/video.mp4'
      
        self.audio = editor.AudioFileClip(self.audio_path)
        if not img_list:
            self.img_list = self.get_images()
        else:
            self.img_list = img_list
            

        # Calling the create_video() method.
        self.create_video()

    def get_images(self):
        """
        This method reads the filenames of the images present
        in the folder_path of type '.png' and stores it in the
        'images' list.

        Then it opens the images, resizes them and appends them
        to another list, 'image_list'

        :return: list of opened images
        """
        path_images = Path(self.folder_path)
        images = list(path_images.glob('*.png'))
        image_list = list()
        for image_name in images:
            image = Image.open(image_name)#.resize((800, 800), Image.ANTIALIAS)
            image_list.append(image)
        return image_list

    def get_subtitles(self):
        """
        set_position:設置文字顯示位置【屏幕左上角为(0, 0)，右下角为(屏幕宽度, 屏幕高度)】
            1、set_position((800, 500)): 显示在800, 500的位置上
            2、set_position(("center", "center")): 显示在屏幕的正中央
            3、set_position((0.4, 0.6), True): 显示在距离左边百分之40、距离上边百分之60的位置上
        set_duration(10): 持续10秒
        set_opacity(0.6): 设置透明度为0.6
        set_start(5)：设置开始显示的时间点
        set_end(10):设置结束的时间点
        """
        # 创建字幕剪辑
        vtt_path = self.audio_path.replace("mp3","vtt")
        subtitles = file_to_subtitles(vtt_path)

        generator = lambda txt: editor.TextClip(txt, font='output/STKAITI.TTF', fontsize=50, color='green', transparent=True)
        
        subtitles_clip = SubtitlesClip(subtitles, generator)
        return subtitles_clip
        

    def create_video(self):
        """
        This method calls the get_length() and get_images()
        methods internally. It then calculates the duration
        of each frame. After that, it saves all the opened images
        as a gif using the save() method. Finally it calls the
        combine_method()

        :return: None
        """
        # Import the audio(Insert to location of your audio instead of audioClip.mp3)
        
        #image_clip = ImageClip(str(images[0]))
        
        
        images = [np.array(img) for img in self.img_list]
        img_duration = self.audio.duration/len(images)
        
        image_clip = [editor.ImageClip(m).set_duration(img_duration) for m in images]
        concat_clip = editor.concatenate_videoclips(image_clip, method="compose")
        
        
        # Generate a text clip 
        text_clip = editor.TextClip(txt=self.title,
                             size=(.5*image_clip[0].size[0], 0),
                             font='STKAITI.TTF',
                             color="#00CD00")
        
        im_width, im_height = text_clip.size
        title_bg_clip = editor.ImageClip("output/title_bubble.png").resize((int(im_width*1.5),int(im_height*1.5)))
          
        #color_clip = editor.ColorClip(size=(int(im_width*1.2), int(im_height*1.1)), color=(0, 255, 255))
        title_clip = editor.CompositeVideoClip([title_bg_clip.set_opacity(.8), text_clip.set_position('center')])
        
        subtitles_clip = self.get_subtitles()
        
        conten_clip = editor.CompositeVideoClip([concat_clip, title_clip.set_position('center').set_duration(2).crossfadeout(1), subtitles_clip.set_position('bottom')]).set_duration(self.audio.duration)
        output_video = conten_clip.set_audio(self.audio)
        output_video.write_videofile(self.video_path_name, fps=1)
        
        
    def combine_audio(self):
        """
        This method attaches the audio to the gif file created.
        It opens the gif file and mp3 file and then uses
        set_audio() method to attach the audio. Finally, it
        saves the video to the specified video_path_name

        :return: None
        """
        video = editor.VideoFileClip(self.folder_path + "/temp.gif")
        final_video = video.set_audio(self.audio)


        final_video.write_videofile(self.video_path_name, fps=60)


    def create_gif(self):
        """
        This method calls the get_length() and get_images()
        :return: None
        """
        length_audio = self.get_length()
        image_list = self.img_list
        duration = int(length_audio / len(image_list)) * 1000
        image_list[0].save(self.folder_path + "/temp.gif",
                           save_all=True,
                           append_images=image_list[1:],
                           duration=duration)




if __name__ == '__main__':

    title  = 'TEST'
    output_folder_path = 'output'
    # Invoking the parameterized constructor of the MP3ToMP4 class.
    MP324([],title, output_folder_path)
