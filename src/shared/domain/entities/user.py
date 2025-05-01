from pydantic import BaseModel
from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.user_status import USER_STATUS

class User(BaseModel):
	user_id: str
	name: str
	email: str
	phone: str
	role: ROLE
	user_status: USER_STATUS
	created_at: int
	updated_at: int 
	email_verified: bool
	phone_verified: bool
	enabled: bool
	
	@staticmethod
	def from_dict_static(data) -> 'User':
		return User(
			user_id=data['user_id'],
			name=data['name'],
			email=data['email'],
			phone=data['phone'],
			role=ROLE[data['role']],
			user_status=USER_STATUS[data['user_status']],
			created_at=int(data['created_at']),
			updated_at=int(data['updated_at']),
			email_verified=data['email_verified'],
			phone_verified=data['phone_verified'],
			enabled=data['enabled']
		)
	
	def to_dict(self) -> dict:
		return {
			'user_id': self.user_id,
			'name': self.name,
			'email': self.email,
			'phone': self.phone,
			'role': self.role.value,
			'user_status': self.user_status.value,
			'created_at': self.created_at,
			'updated_at': self.updated_at,
			'email_verified': self.email_verified,
			'phone_verified': self.phone_verified,
			'enabled': self.enabled
		}
  
	def from_dict(self, data: dict) -> 'User':
		return User.from_dict_static(data)

	def to_auth_dto(self) -> dict:
		return {
			'sub': self.user_id,
			'name': self.name,
			'email': self.email,
			'phone_number': self.phone,
			'custom:role': self.role.value,
			'enabled': self.enabled,
			'email_verified': self.email_verified,
			'phone_verified': self.phone_verified
		}

	def to_public_dict(self) -> dict:
		return self.to_dict()