import random as rand
import abc

class LinkedList : 
	# Initializes an empty linked list.
	def __init__(self):
		self.list = []  # beginning of linked list

	# Returns the number of items in this linked list.
	def size(self):
		return len(self.list)

	# Returns true if this linked list is empty.
	def isEmpty(self):
		return self.size() == 0
	
	# Returns the first item added to this linked list 
	def check(self):
		if self.isEmpty():
			raise ValueError("linked list underflow: ")
		return self.list[0]
	
	#Removes and returns the first item in the linked list
	def peek(self):
		if self.isEmpty():
			raise ValueError("linked list underflow")

		return self.list.pop(0)

	def append(self, item):
		self.list.append(item)

	def prepend(self, item):
		self.list.insert(0, item)

	def accept(self, visitor):
		visitor.visit(self)

class Queue(LinkedList): 

	# Initializes an empty queue.
	def __init__(self, max_size,  *args, **kwargs):
		self.max_size = max_size
		super(Queue, self).__init__(*args, **kwargs)

	def isFull(self):
		return self.size() == self.max_size

	# Adds the item to this queue.
	def enqueue(self, item):
		if self.isFull():
			raise ValueError("Queue overflow")
		self.append(item)

	#Removes and returns the item on this queue that was least recently added.
	def dequeue(self):
		try:
			return self.peek()
		except ValueError:
			raise ValueError("Queue underflow")

class Stack(LinkedList): 
	# Initializes an empty stack.
	def __init__(self, max_size, *args, **kwargs):
		self.max_size = max_size
		super(Stack, self).__init__(*args, **kwargs)

	# Returns true if this stack is full.
	def isFull(self):
		return self.size() == self.max_size

	# Adds the item to this stack.
	def push(self, item):
		if self.isFull():
			raise ValueError("Stack overflow")
		self.prepend(item)
	
	# Removes and returns the item most recently added to this stack.
	def pop(self):
		try:
			return self.peek()
		except ValueError:
			raise ValueError("Stack underflow")

class AutoAdaptiveStack(Stack): 

	def __init__(self, max_trials, size_increment, waitingQueueSize, *args, **kwargs):
		self.max_trials = max_trials
		self.size_increment = size_increment
		self.trials = 0
		self.waitingQueue = Queue(waitingQueueSize)
		super(AutoAdaptiveStack, self).__init__(*args, **kwargs)

	def push(self, item):
		try:
			super(AutoAdaptiveStack, self).push(item)
		except:

			try:
				self.waitingQueue.enqueue(item)
			except:
				print("There is no free space actually :( try later")

			self.trials += 1
			if self.trials == self.max_trials:
				self.max_size += self.size_increment
				self.trials = 0

				while not self.isFull() and not self.waitingQueue.isEmpty():
					self.push(self.waitingQueue.dequeue())

	#redefinition de pop
	def pop(self):
		elem = super(AutoAdaptiveStack, self).pop()

		if not self.waitingQueue.isEmpty():
			self.push(self.waitingQueue.dequeue())

		return elem
	
class AutoAdaptiveQueue(Queue): 

	def __init__(self, max_trials, size_increment, waitingQueueSize, *args, **kwargs):
		self.max_trials = max_trials
		self.size_increment = size_increment
		self.trials = 0
		self.waitingQueue = Queue(waitingQueueSize)
		super(AutoAdaptiveQueue, self).__init__(*args, **kwargs)

	def enqueue(self, item):
		try:
			super(AutoAdaptiveQueue, self).enqueue(item)
		except ValueError:
			
			try:
				self.waitingQueue.enqueue(item)
			except:
				print("There is no free space actually :( try later")
			
			self.trials += 1
			if self.trials == self.max_trials:
				self.max_size += self.size_increment
				self.trials = 0

				while not self.isFull() and not self.waitingQueue.isEmpty():
					self.enqueue(self.waitingQueue.dequeue())

	#redefinition de dequeue
	def dequeue(self):
		ret = super(AutoAdaptiveQueue, self).dequeue()
		
		if not self.waitingQueue.isEmpty():
			self.enqueue(self.waitingQueue.dequeue())

		return ret
		
class Printer(object, metaclass=abc.ABCMeta):
	def __init__(self, name):
		self.name = name

	def visit(self, list_obj):
		if isinstance(list_obj, Stack):
			display_message = "\n-------\n"
			for elem in list_obj.list:
				display_message += '   '+str(elem)+'   '
				display_message += "\n-------\n"
		elif isinstance(list_obj, Queue):
			display_message = "\n|"
			for elem in list_obj.list:
				display_message += str(elem) + "|"
			display_message += "\n"
		else:
			display_message = "\n("
			for elem in list_obj.list:
				display_message += str(elem)
				if elem != list_obj.list[len(list_obj.list)-1]:
					display_message += ","
			display_message += ")\n"
		self.log(display_message)
	
	@abc.abstractmethod
	def log(self, display_message):
		raise NotImplementedError('child objects must define log to create a printer')
		
class ScreenPrinter(Printer):
	def __init__(self, *args, **kwargs):
		super(ScreenPrinter, self).__init__(*args, **kwargs)

	def log(self, display_message):
		print(self.name)
		print(display_message)

class FilePrinter(Printer):
	def __init__(self, file_path, *args, **kwargs):
		self.file_path = file_path
		super(FilePrinter, self).__init__(*args, **kwargs)
	
	def log(self, display_message):
		with open(self.file_path, 'a') as f:
			f.write(self.name)
			f.write(display_message)

class Calculator:

	@staticmethod
	def union(first_list, second_list):
		if isinstance(first_list,Queue) and isinstance(second_list,Queue):

			merged_queue = Queue(max_size=first_list.max_size+second_list.max_size)
			for elem in first_list.list:
				merged_queue.enqueue(elem)

			for elem in second_list.list:
				merged_queue.enqueue(elem)

			return merged_queue

		elif isinstance(first_list,Stack) and isinstance(second_list,Stack):
			merged_stack = Stack(max_size=first_list.max_size+second_list.max_size)
			for elem in reversed(first_list.list):
				merged_stack.push(elem)

			for elem in reversed(second_list.list):
				merged_stack.push(elem)

			return merged_stack
		elif isinstance(first_list,LinkedList) and isinstance(second_list,LinkedList):
			
			list1 = first_list.list
			list2 = second_list.list

			first_list.list = first_list.list.copy()
			second_list.list = second_list.list.copy()
			
			merged_list = LinkedList()

			while not first_list.isEmpty() and not second_list.isEmpty():
				if(rand.uniform(0,1) < 0.5):
					merged_list.append(first_list.peek())
				else:
					merged_list.append(second_list.peek())

			while not first_list.isEmpty():
				merged_list.append(first_list.peek())

			while not second_list.isEmpty():
				merged_list.append(second_list.peek())

			first_list.list = list1
			second_list.list = list2

			return merged_list
		else:
			raise ValueError('The types of both lists are different')