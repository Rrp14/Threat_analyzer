import json

from app.core.exceptions import IngestionError
from app.enums.input_type import InputType
from app.services.parsers.base import BaseParser


class JSONParser(BaseParser):


    @property
    def supported_input(self)->InputType:
        return InputType.JSON
    
    def parse(self, content:str)->str:

         if not isinstance(content, str):
            raise IngestionError(
                message="JSONParser expects string input.",
                details={
                    "received_type": type(content).__name__,
                },
            )
         
         try:
             data=json.loads(content)

             return json.dumps(
                 data,
                 indent=2,
                 ensure_ascii=False
             )
         
         except json.JSONDecodeError as exc:
             raise IngestionError(
                 message="Invalid JSON input.",
                 details={
                     "error":str(exc)
                 },
                 
             )from exc

        
    