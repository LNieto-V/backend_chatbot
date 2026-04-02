"""IoT route — POST /iot endpoint."""

from fastapi import APIRouter

from app.controllers.iot_controller import handle_iot_data
from app.models.iot import IoTData, IoTResponse

router = APIRouter()


@router.post(
    "",
    response_model=IoTResponse,
    summary="Submit IoT sensor data",
    description=(
        "Validates and processes sensor readings (temperature, humidity, light) "
        "and returns an automated diagnosis with risk level assessment."
    ),
)
async def submit_iot_data(data: IoTData) -> IoTResponse:
    """Process IoT sensor readings."""
    return await handle_iot_data(data)
