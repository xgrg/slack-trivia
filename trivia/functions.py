def get_channel_id(client, name):
    gl = client.groups_list()
    response = [e for e in gl.data['groups']\
        if e['name'] == name]
    if len(response) == 0:
        cl = client.channels_list()
        response = [e for e in cl.data['channels']\
            if e['name'] == name]
    return response[0]['id']

def get_conversation_id(client, id):
    #types=['public_channel','private_channel','mpim','im']
    cl = client.conversations_list(types='im')
    print(cl)
    response = [e for e in cl.data['channels']\
        if e['user'] == id]
    return response[0]['id']


def get_users_table(client):
    table = []
    ul = client.users_list()
    for each in ul.data['members']:
        row = [each['id'], each['name']]
        table.append(row)
    return dict(table)
