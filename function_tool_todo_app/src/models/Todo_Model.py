from pydantic import BaseModel,field_validator

class TodoModel(BaseModel):
    title:str
    description:str
    status: bool = False

    @field_validator('title')
    def validate_title(cls,value):
        if not value.strip():
            raise ValueError("title must not be empty")
        return value


        
    