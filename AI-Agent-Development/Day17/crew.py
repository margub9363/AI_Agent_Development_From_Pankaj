from crewai import Crew, Process, Task
from agents import (
    researcher, coder, reviewer
)
from tasks import (
    research_task, coding_task, reviewer_task
)

crew = Crew(agents=[researcher, coder, reviewer],
tasks=[
    research_task,
    coding_task,
    reviewer_task
],
process=Process.sequential,
verbose=True
)