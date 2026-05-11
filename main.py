from starlette.status import HTTP_201_CREATED
from fastapi import FastAPI, Depends, HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
from database import Base, get_db, engine
import models
from schemas import PostCreate, PostResponse, UserCreate, UserResponse,Token
from sqlalchemy.orm import Session, joinedload
import utils
import auth
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt,JWTError

app = FastAPI(title="Blog API", description="A REST API for a blog application")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins, change this in production!
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)
Base.metadata.create_all(bind=engine)

oauth2schema = OAuth2PasswordBearer(tokenUrl="/api/login")

#authentication

@app.post("/api/register",response_model=UserResponse)
def user_register(user: UserCreate,db:Session = Depends(get_db)):
    """
    Register a new user. Checks if username or email already exists.
    """
    existing_user = db.query(models.User).filter(
        (models.User.email == user.email) | (models.User.username == user.username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Username or Email already exists')
    
    hashed_password = utils.hash_password(user.password)
    new_user = models.User(
        username = user.username,
        email = user.email,
        password = hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/login",response_model=Token)
def user_login(form_data: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    """
    Authenticate a user and return a JWT access token.
    """
    user = db.query(models.User).filter(models.User.username==form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credential",headers={'WWW-Authenticate':'Bearer'})
    if not utils.verify_password(form_data.password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid password',headers={'WWW-Authenticate':'Bearer'})
    
    access_token = auth.create_access_token(
        data ={
            "user_id": str(user.id),
            "email": user.email
        }
    )
    return {"access_token":access_token,"token_type":"bearer"}

def get_current_user(token: str = Depends(oauth2schema),db:Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credential",headers={'WWW-Authenticate':'Bearer'})
    try:
        payload = jwt.decode(token,auth.SECRET_KEY,algorithms=[auth.ALGORITHM])
        user_id = payload.get("user_id")
        email = payload.get("email")
        if user_id is None or email is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    
        
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise credential_exception
    
    return user

@app.post("/api/posts",response_model=PostResponse,status_code=status.HTTP_201_CREATED)
def create_post(post:PostCreate,db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    """
    Create a new blog post. The author will be the currently authenticated user.
    """
    new_post = models.Post(**post.model_dump(), author_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/api/posts",response_model=list[PostResponse])
def get_posts(db:Session = Depends(get_db), limit: int = 10, skip: int = 0):
    """
    Retrieve a paginated list of all blog posts, including their authors.
    """
    posts = db.query(models.Post).options(joinedload(models.Post.author)).offset(skip).limit(limit).all()
    return posts

@app.get("/api/posts/{post_id}",response_model=PostResponse)
def get_post(post_id: int, db:Session = Depends(get_db)):
    """
    Retrieve a single blog post by its ID.
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    return post

@app.put("/api/posts/{post_id}",response_model=PostResponse)
def update_post(post_id:int, post_update: PostCreate, db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    """
    Update an existing blog post. Only the author of the post can update it.
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    
    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not authorized to update this post")
    
    post.title = post_update.title
    post.content = post_update.content
    db.commit()
    db.refresh(post)
    return post

@app.delete("/api/posts/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    """
    Delete an existing blog post. Only the author of the post can delete it.
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    
    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not authorized to delete this post")
    db.delete(post)
    db.commit()

    return {"message":"Post deleted successfully"}