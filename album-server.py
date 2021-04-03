from bottle import route, request,post
from bottle import run
from bottle import HTTPError
import json


from Web_server import album_main


# def save_artist(album_data):
#     year = album_data["year"]
#     artist = album_data["artist"]
#     genre = album_data["genre"]
#     album = album_data["album"]
#
#     filename = "{}-{}.json".format(artist, album)
#     with open(filename, "w") as fd:
#         json.dump(album_data, fd)
#     return filename

@route ("/albums/<artist>", method='GET')
def albums(artist):
    albums_list = album_main.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(400, message)
    else:
        albums_names = [album.album for album in albums_list]
        result_message = "Список альбомов\n {}:".format(albums_names)
        albums_names_count = len(albums_names)
        count_message = " Количество альбомов : \n{} ".format(albums_names_count)
        result_message += ", ".join(albums_names)
        # count_message  = "/n ".join(albums_names_count)
    return result_message, count_message


@route('/albums', method="POST")
def album_new():
    #словарь для добавления новой строки в БД
    album_data = {
        'year':request.forms.get('year'),
        'artist':request.forms.get('artist'),
        'genre':request.forms.get('genre'),
        'album':request.forms.get('album')
    }

     # получить список альбомов для введенного с формы артиста

    album_list_by_artist = album_main.find_album(album_data["artist"])
    # получить список альбомов исполнителя
    albums_names_by_artist = [album.album for album in album_list_by_artist]
    #для каждого альбома из списка проверить наличие в словаре album_data
    if album_data['album'] in albums_names_by_artist:
        message = "Альбом для введенного артиста {} уже существует".format(album_data['artist'])
        result = HTTPError(409, message)
    else:
        if not album_main.yearcheck(album_data['year']):
            message = "Неверный формат года"
            result = HTTPError(409,message)
        elif not album_main.valid_data(data=album_data):
            message = "Не все данные внесени. Заполните значения "
            result = HTTPError(409, message)
        else:
            album_main.save_artist(album_data)
            result ='Данные сохранены'

    return result


if __name__ =="__main__":
    run(host="localhost", port=8080, debug=True)





