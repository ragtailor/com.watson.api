
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

walter_router = APIRouter(prefix="/titanic/james", tags=["james"])