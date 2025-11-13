from db.main import get_session 
from fastapi.exceptions import HTTPException 
from fastapi import APIRouter,status ,Depends
from services.book_service import BookService 
from typing import List
from models.book_model import Book
from schema.book_schema import Book,UpdateBookModel
from sqlalchemy.ext.asyncio.session import AsyncSession

book_router = APIRouter()
book_service = BookService()

@book_router.get("/",response_model=List[Book])
async def get_all_books(session:AsyncSession=Depends(get_session)): 
    books = await book_service.get_all_books()
    return books 


@book_router.post("/",status_code=status.HTTP_201_CREATED,response_model=Book)
async def create_a_book(book_data:Book): 
    new_book = await book_service.create_book(book_data:Book,session:AsyncSession=Depends(get_session))
    return new_book 

@book_router.get("/{book_id}",response_model=Book)
async def get_book(book_id:int): 
    book = await book_service.get_book(book_uid=book_id)
    if book:
       return book
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="book_not_found") 



@book_router.patch("/{book_id}")
async def update_book(
    book_id:int, 
    update_data:UpdateBookModel,
    session:AsyncSession=Depends(get_session)
):
    
    update_book = await book_service.update_book(book_id,update_data)
    
    
    if not update_book: 
        raise HTTPException(status=status.HTTP_404_NOT_FOUND,detail="book not found")
    
    return update_book
    

@book_router.delete("/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int):
    
    book_to_delete = await book_service.delete_book(book_id:int,session:AsyncSession=Depends(get_session))
    
    if book_to_delete: 
        return 
    else: 
        raise HTTPException(status=status.HTTP_404_NOT_FOUND,detail="Book Not Found")




    
    

    

    