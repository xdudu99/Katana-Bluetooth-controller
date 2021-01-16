import mido
import threading as th #I needed to learn how to thread to make switching banks and effects possible
from time import sleep
from mido.ports import MultiPort # Multiport is needed because of the 3 katana ports generated.
mido.get_input_names() # Shows the midi device names
mididev = mido.get_input_names() # Its necessary to create a variable for input names so the program can find them even if they change names. 
checkport = mido.get_input_names()
btmidi = mididev[0] # From observing mido.get_input_names() output, ive determined that my midi devices stay always in the same position, so mididev[0] always refer to the same device.
katana1 = mididev[1]
katana2 = mididev[2]
katana3 = mididev[3]
out1 = mido.open_output(katana1) # Creating the output ports because i dont know wich of the 3 is the one i need, so i send the message to all of them.
out2 = mido.open_output(katana2)
out3 = mido.open_output(katana3)
multi = MultiPort([out1, out2, out3])
outcheck = checkport[1]
outc = mido.open_input(outcheck)
ch1a = mido.Message('program_change', program=0) # Well, from sheer fcking luck the katana program change (pc) messages for channel switching are basic values.
ch2a = mido.Message('program_change', program=1)
ch1b = mido.Message('program_change', program=5)
ch2b = mido.Message('program_change', program=6)
chp = mido.Message('program_change', program=4)
input = mido.open_input(btmidi)
boostoff = mido.Message('control_change', control=16, value=0) #Figured it out how to send the messages for pretty much anything that i need. The thing i was missing was the "value" argument on CC messages. THANK BOSS FOR INFO ON THE MANUAL
booston = mido.Message('control_change', control=16, value=127)
delayoff = mido.Message('control_change', control=19, value=0)
delayon = mido.Message('control_change', control=19, value=127)
reverboff = mido.Message('control_change', control=20, value=0)
reverbon = mido.Message('control_change', control=20, value=127)
fxoff = mido.Message('control_change', control=18, value=0)
fxon = mido.Message('control_change', control=18, value=127)
modoff = mido.Message('control_change', control=17, value=0)
modon = mido.Message('control_change', control=17, value=127)
bank = 0 # Counter for "bank" of commands for switching between channels or effects (b1 or b2)




boostchk = mido.Message.from_hex('F0 41 00 00 00 00 33 11 60 00 00 10 00 00 00 02 0E F7')
modchk = mido.Message.from_hex('F0 41 00 00 00 00 33 11 60 00 01 00 00 00 00 02 1D F7')
delaychk =  mido.Message.from_hex('F0 41 00 00 00 00 33 11 60 00 05 00 00 00 00 02 19 F7')
reverbchk = mido.Message.from_hex('F0 41 00 00 00 00 33 11 60 00 05 40 00 00 00 02 59 F7')
fxchk = mido.Message.from_hex('F0 41 00 00 00 00 33 11 60 00 03 00 00 00 00 02 1B F7')


def effects_check():
	global modchkmsg, boostchkmsg, delaychkmsg, reverbchkmsg, fxchkmsg
	while True:
		sleep (0.3)
		multi.send(modchk)
		modchkmsg = outc.receive()
		multi.send(boostchk)
		boostchkmsg = outc.receive()
		multi.send(delaychk)
		delaychkmsg = outc.receive()
		multi.send(reverbchk)
		reverbchkmsg = outc.receive()
		multi.send(fxchk)
		fxchkmsg = outc.receive()
	



effectscheck_thread = th.Thread(target = effects_check, daemon = True)
effectscheck_thread.start()

print ('Start')
bank += 1


print ('Running main loop')

while True:
	
	msg = input.receive()
	sleep (0.1)
	# Bank 1
		#Channels 

	if msg.control == 64 and msg.value == 127 and bank == 1:  # Series of if commands that sends the channel switch message based on the btctl input.
		multi.send(ch1a)
		print ('Channel 1A')
		continue
	elif msg.control == 66 and msg.value == 127 and bank == 1:					
		multi.send(ch2a)
		print ('Channel 2A')
		continue
	elif msg.control == 65 and msg.value == 127 and bank == 1:
		multi.send(ch1b)
		print ('Channel 1B')
		continue
	elif msg.control == 67 and msg.value == 127 and bank == 1:
		multi.send(ch2b)
		print ('Channel 2B')
		continue
	elif msg.control == 68 and msg.value == 127 and bank == 1:
		multi.send(chp)
		print ('Channel Pannel')
		continue
		
	
	#Bank change
	
	elif msg.control == 69 and msg.value == 127 and bank == 1:
		bank += 1
		print ('Bank 2')
		continue

# Bank 2

	#Boost
		
	elif msg.control == 64 and msg.value == 127 and bank == 2:

		if boostchkmsg.data[11] == 0:
			multi.send(booston)
			print ('Boost On')
			continue
			
		elif boostchkmsg.data[11] == 1:
			multi.send(boostoff)
			print ('Boost Off')
			continue
		else:
			pass
	
	
	#Delay
	
	elif msg.control == 66 and msg.value == 127 and bank == 2:
		
		if delaychkmsg.data[11] == 0:
			multi.send(delayon)
			print ('Delay On')
			continue
			
		elif delaychkmsg.data[11] == 1:
			multi.send(delayoff)
			print ('Delay Off')
			continue
	
	#Reverb
	
	elif msg.control == 65 and msg.value == 127 and bank == 2:
	
		if reverbchkmsg.data[11] == 0:
			multi.send(reverbon)
			print ('Reverb On')
			continue
		
		elif reverbchkmsg.data[11] == 1:
			multi.send(reverboff)
			print ('Reverb Off')
			continue
	
	#Mod

	elif msg.control == 67 and msg.value == 127 and bank == 2:

		if modchkmsg.data[11] == 0:
			multi.send(modon)
			print ('Mod On')
			continue

		elif modchkmsg.data[11] == 1:
			multi.send(modoff)
			print ('Mod Off')
			continue
	
	
	#Fx
	
	elif msg.control == 68 and msg.value == 127 and bank == 2:
		
		if fxchkmsg.data[11] == 0:
			multi.send(fxon)
			print ('Fx On')
			continue
		elif fxchkmsg.data[11] == 1:
			multi.send(fxoff)
			print ('Fx Off')
			continue
	
	
	#Bank change
	
	elif msg.control == 69 and msg.value == 127 and bank == 2:
		bank -= 1
		print ('Bank 1')
		continue
	else:
		pass



