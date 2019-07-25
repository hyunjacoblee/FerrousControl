import serial
import time
import array
from random import randint

PACKET_SIZE = 64

def main():
	s = serial.Serial('/dev/cu.usbmodem5803660', 1000000)
	count = 0
	
	while True:
		start_time = time.time()
		nums = []
		for i in range(PACKET_SIZE):
			nums.append(randint(0,200))
		# print(nums)
		
		#nums.append(count) #special last byte
		count += 1
		count = count % 255
		#nums[0] = 255
		nums[-1] = count

		s.write(array.array('B', nums))

		print("Sent bytes: " + str(nums) + '\n\n')

		#teensyBytes = s.read(PACKET_SIZE)
		#converted = array.array('B', teensyBytes)
		

		teensyBytes = []

		recv = s.read(1)
		while (recv != b'$'):
			if recv != b'\n' and recv != b'\r':
				teensyBytes.append(ord(recv))
			recv = s.read(1)

		print("Teensy bytes: " + repr(teensyBytes) + '\n\n')

		print("SUM: " + str(sum(nums) % 65535) + '\n\n')

		print((time.time() - start_time) * 1000)
		#time.sleep(0.5)



if __name__ == "__main__":
	main()