From now, you are expert Python developer.
Your task is to build python pakage named "socrates".


# Who will use this package?  
Anyone who wants to cheat interviewer and win the interview with AI-assistant.  
Anyone who wants to have automatic answer to interviewer's questions.  

# How will they use this package?
This system consists of frontend and backend in big picture.
Typical user will have 2 PC(personal comuter) generally. One is just for running interview-channel such as Google Meet or Zoom. Another one is for controlling the screen of the first one using remote controllers like AnyDesk or TightVNC and most importantly for seeing some help from third-parties like chatgpt or our Socrates system. Let's call the first one "backqwerPC", and call the second one "frontzxcvPC".

The frontend part of socrates system will run on frontzxcvPC and the backend part will run on backqwerPC.
The functionality of each part will be following in systemDesign.md.
To use socrates, they will install this pakage by cli like the following.

On backqwerPC, 
```bash
pip install socrates
socrates -b [port] [password]
```
Then the backend will start to run.


On frontzxcvPC,
```bash
pip install socrates
socrates -f [backend_ip_address] [backend_port] [password]
```
Then the frontend will start to run.

# What you have to now.
First of all, make a folder named "socrates" and you should play inside there.
1. You have to construct project structure and development environment so that we can develop code to implement requirements from systemDesign.md and finally build python pakage easily, which will be used by cli as you seen above.
2. Then, please go ahead developing derived tasks in each part of the project as much as you can.
# Caution
This system includes usage of OpenAI api to take advantage of chatgpt. Here, I strongly want to develop the part of using AI at last. So please consider making some mocks for non-real AI agent to develop successfully the steps before final ai-concentrated development.
