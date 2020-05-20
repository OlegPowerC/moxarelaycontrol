Включение на 1 секунду (по умолчанию, можно изменить) реле 1 (так же можно изменить на 2)
Так как по SNMP пока невозможно включить - выключить реле, способ таков:
По SSH подключаемся и конфигурируем выход реле как:
    Сначала relay-warning event di 1 off relay 1
    пауза 1 секунда, no relay-warning event di 1 off
    Затем relay-warning event di 1 on relay 1
    пауза 1 секунда, no relay-warning event on 1 off

Для чего дважды? потому как состояние входа может быть off или on и реле в любом случае сработает.
При срабатывании реле загорается светодиод Fault!

Контакты реле в коммутаторах Moxa нормально замкнуты
То есть срабатывание реле, означает их размыкание

если не указывать имя пользователя и пароль , то имя читается из файла configmoxa.txt а пароль из keychain с именем
указанным в файле.

Пример команды:
python3 relayonoff.py -u admin -p admin -i 192.168.1.34 -c moxacommand.txt

Так же в CentOS 7 требуется:
sudo yum install -y rng-tools
systemctl start rngd.service
systemctl enable rngd.service
