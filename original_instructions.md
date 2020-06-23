# Original Instructions

Your code will be evaluated on the amount of test coverage and overall general quality too include readability, following best practices for the language, etc. Your code will be evaluated by more than one person, typically the hiring manager and potential future-coworkers that all completed a coding challenge before joining the team.  Please note they will execute their review based on the instructions you provide.

We advise using these best practices for your response:

* Provide working test cases;
* Provide full documentation of everything in your response.  Too include assumptions; 
* Provide a set of instructions for the reviewers to execute their review;
* And confirm the program runs out of the box before sending.

## QA Automation Engineer Coding Challenge

Our company develops a threat monitoring software that is cross platform and captures process executions and traffic going through physical interface. Our product runs on several endpoints like webservers which has lot of processes being spun up and heavy traffic going through the interfaces. Once we identify a process/executable, the hash will be stored in a cache for 60 seconds. If the same executable is captured within next 60 seconds, we will discard because the hash is already known and the counter will be incremented. This helps to avoid storing redundant data.

As you can guess, for our product to be an effective threat monitoring software we need to capture data accurately and most importantly capture data :smile:.  We would like to know the test plan/setup you will create to ensure quality of the product is good enough to be released to clients.

Additionally, can you create an automated test suite for the below:

* Given an endpoint generate a flood of processes and all have unique hash values.
* Make the test suite cross platform: Windows and Linux. If not possible, please discuss the reasons.
* One should be able to run the test on any given endpoint.

Of course in order to verify the accuracy of data captured we will have to examine the data pipeline or data stored in the database. Since that is not possible for this challenge, please discuss what other alternative ways you have to verify the same.

---

## Follow-up Questions & Answers

### Questions: Emulated Endpoint Agent & "Flood of Processes"

As I read it, in order to have a harness test against the scenario described, I must:

* Create a _simulated endpoint agent_ which replicates a small portion of the functionality that **Red Cloak** provides. At minimum, it must:
  * Track all existing processes (e.g., PID, process name)
  * Using some sort of hashing, continue to sample the endpoint environment and not trigger a "new process found" state unless the process re-emerges > 60 seconds after first discovery.
  * A counter of some sort will be incremented (the counter is incremented if process has already been seen?)
* Besides the existing "real" processes existing on the endpoint tested against (whether bare metal OS box or a VM), I need to create _yet another process_ which in turn generates faux processes which can be tracked per the above.
* With those two processes in place, I need to create a test harness which will expect certain conditions to be existent within the emulated endpoint agent.

### Reply to Questions

Thanks for asking these questions.

The intention of the challenge was not necessarily to create a dumb agent. It was more about treating it as a black box.

Kind of #2 and #3 from your points below.

The points I was mainly interested to see are:

* Are we able to understand the functionality of a threat monitoring sensor?
* Type of telemetry gathered?
* What are the break points and places to go wrong?
* How do we ensure we capture data and the right data?

However, if you really want to take it one step extra to earn bonus points :smile: , feel free to attempt a dumb agent. Keep it as simple as possible and don’t have to do processes and netflows both. Pick either one of them.

If you are not able to design a dumb agent at least discuss ways this could be done and associated verification.

 Also, since we don’t have an upstream (or downstream) connection to the cloud what other ways we can employ to verify the accuracy of data captured.

 Hope this helps. Feel free to reach out if necessary.