# Notif.ai zadanie rekrutacyjne

Powyższą aplikacją jest API służace do zapisywania, zwracania
zapisanych oraz edycji krótkich tekstów (do 160 znaków). 
 

aplikacja dostępna jest pod adresem https://daftcode-course.herokuapp.com/

dokumentacja automatyczna zapewniona przez framework FastAPI dostępna jest pod adresem https://daftcode-course.herokuapp.com/docs#/

Kilka słow o endpointach i ich działaniu:
## /get_text/{id} metoda: GET
endpoint służący do pobierania tekstów o podanym przez użytkownika ID, dostępny dla użytkowników wszystkich użytkowników (authorized i unauthorized)
zwraca obiekt w formacie:
```
{
    'id': int
    'visit_counter': int
    'text': str
}
```

## /put_text metoda: POST 
endpoint służący do utworzenia lub edycji (jeśli użytkownik poda ID, które już istnieje dany obiekt zostanie zedytowany) 
tekstów o podanym ID, wymaga autoryzacji. Wymaga pliku json w formacie:
```
{
    'id': int
    'text': str
}
```
## /delete_text/{id} metoda: DELETE
endpoint służący do usuwania tekstów o podanym ID, wymaga autoryzacji.

## /login metoda: GET
endopoint służacy do autoryzacji, dzięki niemu użytkownik będzie mógł 

## /get_text metoda: GET
endpoint zwraca wszystkie obiekty Text oraz ich ID z bazy danych

aplikacja została zdeployowana za pomocą heroku zgodnie z instrukcją z linku https://github.com/daftcode/daftacademy-python_levelup-spring2021/blob/master/1_D_jak_deploy/D_jak_Deploy.ipynb punkty 5 i 6
