# Socrates system

## Layer 0  
### Elements
The system consists of 2 main parts- frontend and backend. 
The frontend will run on "frontzxcvPC" and the backend will run on "backqwerPC".(if you don't know, please see ToCursor_01.md)
### What do they do?
#### frontend
-As soon as it starts to run, it sends connection request via tcpsocket.  
-If the socket connection gets lost by accident, it recovers connection as soon as possible. The connection state should be shown to user on GUI.  
-When it receives gpt-assisted answer from the backend, displays the answer on GUI.  
-If user clicks button or presses specified key to control the backend, it will send corresponding instruction message to the backend via the socket.  
#### backend
-As soon as it starts to run, it listens for tcpsocket connection request from the frontend.  
-If the socket connection gets lost by accident, it listens again for the another connection request.  
-(this is one of the most important function of the backend)It always observes the sound stream from speaker output of backqwerPC and as soon as it gets instruction message from the frontend, it will do the corresponding action such as starting recording, ending recording, sending recorded sound stream  to gpt to have an answer, sending gpt's answer to the frontend.  
**In a word, the backend is event-driven. For example, tcpsocket connection request, getting instruction message,  getting gpt's answer.**

