from app.api.features.agents.reply_gen_agents import CustomAgents
from app.api.features.tasks.reply_gen_tasks import CustomTasks
from app.api.schemas.schema import FinalEmailSchema
from crewai import Crew

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class EmailGeneratorCrew:
    def __init__(self):
        self.agents = CustomAgents()
        self.tasks = CustomTasks()

    def kickoff(self, state):

        content_agent = self.agents.content_agent()
        review_agent = self.agents.review_agent()
        personalization_agent = self.agents.personalization_agent()
        output_agent = self.agents.output_agent()

        final_email_result = FinalEmailSchema(**state["final_email"])

        content_task = self.tasks.content_task(content_agent, final_email_result)
        review_task = self.tasks.review_task(review_agent, final_email_result)
        personalization_task = self.tasks.personalization_task(personalization_agent, final_email_result)
        output_task = self.tasks.output_task(output_agent, final_email_result)

        crew = Crew(
            agents=[
                content_agent,
                review_agent,
                personalization_agent,
                output_agent,
            ],
            tasks=[
                content_task,
                review_task,
                personalization_task,
                output_task,
            ],
            verbose=True,
        )

        result = crew.kickoff()

        return {**state, "email_output": result}