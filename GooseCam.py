import socket
import time
import math			
from tkinter import*
from tkinter import ttk
from tkinter.font import Font
import tkinter.scrolledtext as ScrolledText
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk, ImageDraw

# ( ) upload, download, progressbar

# (?) off auch in rot bei Fehler  
# ( ) bei laufender Aufnahme delete ausschalten!!!
# ( ) Enter ... bei den anderen sachen binden!

#________________
# ( ) testshot
# ( ) settings
# ( ) 

def get_min(root):
    if root.winfo_screenheight()/900 > root.winfo_screenwidth()/1600:
        return root.winfo_screenwidth()/1600
    else:
        return root.winfo_screenheight()/900
def get_goosecams(root,n,i):
	root.hist_t.config(state='normal')
	if i <= n-2:
		try:
			if i == 0:
				ip = socket.gethostbyname('goosecam.local')
			else:
				ip = socket.gethostbyname('goosecam' + str(i) + '.local')
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect((ip, root.port))
				s.send(bytes('test', 'UTF-8'))
				s.close()
				if ip not in root.serverMacAddress:
					root.serverMacAddress.append(ip)
					root.camera_t.insert(END,ip)
					pos = root.pos_entry.get()
					root.position_t.insert(END,pos)
					root.hist_t.insert(END, ip+': added\n')
				else:
					root.hist_t.insert(END, ip+' is already in use\n')
			except:
				print('you have to start server on ' + ip)
				root.lab.config(bg='red')
		except:
			print('adding goosecam failed')
		root.cam_prog['value'] = i+1
		root.after(100,get_goosecams,root,n,i+1)
	elif i==n-1:
		root.ip_lab.place_forget()
		root.ip_entry.place_forget()
		root.ip_entry.delete(0,END)
		root.pos_lab.place_forget()
		root.pos_entry.place_forget()
		root.pos_entry.delete(0,END)
		root.add_b.place_forget()
		root.cams_b.place_forget()
		root.camera_t.place(relx=.515, rely=.17, relwidth=.22, relheight=.185)
		root.position_t.place(relx=.735, rely=.17, relwidth=.225, relheight=.185)
		root.scrollbar.place(relx=.97, rely=.17, relwidth=.01, relheight=.185)
		root.set_b.place(relx=.515, rely=.36, relwidth=.089, relheight=.03)
		root.test_b.place(relx=.609, rely=.36, relwidth=.089, relheight=.03)
		root.up_b.place(relx=.703, rely=.36, relwidth=.089, relheight=.03)
		root.down_b.place(relx=.797, rely=.36, relwidth=.089, relheight=.03)
		root.del_b.place(relx=.891, rely=.36, relwidth=.089, relheight=.03)
		root.add_camera_b.place(relx=.93, rely=.12, relwidth=.05, relheight=.04)
		root.cam_prog.place_forget()
	root.hist_t.config(state='disabled')
	root.select_box['values'] = root.serverMacAddress
def update_time(root): 
	t = time.time() - root.t0
	h = math.floor(t/3600)
	min = math.floor((t%3600)/60)
	sec = math.floor((t%3600) %60)
	if root.recvalue == 1:
		root.after(1000, update_time, root)
		root.time_lab.config(text=str(h).zfill(2)+':'+str(min).zfill(2)+':'+str(sec).zfill(2))
		for i in range(len(root.serverMacAddress)):
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect((root.serverMacAddress[i], root.port))
				s.send(bytes('test', 'UTF-8'))
				s.close()
				root.lab.config(bg='grey')
			except:
				root.hist_t.config(state='normal')
				root.hist_t.insert(END, root.serverMacAddress[i] + ': connection failed\n','err')
				root.hist_t.config(state='disabled')
				print('error')
				root.recvalue = 0
				root.lab.config(bg='red')
def status(root):
	root.hist_t.config(state='normal')
	for i in range(len(root.serverMacAddress)):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((root.serverMacAddress[i], root.port))
			s.send(bytes('status,'+str(root.stat_var.get()),'UTF-8'))
			s.close()
			root.lab.config(bg='grey')
			if root.stat_var.get() == 1:
				root.hist_t.insert(END, root.serverMacAddress[i] + ': status on\n')
			else:
				root.hist_t.insert(END, root.serverMacAddress[i] + ': status off\n') 
		except:
			print('no camera connected')
			root.lab.config(bg='red')
	root.hist_t.yview(END) #autoscroll to bottom
	root.hist_t.config(state='disabled')
def light(root,state):
	root.hist_t.config(state='normal') 
	for i in range(len(root.serverMacAddress)):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((root.serverMacAddress[i], root.port))
			if state == 1:
				message = 'light-on'
				root.light_b.config(text='light off',command=lambda:light(root,0))
			elif state == 0:
				message = 'light-off'
				root.light_b.config(text='light on', command=lambda: light(root,1))
			s.send(bytes(message,'UTF-8'))
			s.close()
			root.lab.config(bg='grey')
			root.hist_t.insert(END, root.serverMacAddress[i] + ': '+ message+'\n') 
		except:
			print('no camera connected')
			root.lab.config(bg='red')
			root.hist_t.insert(END, root.serverMacAddress[i] + ': light on/off failed\n','err') 
	root.hist_t.yview(END) #autoscroll to bottom
	root.hist_t.config(state='disabled')
def start_video(root,title):
	root.hist_t.config(state='normal') 
	if title != '':
		for i in range(len(root.serverMacAddress)):
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect((root.serverMacAddress[i], root.port))
				s.send(bytes('start_video,'+'cam'+root.serverMacAddress[i].split('.')[-1]+'_'+str(title),'UTF-8'))
				s.close()

				root.bind('g', lambda event: annotate_text(root,'Gänsehaut'))
				root.video_b.config(text= 'stop video', command= lambda: stop_video(root))
				root.light_b.config(text='light off', command=lambda: light(root, 0))
				root.text_tv.delete(0,END)
				root.text_e.config(state='normal')
				root.text_tv.place_forget()
				root.time_lab.place(relx=.23, rely=.32, relwidth=.255, relheight=.06)
				root.add_camera_b.config(state='disabled')
				root.lab.config(bg='grey')
				root.recvalue = 1
				root.t0=time.time()
				update_time(root)
				print(root.serverMacAddress[i] + ': start-video: ' + title + '.h264\n')
				root.hist_t.insert(END, root.serverMacAddress[i] + ': start-video: ' + title + '.h264\n')
				print('hi')
			except:
				root.hist_t.insert(END, 'start-video failed\n','err')
				root.lab.config(bg='red')
	else:
		root.hist_t.insert(END, 'please enter title!\n')
	root.hist_t.yview(END) #autoscroll to bottom
	root.hist_t.config(state='disabled')
def stop_video(root):
	root.hist_t.config(state='normal')
	for i in range(len(root.serverMacAddress)):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((root.serverMacAddress[i], root.port))
			s.send(bytes('stop_video', 'UTF-8'))
			s.close()

			root.bind('g')
			root.video_b.config(text='start video', command=lambda: start_video(root,root.text_tv.get()))
			root.light_b.config(text='light on', command=lambda: light(root, 0))
			root.text_tv.place(relx=.23, rely=.32, relwidth=.255, relheight=.06)
			root.time_lab.place_forget()
			root.add_camera_b.config(state='normal')
			root.lab.config(bg='grey')
			root.recvalue = 0
			root.hist_t.insert(END, root.serverMacAddress[i] + ': stop-video\n')
		except:
			root.hist_t.insert(END, 'stop-video failed\n','err')
			root.lab.config(bg='red')
	root.hist_t.yview(END) #autoscroll to bottom
	root.hist_t.config(state='disabled')
	root.text_e.config(state='disabled')
def photo(root,title):
	root.hist_t.config(state='normal')
	if title != '':
		for i in range(len(root.serverMacAddress)):
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect((root.serverMacAddress[i], root.port))
				s.send(bytes('photo'+','+'cam'+root.serverMacAddress[i].split('.')[-1]+'_'+title, 'UTF-8'))
				s.close()
				root.text_tp.delete(0, END)
				root.lab.config(bg='grey')
				root.hist_t.insert(END, root.serverMacAddress[i] + ': photo '+ title +'.jpg\n')
			except:
				root.hist_t.insert(END, root.serverMacAddress[i] + ': photo failed\n','err')
				root.lab.config(bg='red')
	else:
		root.hist_t.insert(END, 'please enter title\n')
	root.hist_t.yview(END) #autoscroll to bottom
	root.hist_t.config(state='disabled')
def annotate_text(root,text):
	root.hist_t.config(state='normal')
	for i in range(len(root.serverMacAddress)):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((root.serverMacAddress[i], root.port))
			s.send(bytes('annotate'+','+text+';', 'UTF-8'))
			s.close()
			root.text_e.delete(0, END)
			root.lab.config(bg='grey')
			root.hist_t.insert(END,root.serverMacAddress[i] + ': annotate: '+text+'\n')
		except:
			root.hist_t.insert(END, root.serverMacAddress[i] + ': annotation failed\n','err')
			root.lab.config(bg='red')
	root.hist_t.yview(END) #autoscroll to bottom
	root.hist_t.config(state='disabled')
def init_set(root):
	root.selected_cams = []
	for i in root.camera_t.curselection():
		root.selected_cams.append(i)
	
	print(root.selected_cams)
	for i in range(len(root.frame_elements)):
		root.frame_elements[i].place_forget()
	root.frame_elements = []
	
	root.frame_elements.append(Label(text='settings',  bg='grey',font=root.buttonfont))
	root.frame_elements[-1].place(relx=.515, rely=.42, relwidth=.465, relheight=.04)
	
	root.frame_elements.append(Label(text='brightness',  bg='lightgrey',font=root.buttonfont))
	root.frame_elements[-1].place(relx=.515, rely=.47, relwidth=.2, relheight=.04)
	
	root.frame_elements.append(Scale(font=root.scalefont, orient='horizontal',bg='lightgrey', highlightthickness=0 ,from_ =0, to=100, resolution=1))
	root.frame_elements[-1].place(relx=.725, rely=.47, relwidth=.255, relheight=.05)
	root.frame_elements[-1].set(50)
	
	root.frame_elements.append(Label(text='resolution',  bg='lightgrey',font=root.buttonfont))
	root.frame_elements[-1].place(relx=.515, rely=.53, relwidth=.2, relheight=.04)
	
	root.frame_elements.append( Entry(font=root.buttonfont))
	root.frame_elements[-1].place(relx=.725, rely=.53, relwidth=.1, relheight=.04)
	root.frame_elements[-1].insert(END,'480')
	
	root.frame_elements.append(Label(text='x',  bg='lightgrey',font=root.buttonfont))
	root.frame_elements[-1].place(relx=.825, rely=.53, relwidth=.055, relheight=.04)
	
	root.frame_elements.append( Entry(font=root.buttonfont))
	root.frame_elements[-1].place(relx=.88, rely=.53, relwidth=.1, relheight=.04)
	root.frame_elements[-1].insert(END,'480')
	
	root.frame_elements.append(Label(text='fps',  bg='lightgrey',font=root.buttonfont))
	root.frame_elements[-1].place(relx=.515, rely=.58, relwidth=.2, relheight=.04)
	
	root.frame_elements.append(Scale(font=root.scalefont, orient='horizontal',bg='lightgrey', highlightthickness=0, from_ =0, to=30))
	root.frame_elements[-1].place(relx=.725, rely=.58, relwidth=.255, relheight=.05)
	root.frame_elements[-1].set(10)
	
	root.frame_elements.append(Button(text='set', command=lambda:set(root, root.frame_elements[2].get(), root.frame_elements[4].get()+'x'+root.frame_elements[6].get(), root.frame_elements[8].get()), bg='grey',font=root.buttonfont))
	root.frame_elements[-1].place(relx=.93, rely=.79, relwidth=.05, relheight=.04)
def set(root, bright, res, fps):
	for i in range(len(root.frame_elements)):
		root.frame_elements[i].place_forget()
	root.frame_elements = []
	
	root.hist_t.config(state='normal')
	for i in root.camera_t.curselection():
		try:
			print(str(bright))
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((root.camera_t.get(i), root.port))
			s.send(bytes('set'+','+str(bright)+','+str(res)+','+str(fps), 'UTF-8'))
			s.close()
			root.lab.config(bg='grey')
			root.hist_t.insert(END, root.camera_t.get(i) + ': set: \n\tbrightness: '+str(bright)+'%\n\tresolution: '+str(res)+'\n\tframes per second: '+str(fps)+'\n')
		except:
			root.lab.config(bg='red')
			root.hist_t.insert(END, root.camera_t.get(i) + ': setting failed\n','err')
	root.hist_t.yview(END) #autoscroll to bottom
	root.hist_t.config(state='disabled')
def add_camera(root):
	for i in range(len(root.frame_elements)):
		root.frame_elements[i].place_forget()
	root.frame_elements = []
	
	root.camera_t.place_forget()
	root.position_t.place_forget
	root.set_b.place_forget()
	root.test_b.place_forget()
	root.up_b.place_forget()
	root.down_b.place_forget()
	root.del_b.place_forget()
	root.scrollbar.place_forget()
	root.ip_lab.place(relx=.515, rely=.17, relwidth=.2, relheight=.04)
	root.ip_entry.place(relx=.725, rely=.17, relwidth=.255, relheight=.04)

	root.pos_lab.place(relx=.515, rely=.22, relwidth=.2, relheight=.04)
	root.pos_entry.place(relx=.725, rely=.22, relwidth=.255, relheight=.04)
	
	root.add_b.place(relx=.93, rely=.36, relwidth=.05, relheight=.03)
	root.cams_b.place(relx=.515, rely=.36, relwidth=.2, relheight=.03)
	root.cam_prog.place(relx=.725, rely=.36, relwidth=.195, relheight=.03)
	root.cam_prog['value'] = 0
	root.add_camera_b.place_forget()	
def get_add_camera(root):
	root.hist_t.config(state='normal')
	try:
		ip = root.ip_entry.get()
		pos = root.pos_entry.get()
		if ip not in root.serverMacAddress:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((ip, root.port))
			s.send(bytes('test', 'UTF-8'))
			s.close()
			root.serverMacAddress.append(ip)
			root.camera_t.insert(END,ip)
			root.position_t.insert(END,pos)
			root.lab.config(bg='grey')
			root.hist_t.insert(END, ip+ ': added\n')
	except:
		root.hist_t.insert(END, ip+': not available\n','err')
		root.lab.config(bg='red')
	root.ip_lab.place_forget()
	root.ip_entry.place_forget()
	root.pos_lab.place_forget()
	root.pos_entry.place_forget()
	root.ip_entry.delete(0,END)
	root.pos_entry.delete(0,END)
	root.add_b.place_forget()
	root.add_camera_b.place(relx=.93, rely=.12, relwidth=.05, relheight=.04)
	root.cams_b.place_forget()
	root.cam_prog.place_forget()
	
	root.camera_t.place(relx=.515, rely=.17, relwidth=.22, relheight=.185)
	root.position_t.place(relx=.735, rely=.17, relwidth=.225, relheight=.185)
	root.scrollbar.place(relx=.97, rely=.17, relwidth=.01, relheight=.185)
	root.set_b.place(relx=.515, rely=.36, relwidth=.089, relheight=.03)
	root.test_b.place(relx=.609, rely=.36, relwidth=.089, relheight=.03)
	root.up_b.place(relx=.703, rely=.36, relwidth=.089, relheight=.03)
	root.down_b.place(relx=.797, rely=.36, relwidth=.089, relheight=.03)
	root.del_b.place(relx=.891, rely=.36, relwidth=.089, relheight=.03)
	
	root.hist_t.yview(END) #autoscroll to bottom ############
	root.hist_t.config(state='disabled') 
	root.select_box['values'] = root.serverMacAddress 
def delete_camera(root):
	for i in range(len(root.frame_elements)):
		root.frame_elements[i].place_forget()
	root.frame_elements = []
	
	root.hist_t.config(state='normal')
	del_items = root.camera_t.curselection()
	for i in del_items[::-1]:
		ip=root.camera_t.get(i)
		root.camera_t.delete(i)
		root.position_t.delete(i)
		root.serverMacAddress = list(root.camera_t.get(0,END))
		root.hist_t.insert(END, ip+': deleted\n')
	root.hist_t.yview(END) #autoscroll to bottom
	root.hist_t.config(state='disabled')
def update(root):
	root.selected_cams = root.camera_t.get(root.camera_t.curselection())
	#hier auch nur selected cam
	root.hist_t.config(state='normal')
	for i in range(len(root.selected_cams)):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((root.selected_cams[i], root.port))
			path = askopenfilename()
			filename = path.split('/')[-1]
			bytelen = len(bytes('update,'+filename+',','UTF-8'))
			print(bytelen)
			w = open(path,'rb')
			dat = w.read(1024-bytelen)
			s.send(bytes('update,'+filename+',','UTF-8')+dat)
			dat = w.read(1024)
			while dat:
				s.send(dat)
				dat = w.read(1024)
			s.close()
		except:
			print('no camera connected')
			root.lab.config(bg='red')
	root.hist_t.config(state='disabled')
def get_vp(root,nr):
	#nur selected cam
    if nr == 1:
        root.hist_t.config(state='normal')
        root.up_b.place_forget()
        root.down_b.place_forget()
        root.download_t.place(relx=.515,rely=.7, relwidth=.48, relheight=.13)
        root.scrollbar_download.place(relx=.97,rely=.7, relwidth=.01, relheight=.13)
        root.back_download.place(relx=.515, rely =.65 , relwidth= .025, relheight=.04)
        print(root.select_var.get())
		#for i in range(len(root.serverMacAddress)):
        #    pass
        #noch auf erste stelle fokussieren
        #hier noch die Abfrage falls >= 1 vp dann zeige an ansonsten lass es
    elif nr ==0:
        root.up_b.place(relx=.515,rely=.7, relwidth=.2, relheight=.06)
        root.down_b.place(relx=.515,rely=.77, relwidth=.2, relheight=.06)
        root.download_t.place_forget()
        root.scrollbar_download.place_forget()
        root.back_download.place_forget()
def get_data(root,filename):
	root.hist_t.config(state='normal')
	ip = root.selected_cams
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((ip, root.port))
		s.send(bytes("get_data,"+filename, 'UTF-8'))
			
		with open(filename.split('/')[-1], 'wb') as file_to_write:
			while True:
				data = s.recv(1024)
				if not data:
					break
				file_to_write.write(data)
			file_to_write.close()
		s.close()
			
		print('closed')
		root.hist_t.insert(END, ip+': received file\n')
		root.hist_t.yview(END) #autoscroll to bottom			
		
	except:
		root.lab.config(bg='red')
	root.hist_t.config(state='disabled')
def get_testframe(root):
	for i in range(len(root.frame_elements)):
		root.frame_elements[i].place_forget()
	root.frame_elements = []
	
	root.frame_elements.append(Label(text='test frame',  bg='grey',font=root.buttonfont))
	root.frame_elements[-1].place(relx=.515, rely=.42, relwidth=.465, relheight=.04)
	
	root.frame_elements.append(Label(bg='white'))
	root.frame_elements[-1].place(relx=.515, rely=.47, relwidth=.465, relheight=.36)

	ip = root.camera_t.get(root.camera_t.curselection())
	try:
		filename = 'test.jpg' 
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((ip, root.port))
		s.send(bytes("get_testframe", 'UTF-8'))
			
		with open(filename, 'wb') as file_to_write:
			while True:
				data = s.recv(1024)
				if not data:
					break
				file_to_write.write(data)
			file_to_write.close()
		s.close()
			
	except:
		root.lab.config(bg='red')

	root.img = ImageTk.PhotoImage(file = 'test.jpg') 
	root.frame_elements[-1].config(image = root.img )
	root.update()	
def remove_file(root,folder, filename):
	#nur selected cam
	root.hist_t.config(state='normal')
	for i in range(len(root.serverMacAddress)):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((root.serverMacAddress[i], root.port))
			s.send(bytes("remove,"+filename, 'UTF-8'))
			s.close()
			print('closed')
			root.hist_t.insert(END, root.serverMacAddress[i]+': removed file'+filename+'\n')
			root.hist_t.yview(END) #autoscroll to bottom
			
		except:
			root.lab.config(bg='red')
	get_filenames(root,folder)
def off(root):
	root.hist_t.config(state='normal')
	for i in range(len(root.serverMacAddress)):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((root.serverMacAddress[i], root.port))
			s.send(bytes('off','UTF-8'))
			s.close()
			root.lab.config(bg='grey')
			root.hist_t.insert(END, root.serverMacAddress[i]+': off\n')
			root.camera_t.delete(0,END)
			root.serverMacAddress = root.camera_t.get(0,END)
		except:
			print('no camera connected')
			root.lab.config(bg='red')
	root.hist_t.yview(END) #autoscroll to bottom
	root.hist_t.config(state='disabled')
def onselect():
	sel_cams = root.camera_t.curselection()
	n_sel = len(sel_cams)
	if n_sel == 0:
		root.set_b.config(state = DISABLED)
		root.test_b.config(state = DISABLED) 
		root.up_b.config(state = DISABLED)
		root.down_b.config(state = DISABLED)
		root.del_b.config(state = DISABLED)
	elif n_sel == 1:
		root.set_b.config(state = 'normal')
		root.test_b.config(state = 'normal') 
		root.up_b.config(state = 'normal')
		root.down_b.config(state = 'normal')
		root.del_b.config(state = 'normal')
	elif n_sel > 1:
		root.set_b.config(state = 'normal')
		root.test_b.config(state = DISABLED) 
		root.up_b.config(state = DISABLED)
		root.down_b.config(state = DISABLED)
		root.del_b.config(state = 'normal')
def init_files(root):
	root.selected_cams = root.camera_t.get(root.camera_t.curselection())
	print(root.selected_cams)
	for i in range(len(root.frame_elements)):
		root.frame_elements[i].place_forget()
	root.frame_elements = []
	
	root.frame_elements.append(Label(text='files',  bg='grey',font=root.buttonfont))
	root.frame_elements[-1].place(relx=.515, rely=.42, relwidth=.465, relheight=.04)
	
	root.frame_elements.append(Button(text='videos', command=lambda: get_filenames(root,'videos'), bg='grey',font=root.buttonfont,relief = 'flat'))
	root.frame_elements[-1].place(relx=.515, rely=.47, relwidth=.1516, relheight=.04)
	root.frame_elements.append(Button(text='logfiles', command=lambda: get_filenames(root,'logfiles'), bg='grey',font=root.buttonfont,relief = 'flat'))
	root.frame_elements[-1].place(relx=.6716, rely=.47, relwidth=.1516, relheight=.04)
	root.frame_elements.append(Button(text='photos', command=lambda: get_filenames(root,'pictures'), bg='grey',font=root.buttonfont,relief = 'flat'))
	root.frame_elements[-1].place(relx=.8284, rely=.47, relwidth=.1516, relheight=.04)
	
	root.frame_elements.append(Listbox(selectmode=SINGLE, font = root.infofont, bg='lightgrey', relief = 'flat', highlightthickness = 0))
	root.frame_elements[-1].place(relx=.51, rely=.52, relwidth=.465, relheight=.26)
	root.frame_elements.append(Scrollbar(orient="vertical",command=root.camera_t.yview))
	root.frame_elements[-1].place(relx=.97, rely=.52, relwidth=.01, relheight=.26)
	root.frame_elements[-2].config(yscrollcommand=root.frame_elements[-1].set)
		
	root.frame_elements.append(Button(text='select', bg='grey',font=root.buttonfont,state = DISABLED))
	root.frame_elements[-1].place(relx=.905, rely=.79, relwidth=.075, relheight=.04)
	
	root.frame_elements.append(Button(text='delete', bg='grey',font=root.buttonfont,state = DISABLED))
	root.frame_elements[-1].place(relx=.825, rely=.79, relwidth=.075, relheight=.04)
def get_filenames(root,folder):
	ip = root.selected_cams
	print(ip)
	root.hist_t.config(state='normal')
	
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((ip, root.port))
		s.send(bytes('get_files,'+folder, 'UTF-8'))
		
		data = s.recv(1024)
		data = data.decode('utf-8').split(',')
		s.close()
		
		root.frame_elements[4].delete(0,END)
		for i in data:
			root.frame_elements[4].insert(END,i)
		
		root.frame_elements[-1].config(state = 'normal', command = lambda: remove_file(root,folder,folder +'/'+root.frame_elements[4].get(root.frame_elements[4].curselection())))
		root.frame_elements[-2].config(state = 'normal', command = lambda: get_data(root,folder +'/'+root.frame_elements[4].get(root.frame_elements[4].curselection())))
		
		root.hist_t.insert(END, ip +': '+'recieved filenames \n')
		root.hist_t.yview(END) #autoscroll to bottom
			
	except:
		root.lab.config(bg='red')
	root.hist_t.config(state='disabled')
	

root = Tk()
root.recvalue = 0
root.serverMacAddress = []
root.port = 8888

#fonts
fac = get_min(root) # adjusts the fontsize depending on screen size
root.titlefont = Font(family="Helvetica", size=int(30*fac))
root.infofont = Font(family="Helvetica", size=int(20*fac))
root.buttonfont=Font(family="Helvetica", size=int(25*fac))
root.scalefont = Font(family="Helvetica", size=int(15*fac))

#attributes
root.attributes('-fullscreen',True)

#bindings
root.bind('<Escape>', lambda event: root.quit())


#header 
root.lab = Label(text='GooseCam', bg='grey' , font = root.titlefont)
root.lab.place(relx=.01, rely=.01, relwidth=.98, relheight=.09)

#actions
root.frame =Frame(bg='lightgrey')
root.frame.place(relx=.01, rely=.11, relwidth=.485, relheight=.42)
root.action_lab=Label(text='actions',  bg='grey',font=root.buttonfont)
root.action_lab.place(relx=.02, rely=.12, relwidth=.465, relheight=.04)
root.light_b=Button(text='light on', command=lambda:light(root,1), bg='grey',font=root.buttonfont)
root.light_b.place(relx=.02, rely=.18, relwidth=.2, relheight=.06)
root.p=Button(text='photo', command=lambda:photo(root, root.text_tp.get()),bg='grey',font=root.buttonfont)
root.p.place(relx=.02, rely=.25, relwidth=.2, relheight=.06)
root.text_tp=Entry(font=root.buttonfont)
root.text_tp.place(relx=.23, rely=.25, relwidth=.255, relheight=.06)
root.video_b=Button(text='start video', command=lambda:start_video(root,root.text_tv.get()),bg='grey',font=root.buttonfont)
root.video_b.place(relx=.02, rely=.32, relwidth=.2, relheight=.06)
root.text_tv=Entry(font=root.buttonfont)
root.text_tv.place(relx=.23, rely=.32, relwidth=.255, relheight=.06)
root.time_lab = Label(text='',bg='lightgrey',font=root.buttonfont)
root.text_b=Button(text='annotate text', command=lambda:annotate_text(root, root.text_e.get()), bg='grey',font=root.buttonfont)
root.text_b.place(relx=.02, rely=.39, relwidth=.2, relheight=.06)
root.text_e=Entry(font=root.buttonfont, state = 'disabled')
root.text_e.place(relx=.23, rely=.39, relwidth=.255, relheight=.06)
root.status_lab = Label(text='status LEDs',bg='grey',font=root.buttonfont)
root.status_lab.place(relx=.02, rely=.46, relwidth=.2, relheight=.06)
root.stat_var=IntVar()
root.status_check= Checkbutton(text = 'on', bg='lightgrey', relief='flat', variable =root.stat_var, font=root.buttonfont, command= lambda:status(root))
root.status_check.place(relx=.23, rely=.46, relwidth=.255, relheight=.06)


#cameras
root.frame2 =Frame(bg='lightgrey')
root.frame2.place(relx=.505, rely=.11, relwidth=.485, relheight=.29)
root.camera_lab=Label(text='cameras',  bg='grey',font=root.buttonfont)
root.camera_lab.place(relx=.515, rely=.12, relwidth=.465, relheight=.04)
root.add_camera_b = Button(text='+', command=lambda:add_camera(root), bg='grey',font=root.buttonfont, relief ='flat')
root.add_camera_b.place(relx=.93, rely=.12, relwidth=.05, relheight=.04)
root.camera_t = Listbox(selectmode=MULTIPLE, font = root.infofont, bg='lightgrey', relief = 'flat', highlightthickness = 0)
root.camera_t.place(relx=.515, rely=.17, relwidth=.22, relheight=.185)
root.camera_t.bind('<<ListboxSelect>>', lambda event:onselect())
root.position_t = Listbox(selectmode=SINGLE, font = root.infofont, bg='lightgrey', relief = 'flat', highlightthickness = 0)
root.position_t.place(relx=.735, rely=.17, relwidth=.225, relheight=.185)
root.scrollbar = Scrollbar(orient="vertical",command=root.camera_t.yview)
root.camera_t.config(yscrollcommand=root.scrollbar.set)
root.position_t.config(yscrollcommand=root.scrollbar.set)
root.scrollbar.place(relx=.97, rely=.17, relwidth=.01, relheight=.185)

root.set_b = Button(text='set', command=lambda:init_set(root), bg='grey',font=root.buttonfont, relief ='flat', state = DISABLED)
root.set_b.place(relx=.515, rely=.36, relwidth=.089, relheight=.03)

root.test_b = Button(text='test', command=lambda:get_testframe(root), bg='grey',font=root.buttonfont, relief ='flat', state = DISABLED)
root.test_b.place(relx=.609, rely=.36, relwidth=.089, relheight=.03)

root.up_b = Button(text='upload', command=lambda:update(root), bg='grey',font=root.buttonfont, relief ='flat', state = DISABLED)
root.up_b.place(relx=.703, rely=.36, relwidth=.089, relheight=.03)

root.down_b = Button(text='files', command=lambda:init_files(root), bg='grey',font=root.buttonfont, relief ='flat', state = DISABLED)
root.down_b.place(relx=.797, rely=.36, relwidth=.089, relheight=.03)

root.del_b = Button(text='delete', command=lambda:delete_camera(root), bg='grey',font=root.buttonfont, relief ='flat', state = DISABLED)
root.del_b.place(relx=.891, rely=.36, relwidth=.089, relheight=.03)


root.bind('<Delete>', lambda event: delete_camera(root)) 
root.ip_lab=Label(text='IP-adress',  bg='lightgrey',font=root.buttonfont)
root.ip_entry=Entry(font=root.buttonfont)
root.pos_lab=Label(text='position',  bg='lightgrey',font=root.buttonfont)
root.pos_entry=Entry(font=root.buttonfont)

root.add_b=Button(text='add', command=lambda:get_add_camera(root), bg='grey',font=root.buttonfont)
root.off_b = Button(text='off', command=lambda: off(root), font = root.buttonfont, bg='grey', relief = 'flat')
root.off_b.place(relx=.94,rely=.01, relwidth=.05, relheight=.09)
root.cams_b=Button(text='add available', command=lambda: get_goosecams(root,10,0), font = root.buttonfont, bg='grey')
root.cam_prog = ttk.Progressbar(orient = 'horizontal', length = 200, mode = 'determinate')
root.cam_prog['value'] = 2 ###################################################################
root.cam_prog['maximum'] = 10


#variable frame
root.frame_elements =[]
root.frame3 =Frame(bg='lightgrey')
root.frame3.place(relx=.505, rely=.41, relwidth=.485, relheight=.43)


#shortcuts
root.frame4 =Frame(bg='lightgrey')
root.frame4.place(relx=.505, rely=.85, relwidth=.485, relheight=.14)  
root.shortcut_lab=Label(text='shortcuts',  bg='grey',font=root.buttonfont)
root.shortcut_lab.place(relx=.515, rely=.86, relwidth=.465, relheight=.04)
root.instruction_text=Text(bg='lightgrey', font=root.infofont, relief = 'flat')
root.instruction_text.insert(END,' g: annotate goosebump\nesc: quit')
root.instruction_text.config(state='disabled')
root.instruction_text.place(relx=.515, rely=.91, relwidth=.465, relheight=.08)
'''


#file_transfer
root.frame4 =Frame(bg='lightgrey')
root.frame4.place(relx=.505, rely=.64, relwidth=.485, relheight=.2)  
root.filelab = Label(text='file transfer',  bg='grey',font=root.buttonfont)
root.filelab.place(relx=.515, rely =.65 , relwidth= .465, relheight=.04)
root.select_list=['None']
root.select_var = StringVar()
root.select_box = ttk.Combobox(root, textvariable = root.select_var, values = root.serverMacAddress)
root.select_box.place(relx=.865, rely =.655 , relwidth= .1, relheight=.03)
root.up_b=Button(text='Upload', command=lambda: update(root), font = root.buttonfont, bg='grey', state ='normal')
root.up_b.place(relx=.515,rely=.7, relwidth=.2, relheight=.06)
root.down_b=Button(text='Download', command=lambda: get_vp(root,1), state = 'normal', font = root.buttonfont, bg='grey')
root.down_b.place(relx=.515,rely=.77, relwidth=.2, relheight=.06)
'''

#history
root.frame5 =Frame(bg='lightgrey')
root.frame5.place(relx=.01, rely=.54, relwidth=.485, relheight=.45)
root.history_lab=Label(text='history',  bg='grey',font=root.buttonfont)
root.history_lab.place(relx=.02, rely=.55, relwidth=.465, relheight=.04)
root.hist_t=ScrolledText.ScrolledText(bg='white', state='disabled', relief='flat', font=root.infofont)
root.hist_t.place(relx=.02, rely=.6, relwidth=.465, relheight=.38)
root.hist_t.tag_add('err', END)
root.hist_t.tag_configure('err', foreground = 'red')


'''
#download
root.download_t = Listbox(selectmode=MULTIPLE, font = root.infofont, bg='lightgrey', relief = 'flat', highlightthickness = 0)
root.scrollbar_download = Scrollbar(orient="vertical",command=root.camera_t.yview)
root.download_t.config(yscrollcommand=root.scrollbar.set)
root.back_download = Button(text='<', command=lambda: get_vp(root,0), font = root.buttonfont, bg='grey', state ='normal', relief = 'flat')
root.back_download.place()
'''

root.mainloop()







