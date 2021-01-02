# Katana-Bluetooth-controller
A very simple script for using a bluetooth-midi (or usb) controller for changing channels on a Boss Katana MK2 using a Raspberry Pi


Objective: create a simple program that runs at boot so i can control the amp without a cellphone connected to it.


Disclaimer:
  This is my first ever code, i had 0 previous knowledge about programing or python or linux. This was my first contact with a rpi (wich i bought for this sole purpose). This code was made because i couldnt find anything like it while searching.


Requirements:

  Boss Katana (it can work with mk1 and mk2, but since i have the 50 mk2, ive only searched mappings for mk2)

  Raspberry pi (Im using a 4b, but any model with bluetooh should work, if youre using bt)

  A controller capable of sending signals (Im using an AirTurn bt-200s-6, wich can send midi messages, but with a little bit of tweaking, this should work with conventional keyboards or anything capable of sending signals that python can understand)

  A printer usb-printer cable for connecting to the amp.

  The mapping for the katana midi messages from https://www.vguitarforums.com/smf/index.php?topic=27749.0

  A lot of patience and disposition to search for solutions to problems.


Software requirements:

  A lightweight distro of linux for the pi (im using raspbian little) so it boots faster.
 
  Bluez recompiled with midi enabled (use this guide https://tttapa.github.io/Pages/Ubuntu/Software-Installation/BlueZ.html)

  Python 3 or above with mido and rtmidi modules

  Read-only mode so you can unplug power without fear of corrupting something (https://learn.adafruit.com/read-only-raspberry-pi/)

  One of the many methods for executing the script at boot


Simplified instalation (i will add a more detailed version later): 

  Install all the requirements

  (If using bluetooth) Connect the controller using the bluetoothctl command (scan on, pair xx:xx:xx:xx:xx, trust xx:xx:xx:xx:xx, exit)

  Copy the script to a folder

  Edit the script to your needs (from my testing, my controller is always the first midi device to be listed on mido.get_input_names(), followed by the 3 katana inputs. If thats true for everyone, then the only thing that needs editing is the msg values. If youre using a usb controller, then maybe youll need to change the x in mididev[x] for a value that corresponds to that device. It will probably be a value between 0-4)

  Enable autologin on the pi

  Set the script to run at boot


Use:
  With the rpi off, connect the katana trough usb and turn on the controller. Turn on the rpi, wait a little so it initializes everything and you good to go.


Permission: You can use this code for anything you want, edit it at your will. I only ask that if you improve it somehow, share it so i can improve it too and more people can get the benefits.


Special thanks to snhirsch for creating a super useful program that extends the katana patch storage capabilities wich was proof that it was possible (check it out here https://github.com/snhirsch/katana-midi-bridge) and neuma studio (https://neuma.studio/rpi-as-midi-host.html) for a tutorial that also inspired me to make this.
A big thank you for the linux/raspberry community for being super helpful with thousands of pre answered questions i had with this project.


In the future i wish to make so can turn on/off the devices at any time and the script will just run when it recognizes the necessary devices, and try an integration with the amazing katana-midi-bridge from snhirsch so its possible for both storing more presets and changing channels/switching effects with the same devices, but thats a little out of my confort zone right now. I also wish to learn i little bit more about the midi messages used in the katana so its possible to not only change channels, but use most of the features of this amazing amp.
