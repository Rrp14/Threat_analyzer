

from typing import Any

from app.enums.input_type import InputType
from app.services.parsers.base import BaseParser
from app.core.exceptions import IngestionError, ValidationError
from app.services.parsers.csv import CSVParser
from app.services.parsers.docx import DOCXParser
from app.services.parsers.json import JSONParser
from app.services.parsers.pdf import PDFParser
from app.services.parsers.text import TextParser


class InputIngestionService:

    def __init__(self)->None:
        self._parsers:dict[InputType,BaseParser]={}
        self.register_parser(TextParser())
        self.register_parser(JSONParser())
        self.register_parser(CSVParser())
        self.register_parser(PDFParser())
        self.register_parser(DOCXParser())



    def register_parser(
            self,
            parser:BaseParser
    )    ->None:
        
        if not isinstance(parser,BaseParser):
            raise ValidationError(
                "Only BaseParser instances can be registered"

            )
        
        input_type=parser.supported_input

        if input_type in self._parsers:
            raise ValidationError(
                f"Parser alreadt registered for '{input_type}'."
            )
        
        self._parsers[input_type]=parser


    def get_parser(
            self,
            input_type:InputType
    )    ->BaseParser:
        
        parser=self._parsers.get(input_type)


        if parser is None:
            raise IngestionError(
                message=f"No parser registered for '{input_type}",
                details={
                    "input_type":input_type
                }
            )
        
        return parser
    
    def ingest(
            self,
            input_type:InputType,
            content:Any
    )->str:
        parser=self.get_parser(input_type)

        return parser.parse(content)