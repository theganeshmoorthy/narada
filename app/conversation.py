import dataclasses
import typing as t
from datetime import datetime, timezone
from pinecone import Pinecone, ServerlessSpec
import asyncio
from ollama import AsyncClient

@dataclasses.dataclass
class ChatMessage:
    """
    A simple storage class containing all the information about a single chat message.
    """

    role: t.Literal["user", "assistant"]
    timestamp: datetime
    text: str

@dataclasses.dataclass
class Conversation:
    """
    The Conversation class represents a chat conversation, containing multiple chat messages.
    """
    # The entire message history    
    messages: list[ChatMessage] = dataclasses.field(default_factory=list)
    
    async def respond(self, client: AsyncClient) -> ChatMessage:
        """
        Generate a response from the assistant based on the current converation request.
        Raises an error if the last conversation message is not from the user.
        """

        # Make sure the last message is from the user
        if not self.messages or self.messages[-1].role != "user":
            raise ValueError("The last message must be from the user to generate a response.")
        
        # Prepare messages for the API
        # api_messages = list[t.Any] =  [
        #     {"role": "system", "content": "You are a helpful assistant. Format your responses as markdown. Use ** for bold and _ for italics."}
        # ] + [
        #     {"role": msg.role, "content": msg.text} for msg in self.messages
        # ]
        pc = Pinecone(api_key="pcsk_2q8aUh_D1524UpDbQehKgqLVdWR8iB4sYR66Z7WdAUdTAdJx3UBixMQb4BrKgofVLVyGkg")
        index_name = "rag-test"
        dense_index = pc.Index(index_name)

        user_query = self.messages[-1].text
        # Search the vector database for relevant context
        results = dense_index.search(
            namespace="sample_namespace",
            query={
                "top_k":10,
                "inputs": {
                    'text': user_query
                }
            },
            rerank={
                "model": "bge-reranker-v2-m3",
                "top_n": 5,
                "rank_fields": ["chunk_text"]
            }
        )
        #print(f"The results are {results}")

        chunks = []
        for hit in results['result']['hits']:
            chunk_text = hit['fields']['chunk_text']
            chunks.append(chunk_text)
        context = '\n\n'.join(chunks)
        #print(f"The Context is {context}")
        message = {
            "role": self.messages[-1].role,
            "content": f"""
                Use the following pieces of context to answer the user's question. Do not use any other material othen than the provided context.
                If you don't know the answer, just say that you don't know, don't try to make up an answer.
                If the question is not related to the context, politely inform them that you are tuned to only answer questions that are related to the context.
                if the context is empty, politely inform them that you don't have enough information to answer the question.
                Context: {context}
                Question: {self.messages[-1].text}
            """
        }
        
        # Call the API to get a response
        response = await client.chat(
            model="llama3.1",
            messages=[message],
            stream=False,
        )
        print(response)
        assert isinstance(response.message.content, str), "Expected response content to be a string"
        
        # Create a new ChatMessage for the assistant's response
        assistant_message = ChatMessage(
            role="assistant",
            timestamp=datetime.now(timezone.utc),
            text=response.message.content
        )
        
        # Append the assistant's message to the conversation history
        self.messages.append(assistant_message)
        
        return assistant_message