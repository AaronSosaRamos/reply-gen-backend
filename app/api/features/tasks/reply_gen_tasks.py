from app.api.schemas.schema import FinalEmailSchema
from crewai import Task
from textwrap import dedent

class CustomTasks:
    def __init__(self):
        pass

    def content_task(self, agent, email_request: FinalEmailSchema):
        return Task(
            description=dedent(f"""
                Improve the draft email response based on the original email context and incorporate any necessary changes.

                **Original Email Context**:

                [The original email message that was received.]

                **Response Email Content**:
                {email_request.final_email_response}

                **Subject**:
                {email_request.subject}

                Ensure that the response email addresses the key points of the original email and has a clear subject.
            """),
            agent=agent,
            expected_output="A revised draft of the response email, improving on the initial draft while keeping the original email in focus."
        )

    def review_task(self, agent, email_request: FinalEmailSchema):
        return Task(
            description=dedent(f"""
                Review the draft email response for tone, grammar, and clarity. Ensure the response is professional, well-structured, and aligns with the original email's tone.

                **Email Draft**:
                {email_request.final_email_response}

                **Subject**:
                {email_request.subject}

                **Tone Achieved**:
                {email_request.tone_achieved}

                Make sure the email maintains the intended tone and responds to the original email appropriately.
            """),
            agent=agent,
            expected_output="A reviewed version of the email response, with improvements to tone, grammar, and clarity."
        )

    def personalization_task(self, agent, email_request: FinalEmailSchema):
        return Task(
            description=dedent(f"""
                Personalize the email response for the recipient based on the original email context and their specific preferences.

                **Email Response**:
                {email_request.final_email_response}

                **Recipient Information**:
                [Details about the recipient, such as their preferences.]

                **Call to Action Included**:
                {email_request.call_to_action_included}

                Ensure the response is engaging, personalized to the recipient, and contains a clear call to action.
            """),
            agent=agent,
            expected_output="A personalized version of the response email that addresses the recipient's context and includes a call to action."
        )

    def output_task(self, agent, email_request: FinalEmailSchema):
        email_output_schema = FinalEmailSchema.schema_json(indent=2)
        return Task(
            description=dedent(f"""
                Compile the final version of the email response, ensuring it incorporates all necessary revisions and personalizations, and is ready to be sent.

                **Final Email Content**:
                {email_request.final_email_response}

                **Subject**:
                {email_request.subject}

                **Final Word Count**:
                {email_request.final_word_count}

                Ensure the final email is within the optimal word length, properly responds to the original email, and matches the required format.
                You must give the response in JSON format according to the schema below:

                **Format**:
                {email_output_schema}
            """),
            agent=agent,
            expected_output=f"The finalized email response, ready for sending, in JSON format matching the schema: {email_output_schema}."
        )