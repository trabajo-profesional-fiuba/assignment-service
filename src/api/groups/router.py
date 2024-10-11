from typing_extensions import Annotated
from fastapi import (
    APIRouter,
    Depends,
    Response,
    UploadFile,
    status,
    Query,
    BackgroundTasks,
)
from sqlalchemy.orm import Session

from src.api.auth.jwt import InvalidJwt, JwtResolver, get_jwt_resolver
from src.api.auth.schemas import oauth2_scheme
from src.api.auth.service import AuthenticationService
from src.api.exceptions import EntityNotInserted, EntityNotFound, ServerError

from src.api.groups.dependencies import get_email_sender
from src.api.groups.mapper import GroupMapper
from src.api.groups.repository import GroupRepository
from src.api.groups.schemas import (
    AssignedGroupConfirmationRequest,
    BlobDetailsList,
    GroupList,
    GroupResponse,
    GroupStates,
    GroupCompleteList,
    GroupWithTutorTopicRequest,
)
from src.api.groups.service import GroupService


from src.api.topics.repository import TopicRepository
from src.api.topics.service import TopicService
from src.api.tutors.mapper import TutorMapper
from src.api.tutors.repository import TutorRepository
from src.api.tutors.service import TutorService
from src.api.users.exceptions import InvalidCredentials

from src.api.utils.response_builder import ResponseBuilder
from src.core.azure_container_client import AzureContainerClient
from src.config.config import api_config
from src.config.database.database import get_db

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.post(
    "/",
    response_model=GroupResponse,
    summary="Creates a new group",
    description="""This endpoint creates a new group. The group can already have \
    tutor and topic or just preferred topics.""",
    responses={
        status.HTTP_201_CREATED: {"description": "Successfully added a new group."},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request due unknown operation"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Some information provided is not in db"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Input validation has failed, typically resulting in a \
            client-facing error response."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error - Something happened inside the \
            backend"
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_group(
    group: GroupWithTutorTopicRequest,
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    period=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_student_role(token)

        tutor_service = TutorService(TutorRepository(session))
        topic_service = TopicService(TopicRepository(session))
        group_service = GroupService(GroupRepository(session))

        tutor_period = tutor_service.get_tutor_period_by_tutor_email(
            period, group.tutor_email
        )
        topic = topic_service.get_or_add_topic(group.topic)

        res = GroupResponse.model_validate(
            group_service.create_assigned_group(
                group.students_ids, tutor_period.id, topic.id, period_id=period
            )
        )

        return ResponseBuilder.build_clear_cache_response(res, status.HTTP_201_CREATED)
    except (EntityNotInserted, EntityNotFound) as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(message=str(e))


@router.post(
    "/{group_id}/initial-project",
    description="Uploads a file into storage",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Students were created"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {"description": "Invalid file type"},
    },
)
async def post_initial_project(
    group_id: int,
    file: UploadFile,
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    background_tasks: BackgroundTasks,
    email_sender: Annotated[object, Depends(get_email_sender)],
    project_title: str = Query(...),
):
    try:

        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_student_role(token)

        container_name = api_config.container
        access_key = api_config.storage_access_key
        az_client = AzureContainerClient(
            container=container_name, access_key=access_key
        )
        content_as_bytes = await file.read()
        group_mapper = GroupMapper(tutor_mapper=TutorMapper())
        group_service = GroupService(GroupRepository(session))
        group_service.upload_initial_project(
            group_id, project_title, content_as_bytes, az_client
        )

        group = group_mapper.convert_from_model_to_group(
            group_service.get_group_by_id(group_id, True, True)
        )
        background_tasks.add_task(
            email_sender.notify_attachement, group, "Anteproyecto"
        )

        return "File uploaded successfully"
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except EntityNotFound as e:
        raise e
    except Exception as e:
        raise ServerError(message=str(e))


@router.post(
    "/{group_id}/final-project",
    description="Uploads a file into storage",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Students were created"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {"description": "Invalid file type"},
    },
)
async def post_final_project(
    group_id: int,
    file: UploadFile,
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    project_title: str = Query(...),
):
    try:

        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_student_role(token)

        container_name = api_config.container
        access_key = api_config.storage_access_key
        az_client = AzureContainerClient(
            container=container_name, access_key=access_key
        )
        content_as_bytes = await file.read()
        group_service = GroupService(GroupRepository(session))
        group_service.upload_final_project(
            group_id, project_title, content_as_bytes, az_client
        )
        return "File uploaded successfully"
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except EntityNotFound as e:
        raise e
    except Exception as e:
        raise ServerError(message=str(e))


@router.get(
    "/",
    response_model=GroupCompleteList,
    summary="Returns the list of groups that are in a specific period",
    responses={
        status.HTTP_200_OK: {"description": "Successfully added a new group."},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request due unknown operation"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Some information provided is not in db"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error - Something happened inside the \
            backend"
        },
    },
    status_code=status.HTTP_200_OK,
)
async def get_groups(
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    load_topic: bool = True,
    load_tutor_period: bool = False,
    load_period: bool = False,
    load_students: bool = True,
    period=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)

        group_service = GroupService(GroupRepository(session))

        res = GroupCompleteList.model_validate(
            group_service.get_groups(
                period, load_topic, load_tutor_period, load_period, load_students
            )
        )

        return ResponseBuilder.build_private_cache_response(res)
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(message=str(e))


@router.get(
    "/states/{group_id}",
    response_model=GroupStates,
    summary="Returns states of a group",
    responses={
        status.HTTP_200_OK: {"description": "Successfully returned states"},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request due unknown operation"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Some information provided is not in db"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error - Something happened inside the \
            backend"
        },
    },
    status_code=status.HTTP_200_OK,
)
async def get_group_by_id(
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    group_id: int,
):
    try:
        group_service = GroupService(GroupRepository(session))
        auth_service = AuthenticationService(jwt_resolver)

        is_student = auth_service.is_student(token)
        if is_student:
            jwt_token = auth_service.assert_student_role(token)
            student_id = auth_service.get_user_id(jwt_token)

            group = group_service.get_group_by_student_id(student_id)

            if group.id != group_id:
                raise InvalidJwt("Group requested is different to de student's group")
        else:
            group = group_service.get_group_by_id(group_id)

        group_model = GroupStates.model_validate(group)

        return ResponseBuilder.build_private_cache_response(group_model)
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except EntityNotFound as e:
        raise e
    except Exception as e:
        raise ServerError(message=str(e))


@router.get(
    "/{group_id}/initial-project",
    description="Downloads the file for a group in an specific period",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Success"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Server Error"},
    },
)
async def download_group_initial_project(
    group_id: int,
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    period=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    try:

        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_tutor_rol(token)

        container_name = api_config.container
        access_key = api_config.storage_access_key
        az_client = AzureContainerClient(
            container=container_name, access_key=access_key
        )

        group_service = GroupService(GroupRepository(session))
        bytes = group_service.download_initial_project(period, group_id, az_client)

        response = Response(
            content=bytes, status_code=status.HTTP_200_OK, media_type="application/pdf"
        )
        response.headers["Content-Disposition"] = (
            "attachment; filename=initial_project.pdf"
        )
        return response
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(message=str(e))


@router.get(
    "/initial-project",
    description="Gets all the initial projects metadata from a period",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Success"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Server Error"},
    },
)
async def list_initial_projects(
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    period=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    try:

        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_only_admin(token)

        container_name = api_config.container
        access_key = api_config.storage_access_key
        az_client = AzureContainerClient(
            container=container_name, access_key=access_key
        )

        group_service = GroupService(GroupRepository(session))
        blobs = group_service.list_initial_project(period, az_client)

        return BlobDetailsList.model_validate(blobs)

    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except EntityNotFound as e:
        raise e
    except Exception as e:
        raise ServerError(message=str(e))


@router.put(
    "/",
    response_model=GroupList,
    summary="Update a list of groups",
    description="""This endpoint updates the associated tutor period and topic to a \
                    list of groups """,
    responses={
        status.HTTP_201_CREATED: {"description": "Successfully updated group"},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request due unknown operation"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Some information provided is not in db"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Input validation has failed, typically resulting in a \
            client-facing error response."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error - Something happened inside the \
            backend"
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def update_groups(
    groups: list[AssignedGroupConfirmationRequest],
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_resolver: Annotated[JwtResolver, Depends(get_jwt_resolver)],
    period=Query(pattern="^[1|2]C20[0-9]{2}$", examples=["1C2024"]),
):
    try:
        auth_service = AuthenticationService(jwt_resolver)
        auth_service.assert_tutor_rol(token)

        group_service = GroupService(GroupRepository(session))
        groups_updated = group_service.update(groups, period)

        res = GroupList.model_validate(groups_updated)

        return ResponseBuilder.build_clear_cache_response(res, status.HTTP_201_CREATED)
    except (EntityNotInserted, EntityNotFound) as e:
        raise e
    except InvalidJwt:
        raise InvalidCredentials("Invalid Authorization")
    except Exception as e:
        raise ServerError(message=str(e))
