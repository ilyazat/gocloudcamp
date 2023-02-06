from fastapi import APIRouter, status, HTTPException

from schemas.config import Config, ConfigToDB
from db import crud


router = APIRouter(prefix="/config")


def _check_config_existence(service: str):
    if not crud.get_config_by_service({"service": service}):
        raise HTTPException(status_code=404, detail=f"{service} wasn't found")

    return False


def _check_if_config_is_using_by(service: str):
    config = crud.get_config_by_service({"service": service})
    if config["used_by"]:
        return True
    return False


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_config(config: Config):
    if crud.get_config_by_service({"service": config.service}):
        raise HTTPException(status_code=400, detail=f"{config.service} already exists")

    config_to_db = ConfigToDB(service=config.service,
                              data=config.data,
                              version=1)
    crud.insert_config_into_collection(config_to_db)
    return {"detail": f"Config {config.service} successfully created"}


@router.get("", status_code=status.HTTP_200_OK)
async def get_config(service: str, version: int = None):
    _check_config_existence(service)
    filter_ = {"service": service}
    if version:
        filter_.update({"version": version})

    config = crud.get_config_by_service(filter_)
    if not config:
        raise HTTPException(status_code=404, detail="Config or version of the config wasn't found")

    return {key: value for d in config["data"] for key, value in d.items()}


@router.get("/all")
async def get_all():
    return crud.get_all()


@router.put("", status_code=status.HTTP_200_OK)
async def update_config(config: Config):
    _check_config_existence(config.service)
    crud.update_service(config)
    return {"detail": f"Config {config.service} successfully updated"}


@router.delete("", status_code=status.HTTP_200_OK)
async def delete_config(service: str):
    _check_config_existence(service)
    if _check_if_config_is_using_by(service):
        raise HTTPException(status_code=400, detail="The config can't be deleted. One of the app uses it")
    crud.delete_service({"service": service})
    return {"detail": f"Config {service} successfully deleted"}


@router.put("/add_app", status_code=status.HTTP_200_OK)
async def add_app(service: str, app_label: str):
    _check_config_existence(service)
    crud.add_app_to_config(service, app_label)
    return {"detail": f"The app {app_label} has been added to service {service} successfully"}


@router.put("remove_app", status_code=status.HTTP_200_OK)
async def remove_app(service: str, app_label: str):
    _check_config_existence(service)
    crud.remove_app_from_config(service, app_label)
    return {"detail": f"The app {app_label} has been removed from service {service} successfully"}
