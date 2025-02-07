Notes of my Dell:
Apart: saving ssh key in /home/bernardo/.ssh/id_rsa
password: gitpassword
The key fingerprint is:
SHA256:ZPuNlHOSUYcvR57/aE3V/z9wbtz6pL42k486E6OE8Ok amigosolar.energy@gmail.com

# Cem6_practicing

I had to do this connecction on my Dell because I have here installed Linux Ubuntu as operational system.

To check on which port was connected my rtu modbus sensor I had to run: ls /dev/ttyUSB*
Then I have to give permissions so the file could run it: sudo chmod g+rwx, u+rwx, o+rwx
When I give others permission were when got connected. I have to check which permission needs.

When we use read_holding_registers method the address is the address of the register we are going to read. Count is the number of address we are going to read before the first address we type. And slave is the id is the id of the divice.

With the method write_registers, address is the address of the register we are going to write, the values is an array of the values we are going to set and the slave is the actual slave id of that divice.

change_slave_id_one.py is doing two things: first reading the connected divice with its original slave id and reading some of its registers. Then is setting a new slave id and writing it to the divice, and again reading some registers of the divice using the new slave id.

checking_full_lectures_two.py is reading all registers from the cem6, just to compare the index of the lecture with the modbus address of tha datasheet. There are some differences and some values that I don't know where they came from.

find_slave_id_three.py is a file to find the id of a device... For now it's not working...

saving_lectires_four.py is reading some of the divice data in an infinite loop. At the same time is creating a variable with the actual time (every 60 seconds) to be taken with the registers and been inserted into a database named cem6_lectures_sample.
This device is taking correct lectures of directions 0 to 6 then take 8 and repeat the same mesure of 8 on 46. Other electrical parameters are incorrect.

gateway_six.py is conecting to the Legrand webserver, and reading the cem6 registers throuth it.

one_consumer_device.py is reading and storing the same registers the divice show on its display. Except the kVArh because its value has a mistake. This lectures are getting stored at cem6.db database.

one_consumer_cem6_lectures.py is a file to manipulate data from the database and make operations until get a bill for electric energy. Is importing invoice function from one_consumer_pdf.py to use it with the actual variables.

one_consumer_pdf.py is a file to generate bills or invoice every defined time. Also to show some historical data in a graphic.

one_consumer_add_user.py add into the database cem6.db in table users manually. This is to have the users but is not practical if there are many users. To a bigger application is better to create all users in an excel and then bring the values into this database.

one_consumer_ files are the first application completed for one cem6 working directly with my computer.