#!/bin/bash

cd fastapi_app


alembic upgrade head

uvicorn src.main:app --reload --host 0.0.0.0
