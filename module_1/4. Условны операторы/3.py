door_state = 'закрыта'
have_key = True

if door_state == "закрыта":
    print('Надо открыть дверь, не пройдешь')
    if have_key:
        print('открываю дверь')
        door_state = 'открыта'
        if door_state == "открыта":
            print('Проходи, дверь открыта')