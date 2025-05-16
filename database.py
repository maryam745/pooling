import asyncmy
from asyncmy.pool import Pool
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabasePool:
    def __init__(self):
        self.pool: Pool | None = None

    async def initialize(self):
        try:
            self.pool = await asyncmy.create_pool(
                host="srv865.hstgr.io",
                user="u441049818_360_Bistro",
                password="FlexWave@193708",
                db="u441049818_360_Bistro",
                port=3306,
                autocommit=True,
                minsize=5, 
                maxsize=20, 
                pool_recycle=1800, 
            )
            logging.info(f"Database pool initialized. Min: 5, Max: 20 connections")
        except Exception as e:
            logging.error(f"Failed to initialize database pool: {e}")

    async def get_connection(self):
        if not self.pool:
            logging.critical("Database pool is not initialized!")
            logging.debug(f"Connection acquired. Active connections: {self.pool.size}, Free: {self.pool.freesize}")

            raise Exception("Database pool is not initialized.")
        
        try:
            connection = await self.pool.acquire()
            logging.debug(f"Connection acquired. Active connections: {self.pool.size}, Free: {self.pool.freesize}")
            return connection
        except Exception as e:
            logging.error(f"Failed to acquire connection: {e}")
            raise

    async def release_connection(self, connection):
       if connection:
         try:
            await self.pool.release(connection)  # Proper way to return connection to pool
            logging.debug(f"Connection released. Active: {self.pool.size}, Free: {self.pool.freesize}")
         except Exception as e:
            logging.warning(f"Error while releasing connection: {e}")

    async def close(self):
        if self.pool:
            try:
                await self.pool.close()
                logging.info("Database pool closed.")
            except Exception as e:
                logging.error(f"Error while closing database pool: {e}")
