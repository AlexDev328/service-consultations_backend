Сервис консультаций
=====================

#Для работа сервиса консультаций требуется несколько составляющих:
+ [Peerjs server](https://github.com/peers/peerjs-server)
Сервер для работы WebRTC обеспечивает роутинг для обеспечения звонков между клиентами
Команда для старта   peerjs --path peer --port 9000 --proxied true
  (--allow_discovery можно добавить для защиты от доступа к клиентам извне.)
+ Бекенд приложения осуществляет выдачу идентефикаторов клиентам для звонков
+ На клиенте используется [peerjs-client](https://peerjs.com) - Предоставляет интерфейс для работы с WebRTC
Описание api для взаимодействия по ссылке. 


# При "сложной сети " peerjs-server не может установить соединение (нам нужно подключение напрямую при наличии NAT с одной или двух сторон нужны STUN/TURN сервера)
    STUN Сервер позволяет узнать реальный IP конечного пользователя для установления соединения
    TURN Сервер используется если не удалось узнать реальный IP клиента. В данном случае соединение идет не P2P, а через turn server!
    STUN и TURN сервер лучше использовать COTURN Можно поставить из реп ubuntu.
[Самый лучший мануал](https://gabrieltanner.org/blog/turn-server)
[Мануал №2](https://www.dmosk.ru/miniinstruktions.php?mini=coturn)
[Мануал №3](https://russianblogs.com/article/96781030463/)



Т.к. тестировать работу STUN/TURN сервера не удается проверить можно воспользоваться [сервисом](https://webrtc.github.io/samples/src/content/peerconnection/trickle-ice/)
Если будут ошибки на ip v6 это нормально. на ip v4 ошибок быть не должно.


