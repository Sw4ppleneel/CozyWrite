from .. import schemas , Models , utils
from fastapi import Body, FastAPI, Response, status, HTTPException , Depends , APIRouter
from sqlalchemy.orm import Session 
from sqlalchemy import func
from ..database import get_db
from ..import oauth2
from typing import Optional

router = APIRouter()



#create a post
@router.post("/poststuff", status_code=status.HTTP_201_CREATED , response_model=schemas.Response)
def create_post(new_post: schemas.PostCreate, db : Session = Depends(get_db)
            ,user : int = Depends(oauth2.get_current_user)):

    # cursor.execute("""INSERT INTO posts("Title" , "Content" , "Published") VALUES 
    #                (%s , %s , %s) RETURNING * """ 
    #                , (new_post.Title , new_post.Content, new_post.Published))
    # posted = cursor.fetchone()
    # conn.commit()
    # posted = Models.Post(
    #     Title = new_post.Title , Content = new_post.Content 
    #     , Published = new_post.Published)
   
    posted = Models.Post(**(new_post.dict()), user_id=user.id)
    db.add(posted)
    db.commit()
    db.refresh(posted)
    return posted

# # get all posts
# @router.get("/getpostsall" , response_model=list[schemas.Response] )
@router.get("/getpostsall", response_model=list[schemas.PostOut])
def get_post_stuff(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # fetch posts + vote counts (returns list of (Post, votes))
    rows = (
        db.query(Models.Post, func.count(Models.votes.post_id).label("votes"))
        .join(Models.votes, Models.votes.post_id == Models.Post.id, isouter=True)
        .filter(Models.Post.Title.contains(search))   # if your ORM attr is 'title' change to Post.title
        .group_by(Models.Post.id)
        .limit(limit)
        .offset(skip)
        .all()
    )

    out = []
    for post, votes in rows:
        out.append({"post": post, "votes": votes})
    return out





# # find a specific post
# def find_post(id):
#     for post in my_data:
#         if post['id'] == id:
#             return post
#     return 0


# get a specific post
@router.get("/seepost/{id}", response_model=schemas.PostOut)
def see_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Models.Post).filter(Models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")

    votes = db.query(func.count(Models.votes.post_id)).filter(Models.votes.post_id == id).scalar() or 0

    return {"post": post, "votes": votes}

# # find post index
# def find_post_index(id):
#     for i, post in enumerate(my_data):
#         if post['id'] == id:
#             return i
#     return 0

# delete a specific post
@router.delete("/deletepost/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int , db : Session = Depends(get_db), user : int = Depends( oauth2.get_current_user)):

# #    cursor.execute(""" DELETE FROM posts WHERE "id" = %s RETURNING * """ , (str(id),))
# #    deleted_post = cursor.fetchone()
# #    conn.commit()
# #    if deleted_post is None:
# #        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")       
#    return {"Info": deleted_post}
    show_query = db.query(Models.Post).filter(Models.Post.id == id)
    show = show_query.first()
    if show == None :
        return(HTTPException(status_code=status.HTTP_404_NOT_FOUND))

    if show.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

    show_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update a specific post
@router.put("/updatepost/{id}")
def update_post(id: int, updated_post: schemas.Post , db : Session = Depends(get_db), user_id : int = Depends( oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET "Title" = %s , "Content" = %s , "Published" = %s 
    #                 WHERE "id" = %s RETURNING * """ 
    #                 , (updated_post.Title , updated_post.Content, updated_post.Published, str(id)))
    # updated = cursor.fetchone()
    # conn.commit()
    u_post = db.query(Models.Post).filter(Models.Post.id == id)
    updated = u_post.first()
    if updated is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    if updated.user_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    
    u_post.update(updated_post.dict(), synchronize_session = False)
    db.commit()
    return {"Info": u_post.first()}
