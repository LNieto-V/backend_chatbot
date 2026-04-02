"""IoT controller — orchestrates IoT data processing."""

from app.models.iot import IoTData, IoTResponse


async def handle_iot_data(data: IoTData) -> IoTResponse:
    """Process incoming IoT sensor data and generate a diagnosis.

    Args:
        data: Validated sensor readings.

    Returns:
        IoTResponse with diagnosis and risk level.
    """
    diagnosis_parts = []
    risk_level = "low"

    # Temperature analysis
    if data.temperature >= 35:
        diagnosis_parts.append(
            f"Temperatura crítica ({data.temperature}°C): estrés térmico"
        )
        risk_level = "high"
    elif data.temperature > 30:
        diagnosis_parts.append(
            f"Temperatura elevada ({data.temperature}°C): monitoreo recomendado"
        )
        risk_level = max(risk_level, "medium", key=_risk_priority)
    elif data.temperature < 15:
        diagnosis_parts.append(
            f"Temperatura baja ({data.temperature}°C): crecimiento lento"
        )
        risk_level = max(risk_level, "medium", key=_risk_priority)
    else:
        diagnosis_parts.append(f"Temperatura normal ({data.temperature}°C)")

    # Humidity analysis
    if data.humidity < 30:
        diagnosis_parts.append(f"Humedad crítica ({data.humidity}%): sequedad severa")
        risk_level = "high"
    elif data.humidity < 40:
        diagnosis_parts.append(f"Humedad baja ({data.humidity}%): riego recomendado")
        risk_level = max(risk_level, "medium", key=_risk_priority)
    elif data.humidity > 80:
        diagnosis_parts.append(f"Humedad excesiva ({data.humidity}%): riesgo de hongos")
        risk_level = max(risk_level, "medium", key=_risk_priority)
    else:
        diagnosis_parts.append(f"Humedad normal ({data.humidity}%)")

    # Light analysis
    if data.light > 85:
        diagnosis_parts.append(f"Luz excesiva ({data.light}): radiación alta")
        risk_level = max(risk_level, "medium", key=_risk_priority)
    elif data.light < 40:
        diagnosis_parts.append(f"Luz insuficiente ({data.light}): deficiencia lumínica")
        risk_level = max(risk_level, "medium", key=_risk_priority)
    else:
        diagnosis_parts.append(f"Luz adecuada ({data.light})")

    # Combined risk: high temp + low humidity
    if data.temperature > 30 and data.humidity < 40:
        diagnosis_parts.append("⚠️ Combinación crítica: estrés hídrico detectado")
        risk_level = "high"

    diagnosis = ". ".join(diagnosis_parts)

    return IoTResponse(
        status="ok",
        diagnosis=diagnosis,
        risk_level=risk_level,
    )


def _risk_priority(level: str) -> int:
    """Return numeric priority for risk level comparison."""
    return {"low": 0, "medium": 1, "high": 2}.get(level, 0)
