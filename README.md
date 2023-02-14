# psql
создание таблицы пример
```
CREATE TABLE имя-таблицы ( имя-столбца serial );
```

Эта команда эквивалентна следующей группе команд:
```
CREATE SEQUENCE имя-таблицы_имя-столбца_seq;
CREATE TABLE имя-таблицы
(имя-столбца integer NOT NULL
DEFAULT nextval( 'имя-таблицы_имя-столбца_seq' ));
ALTER SEQUENCE имя-таблицы_имя-столбца_seq
OWNED BY имя-таблицы.имя-столбца;
```

Создание таблицы с foreign key пример
```
CREATE TABLE seats
(aircraft_codechar( 3 )NOT NULL,
seat_no varchar( 4 ) NOT NULL,
fare_conditions varchar( 10 ) NOT NULL,
CHECK( fare_conditions IN ( 'Economy', 'Comfort', 'Business' )),
PRIMARY KEY ( aircraft_code, seat_no ),
FOREIGN KEY ( aircraft_code )
REFERENCES aircrafts (aircraft_code )
ON DELETE CASCADE);
```

Пример добавления данных в бд (если применять к таблице выше убедись что fk '123' существует в таблицу aircrafts)
```
INSERT INTO seats VALUES ( '123', '1A', 'Business' );
```
Пример выборки с агрегациией и сортировкой
```
SELECT aircraft_code, count( * ) FROM seats
GROUP BY aircraft_code
ORDER BY count;
```

Пример создания таблицы с массивом
```
CREATE TABLE pilots
(pilot_name text, schedule integer[]);
```

Пример записи данных в поле с массивом
```
INSERT INTO pilots
VALUES ( 'Ivan', '{ 1, 3, 5, 6, 7 }'::integer[] ),
( 'Petr', '{ 1, 2, 5, 7}'::integer[] );
```

Пример конкатинации c массивом
```
UPDATE pilots
SET schedule = schedule || 7
WHERE pilot_name = 'Boris';
```

Пример работы с срезами

```
UPDATE pilots
SET schedule[ 1:2 ] = ARRAY[ 2, 3 ]
WHERE pilot_name = 'Petr';
```

Пример проверки если левое множество содержит все элементы правого
```
SELECT * FROM pilots
WHERE schedule @> '{ 1, 7 }'::integer[];
```

Пример запроса на проверку если левый массив не содержит значения из правого 
```
SELECT * FROM pilots
WHERE NOT ( schedule && ARRAY[ 2, 5 ] );
```
Пример вставки в таблицу с json
```
INSERT INTO pilot_hobbies
VALUES ( 'Ivan','{ "sports": [ "футбол", "плавание" ],"home_lib": true, "trips": 3}'::jsonb);
```
пример выборки поля где один из ключей json содержит значение
```
SELECT * FROM pilot_hobbies
WHERE hobbies @> '{ "sports": [ "футбол" ] }'::jsonb;
```
что аналогично
```
SELECT pilot_name, hobbies->'sports' AS sports
FROM pilot_hobbies
WHERE hobbies->'sports' @> '[ "футбол" ]'::jsonb;
```
Пример на наличие ключа в json
```
SELECT count( * )
FROM pilot_hobbies
WHERE hobbies ? 'sport';
```
Пример добавления значения в массив jsonа по ключю
```
UPDATE pilot_hobbies
SET hobbies = jsonb_set( hobbies, '{ sports, 1 }', '"футбол"' )
WHERE pilot_name = 'Boris';
```
Пример создания таблицы с уникальыми ключами, ограничениями, обрати внимание что ограничения могут объявлятся двумя видами (во время объявления поля либо после в отдельной строке (так называемой форме ограничения уровня таблицы.))
```
CREATE TABLE progress
(
record_book numeric( 5 ) PRIMARY KEY,
term numeric( 1 ) CHECK ( term = 1 OR term = 2 ),
mark numeric( 1 ) DEFAULT 5,
doc_ser numeric( 4 ),
doc_num numeric( 6 ),
CONSTRAINT unique_passport UNIQUE ( doc_ser, doc_num ),
CONSTRAINT valid_mark CHECK ( mark >= 3 AND mark <= 5 ),
);
```

Пример объявления составного primery key
```
PRIMARY KEY ( имя-столбца1, имя-столбца2, ...)
```
Три экваволентных примера создания таблиц с foreign key
```
CREATE TABLE progress
( record_book numeric( 5 ) REFERENCES students(record_book),);
```
```
CREATE TABLE progress
( record_book numeric( 5 ) REFERENCES students,);
```
```
CREATE TABLE progress
( record_book numeric( 5 ),
FOREIGN KEY ( record_book )
REFERENCES students ( record_book )
);
```
Пример установки комментария (описания к колонке)
```
COMMENT ON COLUMN airports.city IS 'Город';
```
Пример установки ограничения на установленные варианты

```
CHECK ( status IN ( 'On Time', 'Delayed', 'Departed','Arrived', 'Scheduled', 'Cancelled' )
```
вместо Serial можно указать type integer но в default указать
```
DEFAULT nextval('flights_flight_id_seq'::regclass)
```
Пример установки\удаления ограничений уже в существующую таблицу
```
ALTER TABLE airports
ALTER TABLE aircrafts ALTER COLUMN speed SET NOT NULL;
ALTER TABLE aircrafts ADD CHECK( speed >= 300 );

ALTER TABLE aircrafts ALTER COLUMN speed DROP NOT NULL;
ALTER TABLE aircrafts DROP CONSTRAINT aircrafts_speed_check;
```
Пример изменения типа данных столбца
```
ALTER TABLE airports
ALTER COLUMN latitude SET DATA TYPE numeric( 5,2 );
```
Пример удаления ограничения и изменения типа данный с строкового на числовой.
```
ALTER TABLE seats
DROP CONSTRAINT seats_fare_conditions_check,
ALTER COLUMN fare_conditions SET DATA TYPE integer
USING ( CASE WHEN fare_conditions = 'Economy' THEN 1
WHEN fare_conditions = 'Business' THEN 2
ELSE 3 END
);
```
Пример создания материализованного представления (сохраняет данные внутри, в отличии от обычных view)
```
CREATE MATERIALIZED VIEW [ IF NOT EXISTS ] имя-мат-представления
[ ( имя-столбца [, ...] ) ]
AS запрос
[ WITH [ NO ] DATA ];
```