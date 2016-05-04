# Encrypted-Chat-Client
A Chat Client with Group and Secret Chat( based on Encryption) options. Two Layers of Encryption have been used.

To run the project, following are the steps required:
1. Copy the required files ( Server.py and format.py for Server and BREA.py, RSA.py, MathBox.py, Client.py and ClientConsole.py for Client ).
2. Create a Server by running Server.py or Server.pyw( doesn't open the command prompt window ) on the localhost or on the network( default is localhost ) by specifying the IP Address and the port number ( default is 8888 ). IP Address and Port No can be changed in the Server.py File.
3. Run ClientConsole.py or ClientConsole.pyw and connect to the Server by specifying either localhost or the IP Address used in the first step.
4. Choose an appropriate Nickname.
5. A Chat Box will be opened.
6. To chat privately double click on the user in the Users List and only that user will be able to see the message.
7. Check connect to Broadcast to send a message to all the users.
8. Check see all messages to see all the messages being sent, however you'll only be able to decrypt the boradcasted messages or messages sent to you.
