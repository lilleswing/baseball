__author__ = 'karl'


def split_events_by_game(events):
    if not events:
        return list()
    event_list = list()
    l = list()
    event_list.append(l)
    cur_game_id = events[0].game_id
    for event in events:
        if event.game_id == cur_game_id:
            l.append(event)
        else:
            l = list()
            event_list.append(l)
            l.append(event)
    return event_list