# Описание установки

## Окружение
1. установить Python (думаю тут инструкции не нужны, а если и надо то пишите)
2. установить зависимости  `pip install -r req.txt` (делается из консоли находясь в каталоге с репозиторием aka trah_bot)


## Боты
1. Каждому боту (пакет соответствует имени бота) в файле bot.py указать ключ API, кроме материнского (спросить у Оксаны)
2. События с сохранением/загрузки состояния пользователей нужно обсудить
3. События с трекингом процента дочитываемости и количества открытия каждого из ботом нужно обсудить 
4. Каждый бот запускается отдельно из корня репозитория (бот = 1 консоль, для мониторинга)


## Добавление нового бота
*Будет дополнено*


## Конвертер
Принимает фаил под названием "novel.xlsx" (должен находиться в папке converter) и конвертирует его в json (для последующего использования и хранения).
Полученный на выводе фаил ("dialogs.json") закинуть в соответствующего бота в каталог storage (либо допилить скрипт на сейв в БД)
