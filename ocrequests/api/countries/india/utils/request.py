from typing import Dict

from requests import Session

from api.countries.india.consts.referer import Referer
from api.countries.india.utils.urls import get_current_url, get_referer_url
import logging


def send_post_request(
    session: Session,
    token: str,
    url: str,
    data: Dict,
    referer: Referer = Referer.Current,
    files: Dict = None,
):
    response = session.post(
        url=get_current_url(url),
        headers={"referer": get_referer_url(url, referer)},
        data={**data, "token": token},
        files=files,
    )

    logging.info(f"Sent request to {url}, returned status code: {response.status_code}")
    return response


def send_files_request(
    session: Session,
    token: str,
    url: str,
    data: Dict,
    file_field_name: str,
    file_path: str,
):
    file_name = file_path.split("\\")[-1]
    logging.info(f"Uploading file {file_name} to {url}")
    return send_post_request(
        session,
        token,
        url,
        data,
        Referer.Current,
        files={
            file_field_name: (
                file_name,
                open(file_path, "rb"),
                (
                    "application/pdf"
                    if file_name.split(".")[-1] == "pdf"
                    else "image/jpeg"
                ),
            )
        },
    )
