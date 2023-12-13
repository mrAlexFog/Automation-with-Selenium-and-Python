import pytest
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


#  скромная просьба проверяющему, перед запуском теста пожалуйста установите библиотеку webdriver-manager (pip install webdriver-manager)
#  благодаря этой библиотеке больше нет необходимости в скачивании вебдрайверов для различный браузеров (неодходимо только что бы на ПК был установлен сам браузер)
#  прочитав комментарии я понял что идеально выполнить задание, не получив какие либо замечания скорее всего не получится)
#  по этому решил выполнитть его так, что бы проверяющий возможно узнал что то новое и полезное для себя)
#  по опыту работы в тестировании посоветую обратить внимание на файл pytest.ini и его наполнение, особенно на настройку логирования, очень пригодиться для отладки тестов)
#  в файле pytest.ini так же можно настроить параметры запуска теста особенно полезными являются параметры 
#  библиотеки pytest-rerunfailures (pip install pytest-rerunfailures) котая позволяет сразу перезапускать упавший тест (защищает от случайных падений)
#  библиотеки pytest-xdist (pip install pytest-xdist) запускает тесты в нескольких потоках (тесты запускаюься паралельно открывается сразу несколько браузеров (ограничивают только ядра процессора))

#  как запустить что бы не получить ошибок)
#  установить библиотеки из файла Pipfile (selenium, pytest, webdriver-manager)
#  в терминале ввести и запустить команду из задачи pytest --language=es test_items.py
#  специально/ и из-за лени) в строке 71 не прописывал текст кнопки "Добавить в корзину" на всех доступных языках
#  предлагаю что бы посмотреть логирование ошибки запустить команду с языком который я не добавил)
#  например с Румыским, pytest --language=ro test_items.py
#  Удачи Вам и новых знаний)

@pytest.mark.parametrize(
    "url",
    [
        ("http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/")
    ],
    ids=["допустим это dev стенд)"]
) #  передаем url сайта в качестве параметра, + такого подхода в том что тест возможно нужно будет прогонять на разных окружения (например на тестовом стенде и на препроде)
def test_button_add_to_basket(
    browser: webdriver.Chrome | webdriver.Firefox,  #    проверка что параметр браузер имеет класс Chrome или Firefox, так лучше не делать, но по этой причине метод find_element теперь не подсвечен серым и отображается как подсказка после написания browser
    url
):
    """
    Тест проверки наличия на странице кнопки добавить в карзину

    :param: browser - webdriver 
    """
    logging.warning('start test - Проверка доступности кнопки "Добавить в корзину"')
    #  браузер получает url из декоратора
    logging.info(f'переходим по ссылке "{url}"')
    browser.get(url)

    #  собираем результаты всех проверок для финального assert
    set_result_assert = set([True])

    #  явно ожидаем появление кнопки presence_of_element_located - проверяет что элемент будет видемой на странице
    logging.info(f'ищем кнопку на странице')
    #  добавил такую конструкцию так как задание требует что бы на нахождение кнопки должен быть assert) на практике пишу по другому)
    try:
        button = WDW(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//form[@id="add_to_basket_form"]//button[@type="submit"]')))
    except TimeoutException:
        set_result_assert.add(False)
        logging.error(f'Кнопка не найдена на странице')
        assert False, "Кнопка не найдена на странице"

    #  получаем текст кнопки (имя кнопки)
    try:
        logging.info(f'получаем тект(имя) кнопки')
        text = button.text
        logging.info(f'кнопка содержит тект "{text}"')
    except:
        set_result_assert.add(False)
        logging.error(f'ошибка при поиске текста в кнопке')
        assert False, 'ошибка при поиске текста в кнопке'

    #  проверяем что текст кнопки принадлежит перечню языков (Русский, Испанский, Английский, Французкий, Корейский, Польский, Чешский, Арабский, Украинский) для того что бы не ждать 30 секунд)
    try:
        if text not in ("Добавить в корзину", "Añadir al carrito", "Add to basket", "Ajouter au panier", "장바구니 담기", "Dodaj do koszyka", "Vložit do košíku", "أضف الى سلة التسوق", "Додати в кошик"):
            exit()
    except:
        set_result_assert.add(False)
        logging.error('Текст кнопки не соответствует ожидаемому, или введен язык не из перечня')
        assert False, "Текст кнопки не соответствует ожидаемому, или введен язык не из перечня"

    assert True in set_result_assert, "Ошибка выполнения теста, смотрим логи"
    

