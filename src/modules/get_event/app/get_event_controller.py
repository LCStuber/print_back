from .get_event_usecase import GetEventUsecase
from .get_event_viewmodel import GetEventViewModel
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, NotFound, InternalServerError

class GetEventController:

    def __init__(self, usecase: GetEventUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            # Verifica se o parâmetro `event_id` foi fornecido
            if request.data.get('event_id') is None:
                raise MissingParameters("event_id")
            
            if type(request.data.get('event_id')) is not str:
                raise WrongTypeParameter("event_id", str, type(request.data.get('event_id')))
            
            # Obtém o evento pelo caso de uso
            event = self.usecase(request.data.get('event_id'))

            # Cria o ViewModel com os dados do evento
            viewmodel = GetEventViewModel(
                event_id=event.event_id,
                name=event.name,
                description=event.description,
                banner=event.banner,
                start_date=event.start_date,
                end_date=event.end_date,
                rooms=event.rooms,
                subscribers=event.subscribers
            )

            return OK(viewmodel.to_dict())

        except NoItemsFound as e:
            return NotFound(body=e.message)
        except MissingParameters as e:
            return BadRequest(body=e.message)
        except WrongTypeParameter as e:
            return BadRequest(body=e.message)
        except Exception as e:
            return InternalServerError(body=e.args[0])
