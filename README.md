# Secureworks Software Quality Assurance/Automation Engineer Coding Challenge

## Original Instructions

Your code will be evaluated on the amount of test coverage and overall general quality too include readability, following best practices for the language, etc. Your code will be evaluated by more than one person, typically the hiring manager and potential future-coworkers that all completed a coding challenge before joining the team.  Please note they will execute their review based on the instructions you provide.

We advise using these best practices for your response:

* Provide working test cases;
* Provide full documentation of everything in your response.  Too include assumptions; 
* Provide a set of instructions for the reviewers to execute their review;
* And confirm the program runs out of the box before sending.

### QA Automation Engineer Coding Challenge

Our company develops a threat monitoring software that is cross platform and captures process executions and traffic going through physical interface. Our product runs on several endpoints like webservers which has lot of processes being spun up and heavy traffic going through the interfaces. Once we identify a process/executable, the hash will be stored in a cache for 60 seconds. If the same executable is captured within next 60 seconds, we will discard because the hash is already known and the counter will be incremented. This helps to avoid storing redundant data.

As you can guess, for our product to be an effective threat monitoring software we need to capture data accurately and most importantly capture data :-).  We would like to know the test plan/setup you will create to ensure quality of the product is good enough to be released to clients.

Additionally, can you create an automated test suite for the below:

* Given an endpoint generate a flood of processes and all have unique hash values.
* Make the test suite cross platform: Windows and Linux. If not possible, please discuss the reasons.
* One should be able to run the test on any given endpoint.

Of course in order to verify the accuracy of data captured we will have to examine the data pipeline or data stored in the database. Since that is not possible for this challenge, please discuss what other alternative ways you have to verify the same.

## My Assumptions

