import argparse
from typing import Dict, Type
from jupyter_ai_magics.providers import BaseProvider
from jupyter_ai.models import HumanChatMessage

#from jupyterlab_chat.models import Message
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import PromptTemplate

from jupyter_ai.chat_handlers.base import BaseChatHandler, SlashCommandRoutingType
from jupyter_ai.chat_handlers.learn import LearnChatHandler, Retriever

PROMPT_TEMPLATE = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_PROMPT = PromptTemplate.from_template(PROMPT_TEMPLATE)


class CustomLearnException(Exception):
    """Exception raised when Jupyter AI's /ask command is used without the required /learn command."""

    def __init__(self):
        super().__init__(
            "Jupyter AI's default /ask command requires the default /learn command. "
            "If you are overriding /learn via the entry points API, be sure to also override or disable /ask."
        )


class AskChatHandler(BaseChatHandler):
    """Processes messages prefixed with /ask. This actor will
    send the message as input to a RetrieverQA chain, that
    follows the Retrieval and Generation (RAG) technique to
    query the documents from the index, and sends this context
    to the LLM to generate the final reply.
    """

    id = "ask"
    name = "Ask a question"
    help = "Ask a question"
    routing_type = SlashCommandRoutingType(slash_id="ask")

    uses_llm = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parser.prog = "/ask"
        self.parser.add_argument("query", nargs=argparse.REMAINDER)
        import inspect
        self.log.info("MRO for AskChatHandler: %s", inspect.getmro(self.__class__))
        # NOTE: devs should use self.retriever property to access the retriever
    def create_llm_chain(
        self, provider: Type[BaseProvider], provider_params: Dict[str, str]
    ):
        unified_parameters = {
            **provider_params,
            **(self.get_model_parameters(provider, provider_params)),
        }
        self.llm = provider(**unified_parameters)
        
    async def process_message(self, message: HumanChatMessage):
        args = self.parse_args(message)
        if args is None:
            return
        query = " ".join(args.query)
        if not query:
            self.reply(f"{self.parser.format_usage()}", message)
            return
        self.get_llm_chain()
        """
        with self.start_reply_stream() as reply_stream:
            try:
                # TODO: migrate this class to use a LCEL `Runnable` instead of
                # `Chain`, then remove the below ignore comment.
                result = await self.llm._call(  # type:ignore[attr-defined]
                    query
                )
                response = result["answer"]
                # old pending message: "Searching learned documents..."
                # TODO: configure this pending message in jupyterlab-chat
                reply_stream.write(response)
            except AssertionError as e:
                self.log.error(e)
                response = Sorry, an error occurred while reading the from the learned documents.
                If you have changed the embedding provider, try deleting the existing index by running
                `/learn -d` command and then re-submitting the `learn <directory>` to learn the documents,
                and then asking the question again.
                reply_stream.write(response, message) 
        """

        try:
            with self.pending("Generating a response", message):
                # TODO: migrate this class to use a LCEL `Runnable` instead of
                # `Chain`, then remove the below ignore comment.
                response = self.llm._call(query)
            self.reply(response, message)
        except AssertionError as e:
            self.log.error(e)
            response =f"""Sorry, an error occurred while reading the from the learned documents.
            If you have changed the embedding provider, try deleting the existing index by running
            `/learn -d` command and then re-submitting the `learn <directory>` to learn the documents,
            and then asking the question again.
            """
            self.reply(response, message)
