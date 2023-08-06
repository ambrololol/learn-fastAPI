
from .. import models, schemas, oauth2
from typing import List
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
# use double . to get 1 level above from the current directory

# declare a file as a router
# as we set a file as a router, @app doesn't valid anymore. we change it to @router
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
) 

# ================================================================================================
# Grabbing all posts inside database using SQL Alchemy
@router.get("/", response_model=List[schemas.Post])
def test_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # to connect to database 
    
    posts = db.query(models.Post).all() # db, query with the model of Post, all() means to grab all data
    return posts

# Taking all posts inside database 
# @router.get("/posts", response_model=List[schemas.Post])
# def get_posts():
#     cursor.execute("""SELECT * FROM posts """) # triple quotes to make an SQL
#     posts = cursor.fetchall() # variable posts fetch everything inside database
#     print(posts)
#     return posts

# ================================================================================================
# Making a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post_dict = post.dict()
    # Generates random number for 'ID' when making a post
    # post_dict['id'] = randrange (0, 1000000)
    # my_post.append(post_dict)
    
    # set the values by order //
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit() # conn.commit needed if there will be any changes in the database

    # print(current_user)
    new_post = models.Post(owner_id=current_user.id, **post.dict()) 
    db.add(new_post) # db.add() to add the inserted post to current new post 
    db.commit() # same as conn.commit()
    db.refresh(new_post) # same as RETURNING *
    return new_post 

# ================================================================================================
# Taking one post exists. if not exists, sends error.
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, str((id))) # str(id) bcs of expected input of id as an integer, but as string inside the database
    # post = cursor.fetchone()
    #post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
        # Another way to do it 
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"post with id: {id} was not found"}
    return post

# ================================================================================================
# deleting a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", str((id))) # str(id) bcs of expected input of id as an integer, but as string inside the database
    # deleted_post = cursor.fetchone()
    # conn.commit()

    # find the index in the array that has required id
    #index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")

    # make an selection where only the owner of the post can delete the post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform requested action")

    # my_post.pop(index)
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# ================================================================================================
# updating a post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # find the index in the array that has required id
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id) # set up a query with the specific id
    # grab that specific post, if it doesnt exist, sends 404. 
    post = post_query.first() 
    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform requested action")

    # if it exists, we can update using update method in the field we wanna update.
    post_query.update(updated_post.dict(), synchronize_session=False) 
    db.commit()
    

    return post_query.first()