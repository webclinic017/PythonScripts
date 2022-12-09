from PIL import Image
import os
import time

#os.chdir("C:\\Users\\Basha Syed\\Desktop\\img2pdf_python")
new_width=200
a4_aspect_ratio=0.70711

def image_resize(file_obj,new_width):
    width, height = file_obj.size
    if width>height :
        file_obj=file_obj.rotate(angle=90,expand=True)
        width, height = file_obj.size
    aspect_ratio=width/height

    # Find a width and height that would fix the 
    while True:
        if round(aspect_ratio,3) != round(a4_aspect_ratio,3) and aspect_ratio < a4_aspect_ratio:
            width+=2
        elif round(aspect_ratio,3) != round(a4_aspect_ratio,3) and aspect_ratio > a4_aspect_ratio:
            height+=2
        else:
            break
        aspect_ratio=width/height

    return file_obj.resize((width,height))


image_list=[]
resized_image_list=[]
for img in os.listdir():
    print(img)
    if img.lower().endswith(('.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        curr_image=Image.open(img)
        image_list.append(curr_image)
        resized_image_list.append(image_resize(curr_image,new_width)) # Call this to resize the image
        #resized_image_list[-1].show()

        # To create a PDF without re-sizing
        # resized_image_list.append(curr_image)

# Generate PDF
resized_image_list[0].save("something.pdf","PDF",save_all=True,append_images=resized_image_list[1:])
#print(resized_image_list)



#Close all the images
for piclose in image_list:
    piclose.close()
