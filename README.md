# Notif.ai zadanie rekrutacyjne

aplikacja dostępna jest pod adresem https://daftcode-course.herokuapp.com/

dokumentacja automatyczna zapewniona przez framework FastAPI dostępna jest pod adresem https://daftcode-course.herokuapp.com/docs#/

Kilka słow o endpointach i ich działaniu:
## /get_text/{id} 
endpoint służący do pobierania tekstów o podanym przez użytkownika ID, dostępny dla użytkowników wszystkich użytkowników (authorized i unauthorized)
zwraca obiekt w formacie:
```
{
    'id': int
    'visit_counter': int
    'text': str
}
```

## /put_text 
endpoint służący do utworzenia lub edycji (jeśli użytkownik poda ID, które już istnieje dany obiekt zostanie zedytowany) 
tekstów o podanym ID, wymaga autoryzacji. Wymaga pliku json w formacie:
```
{
    'id': int
    'text': str
}
```
## /delete_text/{id} 
endpoint służący do usuwania tekstów o podanym ID, wymaga autoryzacji.

## /login
endopoint służacy do autoryzacji, dzięki niemu użytkownik będzie mógł 

## /get_text 
endpoint zwraca wszystkie obiekty Text oraz ich ID z bazy danych
