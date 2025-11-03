from fastapi import Body, FastAPI, Response, status, HTTPException , Depends , APIRouter
from .. import schemas
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2
from .. import Models

router = APIRouter(prefix= "/vote" ,tags=["votes"])

@router.post("/")
def vote(vote : schemas.Votes , db : Session = Depends(get_db) ,
          current_user : int = Depends(oauth2.get_current_user)) :
    vote_query = db.query(Models.votes).filter(Models.votes.post_id == vote.post_id , 
                                   Models.votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1 :
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT
                                , detail= f" User {current_user.id} has already upvoted!!")
        new_vote = Models.votes(post_id = vote.post_id , user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"messege" : "Sucesfully added vote" }
    
    else :
        if not found_vote :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= "No vote")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"messege" : "vote removed"}



