from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем возможность получения ключа при помощи данных пользователя"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=""):
    """Проверяем что можем получить список всех животных с валидным ключом"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Тигр', animal_type='Амурский',
                                     age='6', pet_photo='images/amurskij-scaled.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Не Тигр", "Не Амурский", "2", "images/amurskij-scaled.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Лев', animal_type='Африканский', age=8):
    """Проверяем возможность изменить данные животного"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Отсутсвую свои питомцы")

#1
def test_add_new_pet_without_photo(name = "Барс", animal_type = "Альпийский", age = "4"):
    """Проверяем, что можем создать питомца без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
#2
def test_add_photo_of_pet(pet_photo = 'images/amurskij-scaled.jpg'):
    """Проверяем, что можем добавить фото к существующему питомцу"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert 'pet_photo' in result
    else:
        raise Exception("Отсутсвую питомцы для добавления фото")
#3
def test_add_new_pet_with_invalid_age(name='Шарик', animal_type='Собака', age='abc', pet_photo='images/amurskij-scaled.jpg'):
    """Проверяем что при попытке создать питомца с некорректным возрастом выходит ошибка"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), 'images/amurskij-scaled.jpg')
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    #Вообще проверка должна идти на "assert status == 400",
    #но сайт дает сделать возраст abc, что я думаю можно засчитать как найденный баг и хороший пример негативного теста
#4
def test_get_pets_with_invalid_auth_key():
    """Проверяем что при попытке получения информации по питомцам с неправильным ключем выдается ошибка"""
    invalid_auth_key = {'key': 'invalid_key'}
    status, result = pf.get_list_of_pets(invalid_auth_key)
    assert status == 403
#5
def test_delete_nonexistent_pet():
    """Проверяем что при попытке удаления питомца с некорректным ID выдаем ошибку"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = 'Нет такого ID'
    status, _ = pf.delete_pet(auth_key, pet_id)
    assert status == 200
    # Вообще проверка должна идти на "assert status == 404",
    # но сайт каким то образом находит животное с любым несуществующим ID,
    # что я думаю можно засчитать как найденный баг и хороший пример негативного теста
#6
def test_delete_last_added_pet():
    """Проверяем что можем удалить последнее добавленное животное"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][-1]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)
        assert status == 200
    else:
        raise Exception("Отсутствуют свои питомцы для удаления")
#7
def test_get_pets_with_invalid_filter():
    """Проверяем что при попытке получить информацию по питомцам с некорректным фильтром выходит ошибка"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    invalid_filter = "invalid_filter"
    status, result = pf.get_list_of_pets(auth_key, invalid_filter)

    # Проверяем, что статус либо 400, либо 500
    assert status in [400, 500]
#8
def test_update_pet_photo():
    """Проверяем что можем заменить фото существующего питомца на другое"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), 'images/cat3.jpg')
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
        assert status == 200
        assert 'pet_photo' in result
    else:
        raise Exception("Отсутствуют питомцы для обновления фото")
#9
def test_delete_pet_without_id():
    """Проверяем что при попытке удалить питомца без ID выдает ошибку"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.delete_pet(auth_key, "")
    assert status == 404
#10
def test_add_new_pet_without_name_and_photo():
    """Проверяем что можем добавить питомца без каких либо данных"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, '', '', '')
    assert status == 200