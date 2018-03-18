'''
================================
USER
================================
'''


class User:
    username = ""
    address = ("", 0)

    def __init__(self, address, username="anonymous"):
        self.username = username
        self.address = address


'''
================================
USERMANAGER
================================
'''


class UserManager:
    clients = []

    def fetch_clientaddress(self, name):
        for c in self.clients:
            if c.username == name:
                return c.address

    def fetch_client(self, name):
        for c in self.clients:
            if c.username == name:
                return User(c)

    def is_member(self, address):
        for c in self.clients:
            if c.address == address:
                return True
        return False

    def to_string(self):
        data = ""
        for i in range(len(self.clients)):
            data += ("\t\t{} : {}\n".format(self.clients[i].username, self.clients[i].address))
        return str(data)




''' 
================================
GROUP
================================
'''


class Group:
    group_id = ""
    members = []
    password = ""

    def __init__(self, group_id, first_client, password=""):
        self.group_id = group_id
        self.password = password
        self.members.append(first_client)

    def add_member(self, client, password=""):
        if str(self.password) == str(password):
            self.members.append(client)
            print("<JoinRoom grp=" + str(self.group_id) + " mem=" + str(client) + ">")

    def check_total(self):
        return len(self.members)

    def is_in_group(self, name):
        for i in range(len(self.members)):
            if str(self.members[i]) == str(name):
                return True
        return False


''' 
================================
GROUP MANAGER
================================
'''


class GroupManager:
    groups = []

    def add_groupchat(self, group_id, first_client):
        self.groups.append(Group(group_id=group_id, first_client=first_client))
        print("<GroupStatus total=" + str(len(self.groups)) + ">")
        print("<AddGroup name=" + group_id + ">")

    def join_groupchat(self, group_id, client):
        self.find_group(group_id).add_member(client=client, password="")
        print("<JoinGroup grp=" + str(group_id) + " mem=" + str(client) + ">")

    def add_chatroom(self, group_id, first_client, password):
        self.groups.append(Group(group_id=group_id, first_client=first_client, password=password))
        print("<GroupStatus total=" + str(len(self.groups)) + ">")
        print("<AddRoom name=" + group_id + ">")
        print("password is " + str(self.groups[0].password))

    def join_chatroom(self, group_id, client, password):
        self.find_group(group_id).add_member(client=client, password=str(password))

    def find_group(self, name):
        for i in range(len(self.groups)):
            if str(self.groups[i].group_id) == str(name):
                print("<FindGroup FOUND>")
                return self.groups[i]
        print("<FindGroup NOTFOUND>")

    def is_in_group(self, group, name):
        return self.find_group(str(group)).is_in_group(str(name))

    def get_chatrooms(self):
        rooms = []
        for g in self.groups:
            if str(g.password) != "":
                rooms.append(g)
        return rooms

    def get_groupchats(self):
        rooms = []
        for g in self.groups:
            if str(g.password) == "":
                rooms.append(g)
        return rooms
