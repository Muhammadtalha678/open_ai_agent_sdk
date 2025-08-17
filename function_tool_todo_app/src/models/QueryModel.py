from pydantic import BaseModel,field_validator

class QueryModel(BaseModel):
    query:str
    
    @field_validator('query')
    def validate_query(cls,value):
        if not value.strip():
             raise ValueError("Query must not be empty")
        return value