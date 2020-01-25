def get_user_id(client, name):
    ul = client.users_list()
    response = [e for e in ul.data['members']\
        if e['name'] == name]
    return response[0]['id']


def get_channel_id(client, name):
    gl = client.groups_list()
    response = [e for e in gl.data['groups']\
        if e['name'] == name]
    if len(response) == 0:
        cl = client.channels_list()
        response = [e for e in cl.data['channels']\
            if e['name'] == name]
    return response[0]['id']


def get_users_table(client):
    table = []
    ul = client.users_list()
    for each in ul.data['members']:
        row = [each['id'], each['name']]
        table.append(row)
    return dict(table)
