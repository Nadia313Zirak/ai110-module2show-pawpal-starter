# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

ANS: 
The initial design centers around on three core actions a user has the ability to perform:

1- The system is designed to help a pet owner manage and organize daily pet care tasks.

2- The user should be able to enter basic information about the owner and pet so the system knows who the schedule is for.


3- The user should be able to add and manage pet care tasks such as feeding, walks, medication, grooming, and enrichment, including details like duration and priority.

4- The user should be able to generate and view a daily care plan that organizes tasks based on constraints, priorities, and available time, while also explaining why the plan was chosen.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.


Yes, I made a few small design improvements after reviewing my initial skeleton and using AI feedback.
One change I made was converting the Owner class into a dataclass to keep it consistent with the Pet and Task classes. This made the code cleaner and more uniform.
I also updated the Scheduler class to accept an optional list of tasks during initialization. This allows the scheduler to directly manage and organize tasks when generating a daily plan. Ialso  modified the PawPalSystem class to allow the owner, pet, tasks, and scheduler to be optional when the system is created. This makes the system more flexible and allows data to be added gradually instead of requiring everything upfront.
These changes improved the structure and flexibility of the system without changing the overall design.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
ANS:
-The scheduler considers several constraints, including available time, task priority, completion status, and scheduling time. Tasks are prioritized based on their priority level, and only tasks that fit within the owner’s available time are included in the daily plan. This ensures that the generated schedule is both realistic and efficient.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
ANS:
-One tradeoff my scheduler makes is in the conflict detection logic. Right now, it only checks whether two tasks have the exact same date and time. This is simpler and easier to understand, but it does not detect partial overlaps based on task duration. For example, if one task starts at 8:00 and lasts 30 minutes, and another starts at 8:15, the current version would not flag that as a conflict.I think this tradeoff is reasonable for this project because it keeps the algorithm lightweight, readable, and easier to test. Since PawPal+ is a beginner-friendly scheduling app.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
ANS:
-I used VS Code Copilot throughout the project for generating class structures, implementing methods, debugging errors, and writing tests. Copilot was especially helpful for generating boilerplate code, suggesting Pythonic solutions such as using sorted() with lambda functions, and helping implement features like recurring tasks and conflict detection.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---ANS:
-One example where I modified AI output was when Copilot suggested overly complex logic for scheduling tasks. I simplified the implementation to prioritize readability and maintainability. I also verified AI-generated code by testing it in my main.py demo and using pytest to ensure correctness before accepting it

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
ANS: 
- One example where I modified AI output was when Copilot suggested overly complex logic for scheduling tasks. I simplified the implementation to prioritize readability and maintainability. I also verified AI-generated code by testing it in my main.py demo and using pytest to ensure correctness before accepting it

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---ANS:
-I am confident that my scheduler works correctly for the main use cases and common edge cases. However, additional testing could be done for more complex scenarios such as overlapping task durations or large numbers of tasks.


## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
ANS:
-One aspect that went well was successfully integrating the backend logic with the Streamlit UI. I was able to create a system where user actions in the UI directly triggered the scheduling logic, making the application interactive and functional.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
ANS:
I would improve the scheduling algorithm to handle overlapping tasks and optimize task selection further. I would also enhance the UI design to make it more visually appealing and user-friendly.
**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

ANS:
-One important takeaway from this project is that working with AI tools like Copilot requires strong human oversight. As the “lead architect,” I was responsible for guiding the design, evaluating AI suggestions, and ensuring that the system remained clean, logical, and maintainable. AI was a powerful assistant, but the final decisions and structure depended on my understanding of the system.
