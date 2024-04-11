from collections import OrderedDict
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings

MODEL_CLASS_MAPPING = OrderedDict(
    [
        ("qwen1.5-14b-chat", ChatOpenAI),
        ("gpt-3.5-turbo", ChatOpenAI),
        ("text-davinci-003", OpenAIEmbeddings),
        ("sentence-transformers/all-mpnet-base-v2", HuggingFaceEmbeddings)
    ]
)

class AutoModel:
    def __init__(self, *args, **kwargs):
        raise EnvironmentError(
            f"{self.__class__.__name__} is designed to be instantiated "
            f"using the `{self.__class__.__name__}.from_repository(model_name_or_path)`"
        )
    
    @classmethod
    def from_repository(cls, model_name_or_path: str, **kwargs):
        """Instantiate one of the model classes of the library from 'model_name_or_path' property.

        Examples:
        ```python
        >>> model = AutoModel.from_repository("qwen1.5-14b-chat")
        ```
        """
        if model_name_or_path in MODEL_CLASS_MAPPING:
            model_class = MODEL_CLASS_MAPPING.get(model_name_or_path)
            if hasattr(model_class(), "model_name"):
                return model_class(model_name=model_name_or_path, **kwargs)
            elif hasattr(model_class(), "model"):
                return model_class(model=model_name_or_path, **kwargs)
        raise ValueError(
            f"Unrecognized model_name_or_path identifier: ({model_name_or_path}). Should contain one of {', '.join(MODEL_CLASS_MAPPING.keys())}"
        )