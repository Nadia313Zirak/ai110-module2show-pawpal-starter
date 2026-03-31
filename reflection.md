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
**b. Design changes**

Yes, I made a few small design improvements after reviewing my initial skeleton and using AI feedback.
One change I made was converting the Owner class into a dataclass to keep it consistent with the Pet and Task classes. This made the code cleaner and more uniform.
I also updated the Scheduler class to accept an optional list of tasks during initialization. This allows the scheduler to directly manage and organize tasks when generating a daily plan. Ialso  modified the PawPalSystem class to allow the owner, pet, tasks, and scheduler to be optional when the system is created. This makes the system more flexible and allows data to be added gradually instead of requiring everything upfront.
These changes improved the structure and flexibility of the system without changing the overall design.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
