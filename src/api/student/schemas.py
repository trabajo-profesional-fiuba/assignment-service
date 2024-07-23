from pydantic import BaseModel, ConfigDict


class StudentBase(BaseModel):
    uid: int
    name: str
    last_name: str
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)

    def __eq__(self, other):
        if not isinstance(other, StudentBase):
            # don't attempt to compare against unrelated types
            return NotImplemented

        is_equals = True
        if self.uid != other.uid:
            is_equals = False
        if self.name != other.name:
            is_equals = False
        if self.last_name != other.last_name:
            is_equals = False
        if self.email != other.email:
            is_equals = False
        if self.password != other.password:
            is_equals = False
        return is_equals
