from src.crud.crud import SqlalchemyRepository, BooksCrud
from src.models.models import *
from src.database.database import session

author_dict = {
    "id": "7f1593d4-c5d5-4e25-b98d-04772841bd22",
    "name_author": "test_author"
}
genre_dict = {
    "id": "175bc87c-ed73-4931-abaa-6244bb11409b",
    "name_genre": "test_genre"
}

book_dict = {
    "id": "75f411cf-fde2-4c5d-9a25-1f4ad846b26d",
    "title":"test_book",
    "author_id": author_dict["id"],
    "genre_id": genre_dict["id"],
}

author_repository = SqlalchemyRepository(session=session, model=Author)
genre_repository = SqlalchemyRepository(session=session, model=Genre)
book_repository = SqlalchemyRepository(session=session, model=Book)
book_rep = BooksCrud(session=session,model=Book)
# author_repository.add(id="7f1593d4-c5d5-4e25-b98d-04772841bd22",
#                       name_author="test_author")
# genre_repository.add(id=genre_dict["id"], 
#                      name_genre=genre_dict["name_genre"])
# book_repository.add(id=book_dict["id"],
#                     title=book_dict["title"],
#                     author_id=book_dict["author_id"],
#                     genre_id=book_dict["genre_id"])
print([[i.id, i.title, i.author.name_author, i.genre.name_genre] for i in book_repository.get()])
print([[i.id, i.title, i.author, i.genre] for i in book_rep.get()])