from pydantic import BaseModel, Field
from typing import List, Optional, TypedDict, Any

class EmailRequest(BaseModel):
    recipient_name: str = Field(..., description="The full name of the email recipient.")
    recipient_email: str = Field(..., description="The email address of the recipient.")
    subject: str = Field(..., description="The subject line of the email.")
    message_context: str = Field(..., description="The context or body content of the email.")

class EmailBodySchema(BaseModel):
    email_body: str = Field(..., description="The initial generated email body based on the original email's context and response requirements.")
    subject: str = Field(..., description="The subject of the email response, reflecting both the original email and response purpose.")
    key_points_covered: bool = Field(..., description="Indicates whether the key points from the original email have been addressed in the response.")
    word_count: int = Field(..., description="The total word count of the email body, ensuring the response is within optimal length.")
    sentiment_analysis_score: float = Field(..., description="Sentiment analysis score of the email body (range 0.0-1.0) indicating positive or negative sentiment of the response.")
    original_tone_reflected: bool = Field(..., description="Indicates whether the response matches or adapts the tone of the original email.")

class PersonalizedEmailSchema(BaseModel):
    personalized_email: str = Field(..., description="The email content personalized with the recipient's details, including name and relevant response context.")
    personalized_greeting: str = Field(..., description="The personalized greeting for the email, tailored to the recipient's name and context of the original email.")
    personalized_sign_off: str = Field(..., description="The personalized sign-off at the end of the email, including the sender's name and position.")
    recipient_email: str = Field(..., description="The recipient's email address, ensuring it matches the original email sender for proper response delivery.")
    language_style: str = Field(..., description="The language style used in the response, e.g., formal, semi-formal, or casual, adjusted based on the original email.")
    recipient_preferences_adapted: bool = Field(..., description="Indicates whether the email response has been adapted to the recipient's preferences, such as tone or communication style, based on the original email.")

class SuggestionsSchema(BaseModel):
    suggestions: List[str] = Field(..., description="A list of suggestions for improving the response email content, such as enhancing tone, structure, or clarity.")
    improvement_areas: List[str] = Field(..., description="Specific areas of the email response content that can be improved, e.g., better alignment with the original email's tone or more concise points.")
    grammar_check: bool = Field(..., description="Indicates whether a grammar check has been performed and any errors identified in the response.")
    engagement_score_prediction: float = Field(..., description="Prediction score (range 0.0-1.0) for how engaging the email response will be to the recipient, based on the content analysis.")
    readability_score: float = Field(..., description="Readability score of the email response (range 0.0-1.0), assessing how easy it is for the recipient to read and understand the response.")

class FinalEmailSchema(BaseModel):
    final_email_response: str = Field(..., description="The finalized version of the response email content after incorporating suggestions and ensuring all necessary details are covered.")
    subject: str = Field(..., description="The final subject of the response email, aligned with both the original email and the response content.")
    tone_achieved: str = Field(..., description="The final tone achieved in the response after revisions, ensuring it matches or adapts to the original email's tone.")
    call_to_action_included: bool = Field(..., description="Indicates whether the response includes a clear call to action for the recipient to take.")
    final_word_count: int = Field(..., description="The total word count of the finalized response email, ensuring it stays within optimal length.")
    final_sentiment_analysis_score: float = Field(..., description="Final sentiment analysis score (range 0.0-1.0) after incorporating revisions, assessing the emotional tone of the response.")
    original_email_responded_to: bool = Field(..., description="Indicates whether the response fully addresses the key points and context of the original email.")

class EmailOutput(BaseModel):
    generated_email: str = Field(..., description="The initial generated response email content based on the original email and provided context.")
    suggestions: List[str] = Field(..., description="The list of suggestions generated for improving the response email content.")
    final_email_improved: str = Field(..., description="The finalized version of the response email, ready to be sent after incorporating suggestions and improvements.")
    email_success_prediction: float = Field(..., description="A prediction score (0.0-1.0) indicating the likelihood of the response email achieving its intended goal, such as prompting further action or response from the recipient.")
    open_rate_prediction: float = Field(..., description="A prediction score (0.0-1.0) indicating the likelihood of the recipient opening the response email, based on the subject line and context.")
    click_through_rate_prediction: float = Field(..., description="A prediction score (0.0-1.0) estimating the likelihood of the recipient clicking any links or taking action based on the response email content.")
    recipient_engagement_likelihood: float = Field(..., description="A prediction score (0.0-1.0) assessing the likelihood of the recipient engaging with the response email, such as replying or following the suggested call to action.")

class GraphState(TypedDict):
    recipient_name: str
    recipient_email: str
    subject: str
    message_context: str

    email_body: EmailBodySchema
    personalized_email: PersonalizedEmailSchema
    suggestions: SuggestionsSchema
    final_email: FinalEmailSchema

    email_output: Any