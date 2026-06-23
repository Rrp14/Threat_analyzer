

from app.enums.input_type import InputType
from app.services.parsers.base import BaseParser


class TextParser(BaseParser):


    @property
    def supported_input(self)->InputType:
        return InputType.TEXT
    
    def parse(
            self,
            content:str
    )->str:
         if not isinstance(content, str):
            raise IngestionError(
                message="TextParser expects string input.",
                details={
                    "received_type": type(content).__name__,
                },
            )
         

         normalized=(
             content.replace("\r\n","\n")
             .replace("\r","\n")
             .strip()
         )


         return normalized



        