# file-sharing-network

Client and server, based on TCP for file sharing.  
Implemented with Python 2.7 on Linux.

## Run

Simulation of `user1` sharing a file to `user2`: 

Step #1:  
Prepare a folder to simulate `user1` with a file to transfer, and a folder to simulate `user2`.  
Run the server on a chosen port from the folder of `user2`, using the following command:
`user2:~$ python server.py <server-port>`  

![alt text](./screenshots/step1.png 'Step #1')  

Step #2:  
From `user1` run the client on mode `0` for Listening Mode, and specify the server's IP and port, and the listening port, using the following command:  
`user1:~$ python client.py 0 <server-ip> <server-port> <listening-port>`  

![alt text](./screenshots/step2.png 'Step #2')  

Step #3:  
From `user2` run the client on mode `1` for User Mode, and specify the server's IP and port, using the following command:  
`user2:~$ python client.py 1 <server-ip> <server-port>`  

![alt text](./screenshots/step3.png 'Step #3')  

Step #4:  
Search for a file name in double quotation marks, for example: `"a"`.  

![alt text](./screenshots/step4.png 'Step #4')  

Step #5:  
Select the desired file by specifying its number, for example: `1`.  

![alt text](./screenshots/step5.png 'Step #5')  

And the file was transferred to `user2` folder!
