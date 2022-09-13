from fastapi import APIRouter, Depends, Request, Form
from fastapi import __version__ as fastapi_version
from fastapi import responses
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import select, or_, func
from database import Movie, MovieIn, User, get_db
from typing import List

j2_templates = Jinja2Templates(directory="templates")
render = j2_templates.TemplateResponse
rick_rolled = RequestValidationError(
    errors=[
        {
            "loc": ("path", "any"),
            "msg": "You've been rick rolled!",
            "reason": "No reason.",
        }
    ],
)
router = APIRouter(tags=["api"])


@router.get("/", response_class=responses.HTMLResponse)
async def get_all_users(request: Request, db: Session = Depends(get_db)):
    all_users = db.query(User).all()
    return render("users.html", {"request": request, "users": all_users})


@router.get("/movies/{user_id}", response_class=responses.HTMLResponse)
async def get_movies(request: Request, user_id: int, db: Session = Depends(get_db)):
    if not (user := db.query(User).filter(User.id == user_id).first()):
        raise rick_rolled
    return render("movies.html", {"request": request, "user": user})


@router.post("/add-movie/{user_id}", response_class=responses.HTMLResponse)
async def add_movie(request: Request, user_id: int, db: Session = Depends(get_db)):
    if not (user := db.query(User).filter(User.id == user_id).first()):
        raise rick_rolled
    user: User
    form = (await request.form())._dict
    validated_movie = MovieIn(**form)
    movie_in_db = Movie(owner_id=user.id, **validated_movie.dict())
    db.add(movie_in_db)
    db.commit()
    return render("movies.html", {"request": request, "user": user})


@router.post("/edit-movie/{movie_id}", response_class=responses.HTMLResponse)
async def add_movie(request: Request, movie_id: int, db: Session = Depends(get_db)):
    if not (movie := db.query(Movie).filter(Movie.id == movie_id).first()):
        raise rick_rolled
    movie: Movie
    form = (await request.form())._dict
    validated_movie = MovieIn(**form)
    movie.title = validated_movie.title
    movie.genre = validated_movie.genre
    movie.trailer = validated_movie.trailer
    movie.year = validated_movie.year
    db.commit()
    return render(
        "search.html",
        {"request": request, "result": [movie]},
    )


@router.get("/status", response_class=responses.HTMLResponse)
async def status(request: Request):
    return render("status.html", {"request": request, "fa": fastapi_version})


@router.post("/search", response_class=responses.HTMLResponse)
async def search(
    request: Request,
    search: str = Form(default=""),
    db: Session = Depends(get_db),
):
    stmt = select(Movie).where(
        or_(
            Movie.title.contains(search.lower()),
            Movie.genre.contains(search.lower()),
        )
    )
    return render(
        "search.html",
        {"request": request, "result": db.scalars(stmt).all(), "search_term": search},
    )
