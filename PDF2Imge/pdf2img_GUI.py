from pdf2image import convert_from_path
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import os


def pdf2img():
	try:
		print(os.stat(str(e1.get())))
		images = convert_from_path(str(e1.get()))
		for i,img in enumerate(images):
			output=str(e1.get()).split('.')[0]+'_'+str(i+1)
			img.save('{}.jpg'.format(output), 'JPEG')

	except :
		print(str(e1.get()))
		Result = "NO pdf found"
		messagebox.showinfo("Result", Result)

	else:
		Result = "success"
		messagebox.showinfo("Result", Result)

# defining open_file_chooser function
def open_file_chooser():
	filename = askopenfilename(initialdir = os.curdir ,title = "Select a File")
	e1.insert(0,filename)
	print("You have selected : %s" % filename)
	# os.chdir(os.path.dirname(filename))


master = Tk()
Label(master, text="File Location").grid(row=0, sticky=W)
master.geometry('350x250+700+200')
# Button : Open
open = Button(master, text = "Browse", command = open_file_chooser)

e1 = Entry(master)
e1.grid(row=0, column=1)

b = Button(master, text="Convert", command=pdf2img)
b.grid(row=1, column=1,columnspan=2, rowspan=2,padx=5, pady=5)
open.grid(row=0, column=2,columnspan=2, rowspan=2,padx=5, pady=5)

mainloop()
