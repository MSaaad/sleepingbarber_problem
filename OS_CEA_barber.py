import threading
import time
import random
import queue 

barber = 1 
customers = int(input("Enter the number of customers for a day : "))  #user input customers
seats = int(input("Enter the number of seats available for sitting : "))  #user input seating options
customer_arrival_wait = 2    #time for next customer

print('**************************************************')
print('               BARBER SHOP IS OPENING               ')
print('**************************************************')

print('**************************************************')
print('              CUSTOMER STARTS ARRIVING              ')
print('**************************************************')

def arrival_wait():
	time.sleep(customer_arrival_wait * random.random())   #time for next customer * rand function to disturb the arrival timings.

class Barber(threading.Thread):
	condition = threading.Condition() # barber either sleeping aur wake up
	should_stop = threading.Event() # waiting room empty, every customer is served

	def __init__(self, ID):
		super().__init__()
		self.ID = barber

	def run(self):
		while True:
			try:	
				current_customer = wait_room.get(block=False) #thread won't wait/block in queue
			except queue.Empty: 	#actives when waiting room = 0
				if self.should_stop.is_set(): 	#when customer count gets 0
					return

				print(f"No customers in the waiting area, barber is sleeping :)") 
				with self.condition:
					self.condition.wait() 	#sleep/wait for customer to wake up
					print(f"Customer wakes up barber") 
			else:
				current_customer.cutHair(self.ID) # customer getting hair cut

class Customer(threading.Thread):
	time_duration_haircut = 6 	#time for one haircut

	def __init__(self, ID):
		super().__init__()
		self.ID = ID + 1

	def getHairCut(self): 
		time.sleep(self.time_duration_haircut * random.random())

	def cutHair(self, barber_ID):  #called from barber thread
		print(f"Customer {self.ID}'s turn arrives, jumps towards barber's room and sits on the barber chair '")
		print(f"Barber started cutting hair of customer {self.ID}")
		self.getHairCut() 
		print(f"Barber finished cutting hair of customer {self.ID}")
		self.serviced.set() 	#customer leaves after getting serviced
	
	def run(self):
		self.serviced = threading.Event()

		try:	#checking space in wait room
			wait_room.put(self, block=False)
		except queue.Full: 	#wait room is full, leave
			print(f"Waiting room is full, {self.ID} is leaving")
			return

		print(f"Customer {self.ID} arrived, sitting in the waiting room")
		with Barber.condition:
			Barber.condition.notify() # barber waking up if sleeping

		self.serviced.wait() 	#waiting for haircut

if __name__ == "__main__":
	
	global locks
	locks = threading.Lock()    #initiating lock in threads	
	total_customers = []          #list of total customers
	wait_room = queue.Queue(seats) 	#number of seats

	barber_thread = Barber(1)   #barber thread
	barber_thread.start()

	for order in range(customers): #customer thread
		arrival_wait()
		customer = Customer(order)
		locks.acquire()
		total_customers.append(customer)
		locks.release()
		customer.start()

	for customer in total_customers:
		customer.join()  # waiting for all customers to leave

	time.sleep(1) #time to clean the shop before closing
	Barber.should_stop.set() 	#tough day is finised for the barber :)	

print('*****************************************************')
print('                BARBER SHOP IS CLOSED                ')
print('*****************************************************')