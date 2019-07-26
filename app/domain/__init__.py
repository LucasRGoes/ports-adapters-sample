"""
Domain
======
	The domain covers all aspects of the application's business logic, holding
models, the commands and events associated with the application, interfaces
for repositories and event queues to implement and "glue" code for the
orchestration of everything.

OBS: A good practice is remembering that business logic should always consider
all of the business problems, so being able to solve every aspect of those
problems in the domain and not raising solvable errors so that other modules
take care of them is important.
"""
