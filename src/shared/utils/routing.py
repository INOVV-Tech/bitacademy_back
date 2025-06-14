from typing import Any

from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, Created, InternalServerError, BadRequest
from src.shared.helpers.errors.errors import MissingParameters, ForbiddenAction

from src.shared.infra.repositories.repository import Repository
from src.shared.infra.repositories.dtos.auth_authorizer_dto import AuthAuthorizerDTO

from src.shared.domain.enums.role import ROLE
from src.shared.domain.entities.vip_subscription import VipSubscription

DEFAULT_ALLOWED_USER_ROLES = [ ROLE.ADMIN ]

def controller_execute(
    Usecase: Any,
    request: IRequest,
    allowed_user_roles: list[ROLE] = DEFAULT_ALLOWED_USER_ROLES,
    fetch_vip_subscription: bool = True,
    return_created: bool = False
) -> IResponse:
    try:
        requester_user = request.data.get('requester_user')

        if requester_user is None:
            raise MissingParameters('requester_user')
        
        requester_user = AuthAuthorizerDTO.from_api_gateway(requester_user)

        if requester_user.role not in allowed_user_roles:
            raise ForbiddenAction('Acesso não autorizado')
        
        if fetch_vip_subscription:
            set_user_vip_subscription(requester_user)
        
        response = Usecase().execute(requester_user, request.data, request.query_params)

        if 'error' in response:
            return BadRequest(response['error'])
        
        if return_created:
            return Created(body=response)
        
        return OK(body=response)
    except MissingParameters as error:
        return BadRequest(error.message)
    except ForbiddenAction as error:
        return BadRequest(error.message)
    except:
        return InternalServerError('Erro interno de servidor')
    
def set_user_vip_subscription(requester_user: AuthAuthorizerDTO) -> None:
    if requester_user.role == ROLE.ADMIN:
        requester_user.vip_subscription = VipSubscription.max_vip_dummy(requester_user.user_id)
        return
    
    if requester_user.role == ROLE.TEACHER:
        requester_user.vip_subscription = VipSubscription.max_vip_dummy(requester_user.user_id)
        return
    
    if requester_user.role != ROLE.VIP:
        requester_user.vip_subscription = VipSubscription.free_dummy(requester_user.user_id)
        return

    repository = Repository(
        auth_repo=True,
        vip_subscription_repo=True
    )

    vip_subscription = repository.vip_subscription_repo.get_one(requester_user.user_id)

    if vip_subscription is None:
        repository.auth_repo.update_user_role(requester_user.email, ROLE.GUEST)
        requester_user.role = ROLE.GUEST

        requester_user.vip_subscription = VipSubscription.free_dummy(requester_user.user_id)
        return

    if vip_subscription.expired():
        repository.vip_subscription_repo.delete(requester_user.user_id)

        repository.auth_repo.update_user_role(requester_user.email, ROLE.GUEST)
        requester_user.role = ROLE.GUEST

        requester_user.vip_subscription = VipSubscription.free_dummy(requester_user.user_id)
        return
    
    requester_user.vip_subscription = vip_subscription