from fastapi import HTTPException, APIRouter, UploadFile, File, Form, Depends
from database import DatabasePool
from pydantic import BaseModel
from typing import Optional, List
import os
import aiofiles
from fastapi.staticfiles import StaticFiles


def create_router(database_pool: DatabasePool):  
    router = APIRouter()
    @router.get("/menu")
    async def get_items():  
       connection = None
       try:
            connection = await database_pool.get_connection()  # Get a fresh one
            async with connection.cursor() as cursor:
               query = """
                SELECT * FROM Menu_Items_New_SS
                """
               print(f"Executing Query: {query}")  # Debugging print
               await cursor.execute(query)
               result = await cursor.fetchall()
               if not result:
                   print(f"No category found")  # Log the failure
                   raise HTTPException(status_code=404, detail="No category Found")
   
               inventory_list = [
                   {
                       "id": row[0],
                       "title": row[1],
                       "category": row[2],
                       "about": row[3],
                       "extra_cost": row[4],
                       "profit": row[5],
                       "total_amount": row[6],
                       "image": row[7],
                       "kitchen": row[8],
                       "status": row[9],
                   }
                   for row in result
               ]
               return inventory_list
   
       except Exception as ex:
           raise HTTPException(status_code=500, detail=f"An error occurred: {ex}")
   
       finally:
            if connection:
                await database_pool.release_connection(connection)
    
    
    
    return router
