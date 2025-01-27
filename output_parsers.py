from typing import List, Dict, Any
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Summary(BaseModel):
    summary: str = Field(description="summary")
    facts: List[str] = Field(description="interesting facts about them")

    # to_dict helps to serialise the fields
    def to_dict(self) -> Dict[str, Any]:
        return {"summary": self.summary, "facts": self.facts}


# init the PydanticOutputParser
summary_parser = PydanticOutputParser(pydantic_object=Summary)
