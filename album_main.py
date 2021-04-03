import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime


DB_PATH = "sqlite:///albums.sqlite3"

Base = declarative_base()

class Album(Base):
    #Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    __tablename__= 'album'
    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER, nullable=False)
    artist = sa.Column(sa.TEXT, nullable=False)
    genre = sa.Column(sa.TEXT, nullable=False)
    album = sa.Column(sa.TEXT,nullable=False)


def connect_db():
     # Создаю сессию
     engine = create_engine(DB_PATH)
     Base.metadata.create_all(engine)
     session = sessionmaker(engine)
     return session()

def find(artist):
 #Находит все альбомы в базе данных по заданному артисту
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    # for row in albums:
    #     print("ID:", row.id, "Year: ",row.year, "Artist:",row.artist, "album:",row.album)
    return albums
#
def find_album(artist):
 # Проверяет артиста по альбому
    session = connect_db()
    album_by_artist = session.query(Album).filter(Album.artist ==artist).all()
    return album_by_artist

def save_artist(album_data):
    add_album = Album()
    add_album.year = album_data['year']
    add_album.artist = album_data['artist']
    add_album.genre = album_data['genre']
    add_album.album = album_data['album']
    result = "Данные сохранены в БД!"
    session = connect_db()
    session.add(add_album)
    # сохраняем все изменения, накопленные в сессии
    session.commit()
    print("Спасибо, данные сохранены!")
    session.close()
    return result
#     with open(filename, "w") as fd:
#         json.dump(user_data, fd)

#Валидация года согласно формату
# def yearcheck(year):
#     # Год  - 4 символ
#      if len(year)!= 4:
#         raise InvalidLenght ("Некорректный формат года. Количество символов не менее 4-х")
#      elif year.isdigit()==False: #Год только цифры
#         raise InvalidFormat ("Некорректный формат года. Значение должно содержать только цифры")
#      return True

#Валидация года согласно формату
def yearcheck(year):
    if year.isdigit():
        if len(year) != 4:
            return False
        elif int(year) > 1800 and int (year) < 2022:
            return True
    else:
        return False

#Валидация обязательности ввода всех значений
def valid_data(data):
    if data['year'] and data['artist'] and data['genre'] and data['album']:
        return True
    else:
        raise NotNullData("Поля : year, artist, genre, album - обязательны для заполнения! ")


#Валидация года только на числа
class InvalidFormat(Exception):
    pass

#Валидация года  на длину
class InvalidLenght(Exception):
    pass

#валидация обязательности
class NotNullData(Exception):
    pass
