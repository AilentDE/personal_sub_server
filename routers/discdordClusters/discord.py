from fastapi import APIRouter, status, HTTPException
from typing import Annotated
from config.database_mssql import get_db

router = APIRouter()