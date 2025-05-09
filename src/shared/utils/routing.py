from typing import Any

from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError, BadRequest
from src.shared.helpers.errors.errors import MissingParameters, ForbiddenAction

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.enums.vip_level import VIP_LEVEL

DEFAULT_ALLOWED_USER_ROLES = [ ROLE.ADMIN ]

def controller_execute(
    Usecase: Any,
    request: IRequest,
    allowed_user_roles: list[ROLE] = DEFAULT_ALLOWED_USER_ROLES,
    required_vip_status: VIP_LEVEL = VIP_LEVEL.VIP_1
) -> IResponse:
    try:
        requester_user = request.data.get('requester_user')

        if requester_user is None:
            raise MissingParameters('requester_user')
        
        requester_user = AuthAuthorizerDTO.from_api_gateway(requester_user)

        if requester_user.role not in allowed_user_roles:
            raise ForbiddenAction('Acesso não autorizado')
        
        if not verify_user_status(requester_user, required_vip_status):
            raise ForbiddenAction('Acceso não autorizado (VIP)')
        
        response = Usecase().execute(request.data)

        if 'error' in response:
            return BadRequest(response['error'])
        
        return OK(body=response)
    except MissingParameters as error:
        return BadRequest(error.message)
    except ForbiddenAction as error:
        return BadRequest(error.message)
    except:
        return InternalServerError('Erro interno de servidor')
    
def verify_user_status(requester_user: AuthAuthorizerDTO, required_vip_status: VIP_LEVEL) -> bool:
    if required_vip_status == VIP_LEVEL.FREE:
        return True
    
    if requester_user.role == ROLE.ADMIN:
        return True
    
    if requester_user.role == ROLE.TEACHER:
        return True
    
    if requester_user.role != ROLE.VIP:
        return False

    repository = Repository(
        auth_repo=True,
        vip_subscription_repo=True
    )

    vip_subscription = repository.vip_subscription_repo.get_one(requester_user.user_id)

    if vip_subscription is None:
        repository.auth_repo.update_user_role(requester_user.email, ROLE.GUEST)

        return False
    
    if vip_subscription.vip_level.value < required_vip_status.value:
        return False

    if vip_subscription.expired():
        repository.vip_subscription_repo.delete(requester_user.user_id)

        repository.auth_repo.update_user_role(requester_user.email, ROLE.GUEST)

        return False

    return True