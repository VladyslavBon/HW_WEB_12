import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.database.db import get_db
from src.routes import contacts, auth

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello World'}

@app.get('api/healthcheacker')
def healthcheacker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text('SELECT 1')).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail='Database is not configured correctly')
        return {'message': 'Welcome to FastAPI!'}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Error connecting to the database')
    
app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)