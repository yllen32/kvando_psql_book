from pymongo import MongoClient

# Подключение к MongoDB серверу
client = MongoClient("mongodb://localhost:27017/")

# Выбор базы данных
db = client.mydatabase

# Выбор коллекции
collection = db.mycollection

# Вставка одного документа
document = {"name": "John", "age": 30}
result = collection.insert_one(document)
print("Вставленный документ ID:", result.inserted_id)

# Вставка нескольких документов
documents = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 35}
]
result = collection.insert_many(documents)
print("Вставленные документы ID:", result.inserted_ids)

# Найти все документы в коллекции
results = collection.find()

# Найти документы, у которых возраст больше 30
results = collection.find({"age": {"$gt": 30}})

# Проход по результатам и вывод данных
for document in results:
    print(document)

# Обновить один документ
filter = {"name": "John"}
update = {"$set": {"age": 35}}
result = collection.update_one(filter, update)
print("Количество обновленных документов:", result.modified_count)

# Обновить несколько документов
filter = {"age": {"$lt": 30}}
update = {"$inc": {"age": 1}}
result = collection.update_many(filter, update)
print("Количество обновленных документов:", result.modified_count)

# Удаление одного документа
filter = {"name": "John"}
result = collection.delete_one(filter)
print("Количество удаленных документов:", result.deleted_count)

# Удаление нескольких документов
filter = {"age": {"$gt": 30}}
result = collection.delete_many(filter)
print("Количество удаленных документов:", result.deleted_count)

# Создание индекса по полю "name"
collection.create_index("name")

pipeline = [
    {"$group": {"_id": "$category", "count": {"$sum": 1}}}
]
results = collection.aggregate(pipeline)
for document in results:
    print(document)

results = collection.find().limit(10)

# Найти документы, у которых возраст больше 30 и меньше 40
results = collection.find({"age": {"$gt": 30, "$lt": 40}})

# Сортировка по полю "name" (если есть соответствующий индекс)
results = collection.find().sort("name")

from pymongo import UpdateOne

operations = [
    UpdateOne({"name": "John"}, {"$set": {"age": 40}}),
    UpdateOne({"name": "Alice"}, {"$inc": {"age": 1}}),
    # Другие операции записи
]

collection.bulk_write(operations)
# получить имена всех учителей текущего subject
pipeline = [
    {
        '$match': {
            'subject': ObjectId(subject_id)
        }
    },
    {
        '$lookup': {
            'from': 'users',
            'localField': 'teacher',
            'foreignField': '_id',
            'as': 'user'
        }
    },
    {
        '$unwind': '$user'
    },
    {
        '$lookup': {
            'from': 'accounts',
            'localField': 'user.account',
            'foreignField': '_id',
            'as': 'account'
        }
    },
    {
        '$unwind': '$account'
    },
    {
        '$project': {
            'firstName': '$account.firstName',
            'lastName': '$account.lastName'
        }
    },
    {
        '$group': {
            '_id': {
                'firstName': '$firstName',
                'lastName': '$lastName'
            }
        }
    },
    {
        '$project': {
            '_id': 0,
            'firstName': '$_id.firstName',
            'lastName': '$_id.lastName'
        }
    }
]

result = collection.aggregate(pipeline)

for teacher in result:
    print(f"Имя: {teacher['firstName']}, Фамилия: {teacher['lastName']}")
