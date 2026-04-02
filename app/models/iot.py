"""IoT sensor data models."""

from pydantic import BaseModel, Field


class IoTData(BaseModel):
    """Sensor readings from IoT devices."""

    temperature: float = Field(
        ...,
        ge=-10.0,
        le=60.0,
        description="Temperature in Celsius (-10 to 60)",
    )
    humidity: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Relative humidity percentage (0 to 100)",
    )
    light: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Light level (0 to 100)",
    )


class IoTResponse(BaseModel):
    """Response after processing IoT sensor data."""

    status: str = Field(default="ok", description="Processing status")
    diagnosis: str = Field(..., description="Automated diagnosis based on sensor data")
    risk_level: str = Field(..., description="Risk level: low, medium, high")
