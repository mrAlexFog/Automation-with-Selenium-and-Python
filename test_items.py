import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC

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

    #  браузер получает url из декоратора
    browser.get(url)

    #  явно ожидаем появление кнопки presence_of_element_located - проверяет что элемент будет видемой на странице
    button = WDW(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//form[@id="add_to_basket_form"]//button[@type="submit"]')))

    #  получаем текст кнопки (имя кнопки)
    text = button.text

    #  проверяем что текст кнопки принадлежит перечню языков (русский, испанский, английский, французкий))
    assert text in ("Добавить в корзину", "Añadir al carrito", "Add to basket", "Ajouter au panier")

