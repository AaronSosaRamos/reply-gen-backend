from fastapi import APIRouter, Depends
from app.api.features.graph.graph import return_graph
from app.api.logger import setup_logger
from app.api.auth.auth import key_check
from app.api.schemas.schema import EmailRequest

logger = setup_logger(__name__)
router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.post("/reply-gen")
async def submit_tool( data: EmailRequest, _ = Depends(key_check)):

    logger.info("Generating the Reply Gen AI Graph")
    graph = return_graph()
    logger.info("The AI Graph has been successfully generated")
    logger.info("Generating the Reply Gen Result")
    results = graph.invoke({
        "recipient_name": data.recipient_name,
        "recipient_email": data.recipient_email,
        "subject": data.subject,
        "message_context": data.message_context
    })

    return results