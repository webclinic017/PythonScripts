from PIL import Image
import os

os.chdir("C:\\Users\\Basha Syed\\Desktop\\img2pdf_python")
avg_wid=0
avg_height=0
n=0
for img in os.listdir():
    
    if img.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        n+=1
        with Image.open(img) as image: 
            width, height = image.size
        print(width,height,sep=' X ')
        avg_wid+=width
        avg_height+=height
        
print('average width X height : '+str(avg_wid/n)+' X '+str(avg_height/n))
