from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kivy.graphics import Rectangle,Color

from kivy.garden.iconfonts import *

import os
from os.path import join, dirname
from PIL import Image as pillow


class ViewImage(ModalView):
    pass

class GalleryWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.images = self.get_imgs('imgs')
        # self.show_imgs(self.images)

        self.view_img_children = None

    def get_imgs(self, img_path):
        if not os.path.exists(img_path):
            print('Invalid Path...')
            return -1
        else:
            all_files = os.listdir(img_path)
            imgs = []
            for f in all_files:
                if f.endswith('.png') or f.endswith('.PNG') or f.endswith('.jpg') or f.endswith('.JPG') or f.endswith('.JPEG') or f.endswith('.jpeg'):
                    imgs.append('/'.join([img_path,f]))
            return imgs
    
    def show_imgs(self, imgs):
        base = self.ids.img_base
        base_data = []
        for img in imgs:
            im_name = img[img.rfind('/')+1:]
            if len(im_name) > 20:
                im_name = im_name[:18] + '...'
            base_data.append({'im_source':img,'im_caption':im_name})
        base.data = base_data

    def get_image(self, im_path):
        self.ids.img_base.data = []
        self.images = [im_path]
        self.show_imgs(self.images)
        self.ids.scrn_mngr.current = 'scrn_media'
        self.ids.scrn_open.trigger = ''
    def get_folder(self, im_path):
        self.ids.img_base.data = []
        self.images = self.get_imgs(im_path)
        self.show_imgs(self.images)
        self.ids.scrn_mngr.current = 'scrn_media'
    
    def next_image(self, inst):
        images = self.images
        cur_idx = None
        last_idx = len(images)-1
        view_children = inst.parent.parent.parent.children
        cur_img = None
        image_container = None

        for child in view_children:
            if str(child).find('BoxLayout') > -1:
                image_container = child.children[0]
                cur_img = image_container.source

        for i, img in enumerate(images):
            if img == cur_img:
                cur_idx = i

        if cur_idx != last_idx:
            nxt_img = images[cur_idx+1]
        else:
            nxt_img = images[0]

        image_container.source = nxt_img
    
    def prev_image(self, inst):
        images = self.images
        cur_idx = None
        last_idx = len(images)-1
        view_children = inst.parent.parent.parent.children
        cur_img = None
        image_container = None

        for child in view_children:
            if str(child).find('BoxLayout') > -1:
                image_container = child.children[0]
                cur_img = image_container.source

        for i, img in enumerate(images):
            if img == cur_img:
                cur_idx = i

        if cur_idx != 0:
            prev_img = images[cur_idx-1]
        else:
            prev_img = images[last_idx]

        image_container.source = prev_img

    def new_img_name(self, inst):
        view_children = inst.parent.parent.parent.children
        self.view_img_children = view_children
        new_name = TextInput(hint_text='New Image Name',multiline=False)
        new_name.bind(on_text_validate=self.rename_img)

        new_name_modal = ViewImage(size_hint=(None,None),size=(400,50))
        new_name_modal.add_widget(new_name)
        new_name_modal.open()
    
    def rename_img(self, inst):
        inst.parent.dismiss()
        new_name = inst.text
        view_children = self.view_img_children
        cur_img = None
        image_container = None

        for child in view_children:
            if str(child).find('BoxLayout') > -1:
                image_container = child.children[0]
                cur_img = image_container.source
        
        ext = cur_img[cur_img.rfind('.'):]

        try:
            im_path = cur_img[:cur_img.rfind('/')+1]
            os.rename(cur_img,im_path+new_name+ext)
            self.ids.img_base.data = []
            images = self.get_imgs('imgs')
            self.show_imgs(images)
            return True
        except Exception as e:
            print(e)
            return False


    
    def viewimg(self, instance):
        # print(instance.im_source)
        im = Image(source=instance.im_source)
        view_size = self.img_resize(im)

        effects_drop = DropDown()

        btn_prev = Button(text='%s'%(icon('zmdi-caret-left',24)),markup=True)
        btn_prev.bind(on_release=self.prev_image)
        btn_rename = Button(text='%s'%(icon('zmdi-file',24)),markup=True)
        btn_rename.bind(on_release=self.new_img_name)
        btn_effects = Button(text='%s'%(icon('zmdi-blur',24)),markup=True)
        btn_effects.bind(on_release=effects_drop.open)
        btn_next = Button(text='%s'%(icon('zmdi-caret-right',24)),markup=True)
        btn_next.bind(on_release=self.next_image)

        btn_mirror = Button(text='%s'%(icon('zmdi-border-vertical',28)),markup=True,size_hint_y=None,height=30)
        btn_mirror.bind(on_release=self.mirror_options)
        btn_burn = Button(text='%s'%(icon('zmdi-grain',28)),markup=True,size_hint_y=None,height=30)
        btn_burn.bind(on_release=self.burn_image)
        btn_flip = Button(text='%s'%(icon('zmdi-flip',28)),markup=True,size_hint_y=None,height=30)
        btn_flip.bind(on_release=self.flip_options)
        btn_rotate = Button(text='%s'%(icon('zmdi-rotate-ccw',28)),markup=True,size_hint_y=None,height=30)
        btn_rotate.bind(on_release=self.rotation_options)

        effects_drop.add_widget(btn_mirror)
        effects_drop.add_widget(btn_burn)
        effects_drop.add_widget(btn_flip)
        effects_drop.add_widget(btn_rotate)


        image_ops = BoxLayout(size_hint=(None,None),size=(200,30),spacing=4)
        image_ops.add_widget(btn_prev)
        image_ops.add_widget(btn_rename)
        image_ops.add_widget(btn_effects)
        image_ops.add_widget(btn_next)
        anchor = AnchorLayout(anchor_x='center',anchor_y='bottom')
        anchor.add_widget(image_ops)

        image_container = BoxLayout()


        view = ViewImage(size_hint=(None,None),size=view_size)
        with view.canvas.before:
            Color(1,1,1, .8)
            Rectangle(size=self.size, pos=self.pos, source=im.source)
        image_container.add_widget(im)
        view.add_widget(image_container)
        view.add_widget(anchor)
        view.open()
        self.view_img_children = view.children

    def burn_image(self, inst):
        view_children = self.view_img_children
        cur_img = None
        image_container = None

        for child in view_children:
            if str(child).find('BoxLayout') > -1:
                image_container = child.children[0]
                cur_img = image_container.source
        
        im = pillow.open(cur_img)

        source = im.split()
        R,G,B = 0, 1, 2
        mask = source[R].point(lambda i: i < 100 and 255)
        out = source[B].point(lambda i: i * 0.7)

        source[G].paste(out, None,mask)
        new_im = pillow.merge(im.mode, source)

        name = im.filename[:-4] + '_burn' + im.filename[-4:]
        im_cap = im.filename[im.filename.rfind('/')+1:]
        new_im.save(name)

        self.ids.img_base.data.insert(0,{'im_source':name,'im_caption':im_cap})
        self.ids.img_base.refresh_from_data()
        image_container.source = name
    
    def flip_options(self, inst):
        main_box = BoxLayout(orientation='vertical')

        box = BoxLayout(padding=10)
        horizontal_label = Label(text='Flip Horizontal',size_hint_x=.1)
        horizontal_check = CheckBox(state='down',size_hint_x=.1)
        lbl_sp = Label(size_hint_x=.3,text='')
        vert_label = Label(text='Flip Vertical',size_hint_x=.1)
        vert_check = CheckBox(size_hint_x=.1)

        box.add_widget(horizontal_label)
        box.add_widget(horizontal_check)
        box.add_widget(lbl_sp)
        box.add_widget(vert_label)
        box.add_widget(vert_check)



        main_box.add_widget(box)
        popup = Popup(title="Image Flip Options", content=main_box,size_hint=(.8,None),height=150)
        submit = Button(text='Submit',size_hint_y=None,height=30,on_release=lambda x: self.flip_image(popup,horizontal_check,vert_check))
        main_box.add_widget(submit)

        popup.open()

    def flip_image(self,inst, h, v):
        inst.dismiss()
        view_children = self.view_img_children
        cur_img = None
        image_container = None

        for child in view_children:
            if str(child).find('BoxLayout') > -1:
                image_container = child.children[0]
                cur_img = image_container.source

        im = pillow.open(cur_img)
        flip = None
        new_im = None
        
        if h.state == 'down':
            flip = im.transpose(pillow.FLIP_LEFT_RIGHT)
            new_im = flip
        if v.state == 'down':
            if flip != None:
                flip = flip.transpose(pillow.FLIP_TOP_BOTTOM)
            else:
                flip = im.transpose(pillow.FLIP_TOP_BOTTOM)
            new_im = flip

        name = im.filename[:-4] + '_flipped' + im.filename[-4:]
        im_cap = im.filename[name.rfind('/')+1:]
        new_im.save(name)

        self.ids.img_base.data.insert(0,{'im_source':name,'im_caption':im_cap})
        self.ids.img_base.refresh_from_data()
        image_container.source = name

    def mirror_options(self, inst):
        main_box = BoxLayout(orientation='vertical')
        full_img_box = BoxLayout(padding=10,size_hint_y=.3)
        sp = Label(text='',size_hint_x=.2)
        lbl = Label(text='Mirror Full Image',size_hint_x=.1)
        mirror_full_check = CheckBox(state='down',size_hint_x=.1)
        sp1 = Label(text='',size_hint_x=.2)
        full_img_box.add_widget(sp)
        full_img_box.add_widget(lbl)
        full_img_box.add_widget(mirror_full_check)
        full_img_box.add_widget(sp1)
        
        mirror_direction_box = BoxLayout(padding=20,size_hint_y=.6)
        mirror_left_lbl = Label(text='Mirror Left',size_hint_x=.1)
        mirror_left_check = CheckBox(state='down',size_hint_x=.1,group='direction')
        mirror_right_lbl = Label(text='Mirror Right',size_hint_x=.1)
        mirror_right_check = CheckBox(size_hint_x=.1,group='direction')

        mirror_direction_box.add_widget(mirror_left_lbl)
        mirror_direction_box.add_widget(mirror_left_check)
        mirror_direction_box.add_widget(mirror_right_lbl)
        mirror_direction_box.add_widget(mirror_right_check)
        
        submit = Button(text='Submit',size_hint_y=None,height=30)

        main_box.add_widget(full_img_box)
        main_box.add_widget(mirror_direction_box)
        main_box.add_widget(submit)

        popup = Popup(size_hint=(.8,None),height=250,title='Mirror Image Options',content=main_box)
        submit.bind(on_release=lambda x: self.mirror_image(popup,mirror_full_check,mirror_left_check,mirror_right_check))
        popup.open()

    def mirror_image(self, modal,full, left, right):
        modal.dismiss()
        view_children = self.view_img_children
        cur_img = None
        image_container = None

        for child in view_children:
            if str(child).find('BoxLayout') > -1:
                image_container = child.children[0]
                cur_img = image_container.source
            
        og = pillow.open(cur_img)

        if full.state == 'down':
            flip = og.transpose(pillow.FLIP_LEFT_RIGHT)
            flip_pos = (og.size[0],0)
            back_size = [og.size[0]*2,og.size[1]]
        else:
            og_half = (0,0,int(og.size[0]/2),int(og.size[1]))
            flip_pos = (og_half[2],0)

            im = og.crop(og_half)
            flip = im.transpose(pillow.FLIP_LEFT_RIGHT)
            back_size = [og.size[0]-2, og.size[1]]
        
        back = pillow.new('RGBA',back_size,'white')

        if left.state == 'down':    
            back.paste(og,(0,0))
            back.paste(flip,flip_pos)
        else:
            back.paste(flip,(0,0))
            back.paste(og,flip_pos)
        
        new_im = back
        im = og

        name = im.filename[:-4] + '_mirrored' + im.filename[-4:]
        im_cap = name[name.rfind('/')+1:]
        new_im.save(name)

        self.ids.img_base.data.insert(0,{'im_source':name,'im_caption':im_cap})
        self.ids.img_base.refresh_from_data()
        image_container.source = name

    def rotation_options(self, inst):
        box = BoxLayout(padding=20)
        lbl = Label(text='Rotation Degrees',size_hint_x=.1)
        rotation = Spinner(text='45',values=['45','90','135','180','225','270','315'],size_hint=(.1,None),height=30)

        submit = Button(text='Submit',size_hint_y=None,height=30)

        box.add_widget(lbl)
        box.add_widget(rotation)
        main_box = BoxLayout(orientation='vertical')
        main_box.add_widget(box)
        main_box.add_widget(submit)
        popup = Popup(size_hint=(.8,None),height=150,title='Choose Rotation Angle',content=main_box)
        submit.bind(on_release=lambda x: self.rotate_image(popup,rotation.text))
        popup.open()
    
    def rotate_image(self,modal,deg):
        modal.dismiss()
        view_children = self.view_img_children
        cur_img = None
        image_container = None

        for child in view_children:
            if str(child).find('BoxLayout') > -1:
                image_container = child.children[0]
                cur_img = image_container.source
            
        im = pillow.open(cur_img)

        new_im = im.rotate(int(deg))

        name = im.filename[:-4] + '_rotated' + im.filename[-4:]
        im_cap = name[name.rfind('/')+1:]
        new_im.save(name)

        self.ids.img_base.data.insert(0,{'im_source':name,'im_caption':im_cap})
        self.ids.img_base.refresh_from_data()
        image_container.source = name

    def img_resize(self, img):
        im_size_x, im_size_y = img.texture_size
        ratio = im_size_x/im_size_y
        aspect = self.aspect_ratio(ratio,50)

        while im_size_x >= Window.width or im_size_y >= Window.height:
            if im_size_x > im_size_y:
                im_size_x -= aspect[0]
                im_size_y -= aspect[1]
            else:
                im_size_y -= aspect[1]
        return [im_size_x,im_size_y]
    
    def aspect_ratio(self,val, lim):

        lower = [0, 1]
        upper = [1, 0]

        while True:
            mediant = [lower[0] + upper[0], lower[1] + upper[1]]

            if val * mediant[1] > mediant[0]:
                if lim < mediant[1]:
                    return upper
                
                lower = mediant
            elif val * mediant[1] == mediant[0]:
                if lim >= mediant[1]:
                    return mediant
                
                if lower[1] < upper[1]:
                    return lower
                
                return upper;
            else:
                if (lim < mediant[1]):
                    return lower
                upper = mediant
    

class GalleryApp(App):
    def build(self):

        return GalleryWindow()

if __name__=='__main__':
    register('default_font','./assets/fonts/Material-Design-Iconic-Font.ttf',join(dirname(__file__),'assets/fonts/zmd.fontd'))
    
    GalleryApp().run()