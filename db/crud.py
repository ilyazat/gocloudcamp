from typing import Optional

from schemas.config import Config, ConfigToDB
from db.db import collection


def insert_config_into_collection(config_to_db: Config) -> None:
    item_ = ConfigToDB(**dict(config_to_db))
    collection.insert_one(dict(item_))


def get_config_by_service(item: dict) -> Optional[dict]:
    if item.get("version"):
        config_from_db = collection.find_one(item, {"_id": 0})
    else:
        pipeline = [
            {"$match": item},
            {"$sort": {"version": -1}},
            # {"$limit": 1},
            {"$project": {"_id": 0}}
        ]
        res = list(collection.aggregate(pipeline))
        config_from_db = res[0] if res else None
    return config_from_db


def delete_service(filter_: dict) -> None:
    """
    Deletes last version of the config
    filter_ should look like this `{"service": service_name}`
    """
    version = get_config_by_service(filter_)["version"]
    filter_.update({"version": version})
    collection.delete_one(filter_)


def update_service(config: Config) -> None:
    config_from_db = get_config_by_service({"service": config.service})
    config_from_db["version"] += 1
    version = config_from_db["version"]
    config_to_db = ConfigToDB(**dict(config), version=version)
    collection.insert_one(dict(config_to_db))


def get_all():
    return list(collection.find({}, {"_id": 0}))


def add_app_to_config(service: str, app_label: str) -> None:
    """
    filter_ == {"service": service_name, "app_label: app_label}
    """

    config = get_config_by_service({"service": service})
    used_by = config["used_by"].append(app_label) if config["used_by"] else [app_label]

    collection.update_one({"service": service, "version": config["version"]}, {"$set": {"used_by": used_by}})


def remove_app_from_config(service: str, app_label: str) -> None:
    config = get_config_by_service({"service": service})
    used_by = config["used_by"].remove(app_label)
    collection.update_one({"service": service, "version": config["version"]}, {"$set": {"used_by": used_by}})
