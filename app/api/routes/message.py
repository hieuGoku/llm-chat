from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.database.models import get_db
from app.api.schemas.agent import (
    ChatAgentResponseSchema,
)
from app.api.schemas.message import (
    UserMessageSchema,
    MessageSchema,
    MessageCreateSchema,
)
from app.api.integrations.processing import (
    craft_agent_chat_context,
    craft_agent_chat_first_message,
    craft_agent_chat_instructions,
)
from app.api.service.message import MessageService
from app.api.service.conversation import ConversationService
from app.api.integrations.openai import OpenAIIntegrationService
from app.logger.logger import custom_logger


router = APIRouter()
message_service = MessageService()
conversation_service = ConversationService()


@router.get("", response_model=List[MessageSchema])
async def manage_messages(conversation_id: str, db: Session = Depends(get_db)):
    """
    Get all messages for a conversation endpoint.
    """
    custom_logger.info(f"Getting all messages for conversation id: {conversation_id}")
    db_messages = message_service.get_messages(db, conversation_id)
    custom_logger.info(f"Messages: {db_messages}")

    return db_messages


@router.post("/chat-agent", response_model=ChatAgentResponseSchema)
async def chat_completion(message: UserMessageSchema, db: Session = Depends(get_db)):
    """
    Get a response from the GPT model given a message from the client using the chat
    completion endpoint.

    The response is a json object with the following structure:
    ```
    {
        "conversation_id": "string",
        "response": "string"
    }
    ```
    """
    custom_logger.info(f"User conversation id: {message.conversation_id}")
    custom_logger.info(f"User message: {message.message}")

    conversation = conversation_service.get_conversation(db, message.conversation_id)

    if not conversation:
        # If there are no conversations, we can choose to create one on the fly OR raise an exception.
        # Which ever you choose, make sure to uncomment when necessary.

        # Option 1:
        # conversation = agents.crud.create_conversation(db, message.conversation_id)

        # Option 2:
        return HTTPException(
            status_code=404,
            detail="Conversation not found. Please create conversation first.",
        )

    custom_logger.info(f"Conversation id: {conversation.id}")

    # NOTE: We are crafting the context first and passing the chat messages in a list
    # appending the first message (the approach from the agent) to it.
    context = craft_agent_chat_context(conversation.agent.context)
    chat_messages = [craft_agent_chat_first_message(conversation.agent.first_message)]

    # NOTE: Append to the conversation all messages until the last interaction from the agent
    # If there are no messages, then this has no effect.
    # Otherwise, we append each in order by timestamp (which makes logical sense).
    hist_messages = conversation.messages
    hist_messages.sort(key=lambda x: x.timestamp, reverse=False)
    if len(hist_messages) > 0:
        for mes in hist_messages:
            custom_logger.info(
                f"Conversation history message: {mes.user_message} | {mes.agent_message}"
            )
            chat_messages.append({"role": "user", "content": mes.user_message})
            chat_messages.append({"role": "assistant", "content": mes.agent_message})
    # NOTE: We could control the conversation by simply adding
    # rules to the length of the history.
    # if len(hist_messages) > 10:
    #     # Finish the conversation gracefully.
    #     custom_logger.info("Conversation history is too long, finishing conversation.")
    #     api_response = agents.api.schemas.ChatAgentResponseSchema(
    #         conversation_id = message.conversation_id,
    #         response        = "This conversation is over, good bye."
    #     )
    #     return api_response

    # Send the message to the AI agent and get the response
    service = OpenAIIntegrationService(
        context=context,
        instruction=craft_agent_chat_instructions(
            conversation.agent.instructions, conversation.agent.response_shape
        ),
    )
    service.add_chat_history(messages=chat_messages)

    response = service.answer_to_prompt(
        # We can test different OpenAI models.
        model="gpt-3.5-turbo",
        prompt=message.message,
        # We can test different parameters too.
        temperature=0.5,
        max_tokens=1000,
        frequency_penalty=0.5,
        presence_penalty=0,
    )

    custom_logger.info(f"Agent response: {response}")

    # Prepare response to the user
    api_response = ChatAgentResponseSchema(
        conversation_id=message.conversation_id, response=response.get("answer")
    )

    # Save interaction to database
    db_message = message_service.create_conversation_message(
        db=db,
        conversation_id=conversation.id,
        message=MessageCreateSchema(
            user_message=message.message,
            agent_message=response.get("answer"),
        ),
    )
    custom_logger.info(f"Conversation message id {db_message.id} saved to database")

    return api_response
