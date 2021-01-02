import mido
mido.get_input_names() # Shows the midi device names
mididev = mido.get_input_names() # Its necessary to create a variable for input names so the program can find them even if they change names. 
btmidi = mididev[0] # From observing mido.get_input_names() output, ive determined that my midi devices stay always in the same position, so mididev[0] always refer to the same device.
katana1 = mididev[1]
katana2 = mididev[2]
katana3 = mididev[3]
out1 = mido.open_output(katana1) # Creating the output ports because i dont know wich of the 3 is the one i need, so i send the message to all of them.
out2 = mido.open_output(katana2)
out3 = mido.open_output(katana3)
from mido.ports import MultiPort # Multiport is needed because of the 3 katana ports generated.
multi = MultiPort([out1, out2, out3])
ch1a = mido.Message('program_change', program=0) # Well, from sheer fcking luck the katana program change (pc) messages for channel switching are basic values.
ch2a = mido.Message('program_change', program=1)
ch1b = mido.Message('program_change', program=5)
ch2b = mido.Message('program_change', program=6)
chp = mido.Message('program_change', program=4)
boost = mido.Message('control_change', channel=1, control=62) # Dosnt work :(
input = mido.open_input(btmidi)
print ('Start')
from time import sleep 
while True:
        sleep(0.1) # Some amount of sleep is needed between cycles so it dosnt break the loop (this sleep was the last i added).
        msg = input.receive(block=True) # Reads the input from the bt controller; (block=True) is maybe useless here, but it works so i wont touch it.
        print ('Running')
        if msg.control == 64:  # Series of if commands that sends the channel switch message based on the btctl input.
                multi.send(ch1a)
        elif msg.control == 66:
                multi.send(ch2a)
        elif msg.control == 65:
                multi.send(ch1b)
        elif msg.control == 67:
                multi.send(ch2b)
        elif msg.control == 68:
                multi.send(chp)
        else:
                pass # Else/pass needed because if msg.control values are different from (64,65,66,67,68), the loop would end and the program would stop.
                sleep(0.1) # A little more time because before i added it, the loop wouldnt run for more than a couple of minutes, maybe because the pi would run out of RAM, or some other reason.
sleep(1) # Because why not?
print ('Error') # Never saw this message, so maybe thats a good thing? Well, i added it after the code was running mostly fine.