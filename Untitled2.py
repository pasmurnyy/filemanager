#!/usr/bin/env python
# coding: utf-8

# In[2]:


import tkinter
import os
import subprocess
from tkinter import messagebox
from tkinter import simpledialog

class MainContextMenu(tkinter.Menu):
	''' Context menu for the internal directory area'''
	def __init__(self, main_window, parent):
		super(MainContextMenu, self).__init__(parent, tearoff = 0)
		self.main_window = main_window
		self.add_command(label="Создать директорию", command = self.create_folder)
		self.add_command(label="Создать файл", command = self.create_file)

	def popup_menu(self, event):
		''' function for activating the context menu'''
		if self.main_window.file_context_menu:
			self.main_window.file_context_menu.unpost()
		if self.main_window.folder_context_menu:
			self.main_window.folder_context_menu.unpost()
		self.post(event.x_root, event.y_root)

	def create_folder(self):
		''' function for creating a new directory in the current one'''
		folder_name = simpledialog.askstring("Новая директория", "Введите название новой директории")
		if folder_name:
			command = "mkdir {0}".format(folder_name).split(' ')
			process = subprocess.Popen(command, cwd=self.main_window.path_text.get(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			out, err = process.communicate()
			if err:
				messagebox.showwarning("Ошибка")
			self.main_window.refresh_window()


	def create_file(self):
		''' function for creating a new file in the current directory'''
		folder_name = simpledialog.askstring("Новый файл", "Введите название нового файла")
		if folder_name:
			command = "touch {0}".format(folder_name).split(' ')
			process = subprocess.Popen(command, cwd=self.main_window.path_text.get(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			out, err = process.communicate()
			if err:
				messagebox.showwarning("Ошибка")
			self.main_window.refresh_window()



	def insert_to_folder(self):
		''' function for copying a file or directory to the current directory'''
		copy_obj = self.main_window.buff
		to_dir = self.main_window.path_text.get()
		if os.path.isdir(self.main_window.buff):
			process = subprocess.Popen(['cp', '-r', copy_obj, to_dir], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			out, err = process.communicate()
			if err:
				messagebox.showwarning("Ошибка", err.decode("utf-8"))
		else:
			process = subprocess.Popen(['cp', '-n', copy_obj, to_dir], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			out, err = process.communicate()
			if err:
				messagebox.showwarning("Операция невозможна!",err.decode("utf-8"))
		self.main_window.refresh_window()
        
        
class FileContextMenu(tkinter.Menu):
	def __init__(self, main_window, parent):
		super(FileContextMenu, self).__init__(parent, tearoff = 0)
		self.main_window = main_window
		self.add_command(label="Открыть файл", command = self.open_file)
		self.add_separator()
		self.add_command(label="Копировать", command = self.copy_file)
		self.add_command(label="Переименовать", command = self.rename_file)
		self.add_separator()
		self.add_command(label="Удалить", command = self.delete_file)


	def open_file(self):
		'''function for opening a file by another  programs'''
		ext = self.main_window.take_extention_file(self.main_window.selected_file)
		full_path = self.main_window.path_text.get() + self.main_window.selected_file

		if ext in ['txt', 'py', 'html', 'css', 'js']:
			if 'mousepad' in self.main_window.all_program:
				subprocess.Popen(["mousepad", full_path], start_new_session = True)
			else:
				self.problem_message()
		elif ext == 'pdf':
			if 'evince' in self.main_window.all_program:
				subprocess.run(["evince", full_path], start_new_session = True)
			else:
				self.problem_message()
		elif ext in ['png', 'jpeg', 'jpg', 'gif']:
			if 'ristretto' in self.main_window.all_program:
				subprocess.run(["ristretto", full_path], start_new_session = True)
			else:
				self.problem_message()
		else:
			self.problem_message()

	def problem_message(self):
		messagebox.showwarning("Ошибка")

	def copy_file(self):
		''' function for copying a file'''
		self.main_window.buff = self.main_window.path_text.get() + self.main_window.selected_file
		self.main_window.refresh_window()


	def delete_file(self):
		'''function to delete the selected file'''
		full_path = self.main_window.path_text.get() + self.main_window.selected_file
		process = subprocess.Popen(['rm', full_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		output, err = process.communicate()
		if err:
			messagebox.showwarning("Ошибка")
		self.main_window.refresh_window()

	def rename_file(self):
		''' function for renaming the selected file'''
		new_name = simpledialog.askstring("Переименование файла", "Введите новое название файла")
		if new_name:
			old_file = self.main_window.path_text.get() + self.main_window.selected_file
			new_file = self.main_window.path_text.get() + new_name
			process = subprocess.Popen(['mv', old_file, new_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, err = process.communicate()
			if err:
				messagebox.showwarning("Ошибка")
			self.main_window.refresh_window()

	def popup_menu(self, event):
		''' function for activating the context menu'''
		self.post(event.x_root, event.y_root)
		if self.main_window.main_context_menu:
			self.main_window.main_context_menu.unpost()
		if self.main_window.dir_context_menu:
			self.main_window.dir_context_menu.unpost()
		self.main_window.selected_file = event.widget["text"]
        
class FolderContextMenu(tkinter.Menu):
	def __init__(self, main_window, parent):
		super(FolderContextMenu, self).__init__(parent, tearoff = 0)
		self.main_window = main_window
		self.add_command(label="Переименовать", command = self.rename_folder)
		self.add_command(label="Копировать", command = self.copy_folder)
		self.add_separator()
		self.add_command(label="Удалить", command = self.delete_folder)

	def copy_folder(self):
		''' function for copying a directory'''
		self.main_window.buff = self.main_window.path_text.get() + self.main_window.selected_file
		self.main_window.refresh_window()


	def delete_folder(self):
		''' function for deleting the selected directory'''
		full_path = self.main_window.path_text.get() + self.main_window.selected_file
		if os.path.isdir(full_path):
			process = subprocess.Popen(['rm', '-rf', full_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, err = process.communicate()
			if err:
				messagebox.showwarning("Ошибка")
		self.main_window.refresh_window()

	def rename_folder(self):
		'''function for renaming the selected directory'''
		new_name = simpledialog.askstring("Переименование директории", "Введите новое название директории")
		if new_name:
			old_dir = self.main_window.path_text.get() + self.main_window.selected_file
			new_dir = self.main_window.path_text.get() + new_name
			process = subprocess.Popen(['mv', old_dir, new_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, err = process.communicate()
			if err:
				messagebox.showwarning("Ошибка")
			self.main_window.refresh_window()

	def popup_menu(self, event):
		''' function for activating the context menu'''
		self.post(event.x_root, event.y_root)
		if self.main_window.main_context_menu:
			self.main_window.main_context_menu.unpost()
		if self.main_window.file_context_menu:
			self.main_window.file_context_menu.unpost()
		self.main_window.selected_file = event.widget["text"]
        
class MainWindow():
	'''Main window class'''
	def __init__(self):
		self.root = tkinter.Tk()
		self.root.title("file manager")
		self.root.resizable(width = False, height = False)
		self.root.geometry('450x300')

		self.hidden_dir = tkinter.IntVar()
		self.buff = None
		self.all_program = os.listdir('C:/')

		self.root.bind('<Button-1>', self.root_click)
		self.root.bind('<FocusOut>', self.root_click)

		#top frame
		self.title_frame = tkinter.Frame(self.root)
		self.title_frame.pack(fill = 'both', expand = True)

		#back button
		self.back_button = tkinter.Button(self.title_frame, text = "..", command = self.parent_folder, width = 1, height = 1)
		self.back_button.pack(side = 'left')

		#path entry
		self.path_text = tkinter.StringVar()
		self.path_text.set('/')
		self.current_path = tkinter.Entry(self.title_frame, textvariable = self.path_text, width = 40, state='readonly')
		self.current_path.pack(side = 'left')


		#main frame
		self.main_frame = tkinter.Frame(self.root)
		self.main_frame.pack()

		# scroll bar
		self.scrollbar_vert = tkinter.Scrollbar(self.main_frame, orient="vertical")
		self.scrollbar_vert.pack(side = 'right', fill = 'y')

		self.scrollbar_hor = tkinter.Scrollbar(self.main_frame, orient="horizontal")
		self.scrollbar_hor.pack(side = 'bottom', fill = 'x')

		#canvas
		self.canvas = tkinter.Canvas(self.main_frame, borderwidth=0,  bg = 'white')
		self.inner_frame = tkinter.Frame(self.canvas,  bg = 'white')

		#scrollbar
		self.scrollbar_vert["command"] = self.canvas.yview
		self.scrollbar_hor["command"] = self.canvas.xview

		#canvas
		self.canvas.configure(yscrollcommand=self.scrollbar_vert.set, xscrollcommand = self.scrollbar_hor.set, width=400, heigh=250)

		self.canvas.pack(side='left', fill='both', expand=True)
		self.canvas.create_window((0,0), window=self.inner_frame, anchor="nw")


		self.folder_content()


	def root_click(self, event):
		''' function for handling the click event in root'''
		if self.file_context_menu:
			self.file_context_menu.unpost()
		if self.main_context_menu:
			self.main_context_menu.unpost()
		if self.folder_context_menu:
			self.folder_context_menu.unpost()

	def folder_content(self):
		''' function for determining the contents of the current directory'''
		folder_list = os.listdir(self.path_text.get())
		path = self.path_text.get()

		if not folder_list:
			self.main_context_menu = MainContextMenu(self, self.canvas)
			self.canvas.bind('<Button-3>', self.main_context_menu.popup_menu)
			if self.buff:
				self.main_context_menu.add_command(label="Вставить", command = self.main_context_menu.insert_to_folder)
			self.inner_frame.bind('<Button-3>', self.main_context_menu.popup_menu)
			self.file_context_menu = None
			self.folder_context_menu = None
			return None

		
		self.main_context_menu = MainContextMenu(self, self.canvas)
		self.canvas.bind('<Button-3>', self.main_context_menu.popup_menu)
		if self.buff:
			self.main_context_menu.add_command(label="Вставить", command = self.main_context_menu.insert_to_folder)
		
		self.file_context_menu = FileContextMenu(self, self.inner_frame)
		self.folder_context_menu = FolderContextMenu(self, self.inner_frame)


		i = 0
		for item in folder_list:

			if os.path.isdir(str(path) + item):
				if os.access(str(path) + item, os.R_OK):
					

						folder_name = tkinter.Label(self.inner_frame, text=item,  bg = 'white', cursor = 'hand1')
						folder_name.bind("<Button-1>", self.move_to_folder)
						folder_name.bind("<Button-3>", self.folder_context_menu.popup_menu)
						folder_name.grid(row=i+1, column=1, sticky='w')
				else:
					if (not self.hidden_dir.get() and not item.startswith('.')) or self.hidden_dir.get():
						
						folder_name = tkinter.Label(self.inner_frame, text=item,  bg = 'white')
						folder_name.bind("<Button-1>", self.move_to_dir)
						folder_name.grid(row=i+1, column=1, sticky='w')

			
			i += 1
		self.inner_frame.update()
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))

	def move_to_folder(self, event):
		''' function for going to the selected directory'''
		elem = event.widget
		fold_name = elem["text"]
		fold_path = self.path_text.get() + fold_name
		if os.path.isdir(fold_path) and os.access(fold_path, os.R_OK):
			old_path = self.path_text.get()
			self.path_text.set(old_path + fold_name + '/')
			self.root_click('<Button-1>')
			self.refresh_window()


	def parent_folder(self):
		'''function for moving to the parent directory'''
		old_path = [i for i in self.path_text.get().split('/') if i]
		new_path = '/'+'/'.join(old_path[:-1])
		if not new_path:
			new_path = '/'
		if os.path.isdir(new_path):
			if new_path == '/':
				self.path_text.set(new_path)

			else:
				self.path_text.set(new_path + '/')
			self.refresh_window()


	def take_extention_file(self, file_name):
		''' function for getting the file extension'''
		ls = file_name.split('.')
		if len(ls)>1:
			return ls[-1]
		else:
			return None

	def refresh_window(self):
		''' function for updating the current directory'''
		for widget in self.inner_frame.winfo_children():
				widget.destroy()
		self.folder_content()
		self.canvas.yview_moveto(0)
        
win = MainWindow()
win.root.mainloop()


# In[ ]:




