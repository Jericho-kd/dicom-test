# DICOM test assignment
Разработать консольное приложение, выполняющее следующие операции:
1. Выполняет C-FIND запрос к PACS по модальности MG, получая список всех исследований в этой модальности
2. Получает от PACS медицинские изображения первой попавшейся серии в первом попавшемся исследовании из списка п.1
3. Создаёт новую серию, содержащую медицинские изображения, повторяющие полученные из PACS, но повернутые на 90 градусов
4. Загружает новую серию в исходное исследование в PACS

В качестве тестового PACS можно использовать контейнеризованный orthanc (osimis/orthanc или jodogne/orthanc).

Версии библиотек:\
pydicom==2.4.3\
pynetdicom==2.0.2 
