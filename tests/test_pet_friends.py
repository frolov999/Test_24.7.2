from api import PetFriends
from settings import valid_email, valid_password
from settings import not_valid_email, not_valid_password
from settings import uncorrect_auth_key
import os
pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
   #     Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
   #     запрашиваем список всех питомцев и проверяем что список не пустой.
   #     Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
        """Проверяем возможность удаления питомца"""

        # Получаем ключ auth_key и запрашиваем список своих питомцев
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
            _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Берём id первого питомца из списка и отправляем запрос на удаление
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)

        # Ещё раз запрашиваем список своих питомцев
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert status == 200
        assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
        """Проверяем возможность обновления информации о питомце"""

        # Получаем ключ auth_key и список своих питомцев
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
        if len(my_pets['pets']) > 0:
            status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

            # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
            assert status == 200
            assert result['name'] == name
        else:
            # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
            raise Exception("There is no my pets")

        """Мои тесты"""

def test_get_all_pets_with_FAILED_key(filter=''):
    """ Проверка на ввод некорректного auth_key"""
    try:
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.get_list_of_pets(uncorrect_auth_key, filter)
    except TypeError:
        print(' Uncorrect auth_key. Error: TypeError!')

#
def test_get_api_key_for_FAILED_password(email=valid_email, password=not_valid_password):
    """ Проверяем корректность аутентификации. Пароль невалиден."""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    print (' Введен некорректный пароль (',password,')! status==403')


def test_get_api_key_for_FAILED_mail(email=not_valid_email, password=valid_password):
    """ Проверяем корректность аутентификации. Логин невалиден."""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    print (' Введен некорректный логин (',email,')! status==403')


def test_get_api_key_for_FAILED_mail_pass(email=not_valid_email,password=not_valid_password):
    """ Проверяем корректность аутентификации. Логин/пароль невалидны."""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    print (' Логин / пароль - некорректны (',email,'/',password,')!  status==403')
#
def test_add_new_pet_with_FAILED_data_name(name=' ', animal_type='дог', age='4', pet_photo='images/cat1.jpg'):
    """Проверяем возможность добавления питомца с НЕкорректными данными"""

    print(' Не заполнено одно из полей: name. status==500')
    try:
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except InternalServerError:
        print ('  Не заполнено одно из полей: name.')
#
def test_add_new_pet_with_FAILED_data_type(name='.аж08', animal_type='', age='4', pet_photo='images/cat1.jpg'):
    """Проверяем возможность добавления питомца с НЕкорректными данными"""

    print(' Не заполнено одно из полей: animal_type. status==500')
    try:
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except InternalServerError:
        print ('  Не заполнено одно из полей: animal_type.')
#
def test_add_new_pet_with_FAILED_data_age(name='95норл', animal_type='дог', age='', pet_photo='images/cat1.jpg'):
    """Проверяем возможность добавления питомца с НЕкорректными данными"""
    print(' Не заполнено одно из полей: age. status==500')
    try:
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except InternalServerError:
        print ('  Не заполнено одно из полей: age.')
#
#
def test_add_new_pet_with_FAILED_data_age_negative(name='Джон', animal_type='дог', age='-3', pet_photo='images/cat1.jpg'):
    """Проверяем возможность добавления питомца с НЕкорректными данными"""

    print("   Ввод отрицательных значений в поле age.")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200



def test_add_new_pet_with_FAILED_data_age_num(name='98оольть', animal_type='дог', age='/-+', pet_photo='images/cat1.jpg'):
    """Проверяем возможность добавления питомца с НЕкорректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200
    print("   Ввод символов в поле age.")


def test_successful_add_foto_of_pet(pet_id='',pet_photo='images/cat1.jpg'):
    """Проверяем успешность запроса на добавление фото питомца по его id"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_foto_of_pet(auth_key, pet_id, pet_photo)

    # Проверяем что статус ответа = 200 и фото питомца соответствует заданному
    assert status == 200
    assert result['pet_photo']
    print('   Добавление фото питомца по его id')


def test_FAILED_add_foto_of_pet(pet_id='', pet_photo='images/otext.txt'):
    """Проверяем успешность запроса на добавление файла TXT в поле photo питомца"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_foto_of_pet(auth_key, pet_id, pet_photo)

    # Проверяем что статус ответа = 500 и фото питомца соответствует заданному
    assert status == 500
    #assert result['pet_photo']
    print('   Добавление фото - тип файла TXT. status == 500')
