# **Job Seeking Bot Assistant**

## **Description of the idea**
Helper service (telegram-bot) for job seekers, which allows you to:

- search for vacancies according to specified parameters: profession of interest, city, working hours (full-time or part-time) and desired salary;

- see top cities and companies in Russia by median salary (information taken from here);

- watch job interviews on the profession of interest;

- find useful materials to prepare for a job/interview: online courses and literature;

- learn tips that can help you succeed in your interview.

### **User Stories describing system's idea**

1. As a soon-to-be graduate, I want the bot to recommend jobs related to my field of study so that I can apply for suitable jobs in a timely manner and find my dream job.

2. As someone who struggles with interviews, I want the bot to recommend video tutorials and materials that will help me prepare for interviews and increase my confidence and preparedness level.

3. As a professional who wants to improve my skills, I want the bot to provide me with training materials and modules that will help me improve certain skills related to my field of work.

4. As a freelancer, I want the bot to recommend projects to me that match my skills and interests so I can find new clients and expand my portfolio.

5. As a job seeker looking to change careers, I want the bot to suggest jobs that match my transferable skills so I can explore new career options.


###  **Used Cloud Services**

-  Cloud Functions

- Object Storage

- API Gateway

- YDB


## **API Description**

### **API Methods**

The documentation of the API in accordance with OpenAPI Specification Version 3.0.3 is placed in the file api_docs.yaml, and can be read and used via Swagger. Methods are grouped by entities

Method | Description | Cloud Service 
--- | --- | ---
GET /vacancies/vacancy | Displaying a vacancy in accordance with the entered parameters involves accessing a third-party API (adzuna) | API Gateway
GET /materials/{vacancy}/{fileId} | Returning materials (pdf textbook for self-study) in accordance with the selected vacancy | API Gateway, Object Storage
GET /materials/interview | Returning of tips for a successful interview | API Gateway
GET /materials/courses/{vacancyTitle} | Returning a link to recommended courses for a specific vacancy or career specialization | API Gateway, YDB, Cloud Functions
GET /users | Listing all bot users from the database | API Gateway, YDB
POST /users/new_user | Creating new user | API Gateway, YDB
GET /users/{userId} | User ID output | API Gateway, YDB
PUT /users/{userId} | Updating user information by ID | API Gateway, YDB
DELETE /user/{userId} | Removing a user by ID | API Gateway, YDB
GET /salaries/cities | Returning top 10 Russian cities by median salary (IT sector) | API Gateway, YDB
GET /salaries/companies | Returning the top 10 companies in Russia by median salary (IT sector) | API Gateway, YDB


## Bot Design (diagrams and diagrams)

### C4  
C4 model was used to visualize the architecture of the service and simplify the process of its creation and communication between us (project participants) in the early stages of design.

- **Context diagram** contains general information about the system's users and other systems with which it directly interacts:

![image](https://github.com/tivakhrusheva/JobSearchAssistantBot/assets/91075802/0fe497b9-4096-43fd-9f6c-85caeb95505c)

- **Container** (contains information about the technologies that are used in development (containers) and how they interact with each other):

![image](https://github.com/tivakhrusheva/JobSearchAssistantBot/assets/91075802/0d2dbd32-0a51-49b7-a119-4af9e2a396d3)

- **Component** (contains information about what the cloud function consists of: commands, the logic of their operation and connections with other services):

![image](https://github.com/tivakhrusheva/JobSearchAssistantBot/assets/91075802/655821c5-7c77-4fa2-bbf8-8a37b192795c)

### Sequence Diagram

This type of diagram has been used to clarify the description of functions: features of user interaction with system elements. A sequence diagram can be useful when thinking through the logic of functions and their further testing.

- **Finding materials to prepare for an interview**:

![image](https://github.com/tivakhrusheva/JobSearchAssistantBot/assets/91075802/d7fd6f0f-631d-454a-94a1-1c180155aec6)

- **Viewing tips for interview success**:

![image](https://github.com/tivakhrusheva/JobSearchAssistantBot/assets/91075802/5b1c707a-b9e1-4de8-945c-a9ea93df419a)

- **Search of a suitable vacancy**

![image](https://github.com/tivakhrusheva/JobSearchAssistantBot/assets/91075802/60027bf1-82e7-4add-8cb0-b5e8ac60aef1)


### **Activity Diagram**

An activity diagram has been used to model the process of system operation when specific functions are called by the user. With its help, you can think through possible solutions when errors occur within the system.

- **Search for top companies in the Russian Federation**:

![image](https://github.com/tivakhrusheva/JobSearchAssistantBot/assets/91075802/b433e6a9-8d7e-42a3-ab55-f43b4238fca8)



## **Examples of Usage**

1. **Search settings**

The user sequentially fills in the requested parameters: first, this is the name of the vacancy (this can be an arbitrary, but existing vacancy name, otherwise nothing will be found in a third-party search), then this is the choice of work mode - full day or part-time, after which the user specifies the desired one minimum salary:

![image](https://github.com/tivakhrusheva/JobSearchAssistantBot/assets/91075802/c1861bba-b44b-463a-8029-ad41f6515e63)


At the end of the setup, the user selects a country to search for - an important limitation is that only 8 countries are available for selection, which does not include the Russian Federation - this was the limitation of the API that was able to be built freely and without visible restrictions:

![image](https://github.com/tivakhrusheva/JobSearchAssistantBot/assets/91075802/c9b88627-366d-478e-8329-577e659995ed)


After this, the user is given a list of found vacancies. He can also query them again by entering the /search command:

![image](https://github.com/tivakhrusheva/JobSearchAssistantBot/assets/91075802/59bc5325-f9c1-494d-814e-b4600e4ebe72)


All specified settings are saved in the database and are accessible via the API via the /users/{userId} endpoint:

![image](https://github.com/tivakhrusheva/JobSearchAssistantBot/assets/91075802/1ce6a9d3-2387-4cf0-92b1-127d73c7018b)


To reset the settings, you can enter the /reset command - it implies the same endpoint and query to the database, but using the DELETE method
![image](https://github.com/tivakhrusheva/JobSearchAssistantBot/assets/91075802/905ffb05-9b43-4ed8-892e-2c7b923bae4f)


2. **Materials for preparation** (bot command - **/useful**, API endpoint - **materials/{vacancy}/{fileId}**):

![image](https://github.com/tivakhrusheva/JobSearchAssistantBot/assets/91075802/dddeda89-ce8e-40e8-8100-924b28496475)

The user enters the command and then selects the specialty or direction he is interested in using the buttons. So far, only 6 options have been supported, which are shown in the screenshot. Next, the user is returned one pdf textbook for independent study and development within the framework of this specialty.
All materials are taken from the object repository. In total, each of the vacancies on the screen in the storage has three PDF options; one of them is retrieved by specifying the index from 1 to 3 in the endpoint (yes, this is a crutch). In the bot, such an index is specified by obtaining a random integer through the random module.
How it could be improved is to send the file with its name, and not the default document.

3. **Tips before the interview** (bot command - **/interview_advice**, API endpoint - **/materials/interview**):

![image](https://github.com/tivakhrusheva/JobSearchAssistantBot/assets/91075802/3e82d14e-14f1-44c1-8753-fe59d0da678a)

The user enters the command without specifying any additional parameters and receives recommendations on how to prepare for the interview. The returned response is static and issued through the dummy type in the API, but in the future it would be possible to prepare several different tips, recommendations and materials for preparing for an interview and then randomly issue one of the prepared materials.

4. **Viewing the top companies** (bot command - **/get_top_companies**, API endpoint - **/salaries/companies**):

![image](https://github.com/tivakhrusheva/JobSearchAssistantBot/assets/91075802/2f6fc6b9-f7b0-4590-8139-aa406546c7ca)

The user enters the command without specifying any additional parameters, and receives a list of 5 companies with the highest median salaries at the end of the first half of 2023. For now, this answer is also static - it is taken from the database and additionally filtered in Yandex functions, i.e. it does not change depending on when the handle is pulled, but it is assumed that in a bright future such data would be updated in the database at least every month. In the bright future, it is also expected to be possible to specify the number of top companies to be returned.

5. **Viewing the top cities by salary** (bot command - **/get_top_salary_cities**, API endpoint - **/salaries/cities**):

![image](https://github.com/tivakhrusheva/JobSearchAssistantBot/assets/91075802/8ea2ae33-d3ba-49bb-988c-3e63889ac483)

6. **Career Course Recommendation** (bot command - **/recommend_course**, API endpoint - **/materials/courses/{vacancyTitle}**):

![image](https://github.com/tivakhrusheva/JobSearchAssistantBot/assets/91075802/1ccb3702-e105-43f6-86ea-7fe789fd4db8)

After entering the command, the user selects the direction of interest through the button, then the course for this specialization is retrieved from the database table. So far, there is only one recommended course in the table for one specialization, but with expansion it would be possible to expand the list.   


