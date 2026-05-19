import json
from typing import Any

import yaml
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(
    title="YAML JSON Converter API",
    version="1.0.0",
    description="A small FastAPI service for converting YAML to JSON and JSON to YAML.",
)


class ConversionRequest(BaseModel):
    content: str = Field(..., description="The input content to convert.")


class ConversionResponse(BaseModel):
    content: str = Field(..., description="The converted output content.")


@app.get("/ping")
def ping() -> dict[str, str]:
    return {"status": "ok"}


def yaml_to_python(content: str) -> Any:
    try:
        parsed = yaml.safe_load(content)
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML: {exc}") from exc

    return parsed


def json_to_python(content: str) -> Any:
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc.msg}") from exc

    return parsed


def python_to_json(data: Any) -> str:
    try:
        return json.dumps(data, indent=2, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Unable to serialize as JSON: {exc}") from exc


def python_to_yaml(data: Any) -> str:
    try:
        return yaml.safe_dump(
            data,
            sort_keys=False,
            allow_unicode=True,
            default_flow_style=False,
        )
    except yaml.YAMLError as exc:
        raise ValueError(f"Unable to serialize as YAML: {exc}") from exc


@app.post("/convert/yaml-to-json", response_model=ConversionResponse)
def convert_yaml_to_json(request: ConversionRequest) -> ConversionResponse:
    if not request.content.strip():
        raise HTTPException(status_code=400, detail="Content must not be empty.")

    try:
        parsed = yaml_to_python(request.content)
        converted = python_to_json(parsed)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return ConversionResponse(content=converted)


@app.post("/convert/json-to-yaml", response_model=ConversionResponse)
def convert_json_to_yaml(request: ConversionRequest) -> ConversionResponse:
    if not request.content.strip():
        raise HTTPException(status_code=400, detail="Content must not be empty.")

    try:
        parsed = json_to_python(request.content)
        converted = python_to_yaml(parsed)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return ConversionResponse(content=converted)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("converter:app", host="127.0.0.1", port=8000, reload=True, reload_dirs=["src"])
