import csv
import os
import time
import psutil

def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

def mem_monitor(func):
    def wrapper(*args, **kwargs):
 
        mem_before = process_memory()
        result = func(*args, **kwargs)
        mem_after = process_memory()
        print("\n{}:consumed memory (Process): {}MB... Total memory (usage): {}KB".format(func.__name__, mem_after / (1024 * 1024),(mem_after - mem_before) / (1024)))
 
        return result
    return wrapper

class Translate:
	def __init__(self, book_path, csv_path):
		self.book_path = book_path
		self.csv_path = csv_path
		self.txt_data = self.load_txt()
		self.csv_data = self.load_csv()

	def load_txt(self):
		f = open(self.book_path, 'r')
		return f.read()

	def load_csv(self):
		return dict(csv.reader(open(self.csv_path)))

	@mem_monitor
	def word_cnt(self):
		words = set({})
		count = {}
		max_print = 0
		txt_data = self.txt_data.lower()
		for k in self.csv_data:
			max_print += 1
			if max_print < 100:
				print('#', end="")
			if k in txt_data:
				count[k] = txt_data.count(k)
				words.add(k)
		else:
			max_print = 0
			print("Total unique replaced word count: {}".format(len(words)))
		choice = input('Bigger output... Are you want to print anyway? (Y/N):')
		if choice.lower() == 'y':
			for d in count:
				print("{}={}".format(d,count[d]))
		return

	def translate(self):
		start = time.time()
		txt_data = self.txt_data
		txt_lower = txt_data.lower()
		max_print = 0
		for mat, repl in self.csv_data.items():
			if mat in txt_lower:
				max_print += 1
				if max_print < 100:
					print('#', end="")
				txt_data = txt_data.replace(mat, repl)
				txt_data = txt_data.replace(mat.capitalize(), repl)
				txt_data = txt_data.replace(mat.lower(), repl)
				txt_data = txt_data.replace(mat.upper(), repl)
		else:
			max_print = 0
		end = time.time()
		self.time_taken = end - start
		return txt_data

	@mem_monitor	
	def generate_doc(self):
		out = os.path.join(os.path.dirname(self.book_path), 'E:\\python samples\\py\\t8.shakespeare.txt')
		with open(out, 'w') as f:
			f.write(self.translate())
		return ("Translation Completed in {} seconds... \
		\nFind your file in this path - {}".format(self.time_taken,out))

	def what_to_do(self):
		print("Welcome to Translate Service".center(100, '*'))
		choice = input("""
			Enter your choice: 
				1. Replaced Unique Words Count
				2. Translate Document ({})
			1 or 2:""".format(self.book_path))
		if choice not in ['1', '2']:
			print('Invalid Choice!')
			sel_opt = input('Are you want to Repeat? (Y/N):')
			if sel_opt.lower() == 'y':
				self.what_to_do()
			return
		else:
			choice = int(choice)
		return (self.word_cnt() if choice == 1 else self.generate_doc())

cls = Translate('E:\\python samples\\py\\t8.shakespeare.txt','E:\\python samples\\py\\french_dictionary.csv')
print(cls.what_to_do())


"""
# to run script,
python module.py
"""
