# file-sharing-network

Client and server, based on TCP for file sharing.  
Implemented with Python 2.7 on Linux.

## Run

Simulation of `user1` sharing a file to `user2`: 

Step #1:  
Prepare a folder to simulate `user1` and a folder to simualte `user2`, and run the server on a chosen port from the folder of `user1`.

![alt text](./screenshots/step1.png 'Step #1')  

Step #2:  
From `user1` run the client on mode `0` for Listening Mode, and specify the server's IP and port, and the listening port.  

![alt text](./screenshots/step2.png 'Step #2')  

Step #3:  
From `user2` run the client on mode `1` for User Mode, and specify the server's IP and port.  

![alt text](./screenshots/step3.png 'Step #3')  

Step #4:  
Search for a file name in double quotation marks, for example: "a".  

![alt text](./screenshots/step4.png 'Step #4')  

Step #5:  
Select the desired file by specifying its number.  

![alt text](./screenshots/step5.png 'Step #5')  

And the file was transferred to `user2` folder!