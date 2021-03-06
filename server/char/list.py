from pyraknet.bitstream import Serializable, c_uint8, c_uint16, c_uint32, c_uint64, c_bool
from plugin import Plugin, Action, Packet
from structs import LUHeader, CString, GameVersion

class CharacterList(Plugin):
    def actions(self):
        return [
            Action('pkt:client_character_list_request', self.character_list_request, 10)
        ]

    def packets(self):
        return [
            ClientCharacterListRequest,
            CharacterListResponse
        ]

    def character_list_request(self, packet, address):
        uid = self.server.connections[address]['uid']
        characters = self.server.handle_until_value('char:characters', True, uid)
        serializable_characters = []

        for character in characters:
            serializable_character = Character()
            serializable_character.character_id = character.account.session.objid
            serializable_character.unknown1 = 0
            serializable_character.character_name = character.name
            serializable_character.character_unapproved_name = character.unapproved_name
            serializable_character.is_name_rejected = character.is_name_rejected
            serializable_character.free_to_play = character.account.free_to_play
            serializable_character.unknown2 = 0
            serializable_character.shirt_color = character.shirt_color
            serializable_character.shirt_style = character.shirt_style
            serializable_character.pants_color = character.pants_color
            serializable_character.hair_style = character.hair_style
            serializable_character.hair_color = character.hair_color
            serializable_character.lh = character.lh
            serializable_character.rh = character.rh
            serializable_character.eyebrows = character.eyebrows
            serializable_character.eyes = character.eyes
            serializable_character.mouth = character.mouth
            serializable_character.unknown3 = 0
            serializable_character.last_zone = character.last_zone
            serializable_character.last_instance = character.last_instance
            serializable_character.last_clone = character.last_clone
            serializable_character.last_login = character.last_login
            serializable_character.items = []
            serializable_characters.append(serializable_character)

        res = CharacterListResponse(serializable_characters)

        self.server.rnserver.send(res, address)

class ClientCharacterListRequest(Packet):
    packet_name = 'client_character_list_request'

    @classmethod
    def deserialize(cls, stream):
        return cls()

class CharacterListResponse(Packet):
    packet_name = 'character_list_response'

    def __init__(self, characters):
        super().__init__(**{k:v for k,v in locals().items() if k != 'self'})

    def serialize(self, stream):
        super().serialize(stream)
        front_char = self.server.handle_until_value('char:front_char_index', True, self.characters[0].user_id)
        stream.write(c_uint8(front_char))
        stream.write(len(self.characters))
        for character in self.characters:
            character.serialize(stream)

class Character(Serializable):
    def __init__(self, character_id, unknown1, character_name, character_unapproved_name, is_name_rejected, free_to_play,
                 unknown2, shirt_color, shirt_style, pants_color, hair_style, hair_color, lh, rh, eyebrows, eyes, mouth,
                 unknown3, last_zone, last_instance, last_clone, last_login, items
                ):
        self.character_id = character_id
        self.unknown1 = unknown1
        self.character_name = character_name
        self.character_unapproved_name = character_unapproved_name
        self.is_name_rejected = is_name_rejected
        self.free_to_play = free_to_play
        self.unknown2 = unknown2
        self.shirt_color = shirt_color
        self.shirt_style = shirt_style
        self.pants_color = pants_color
        self.hair_style = hair_style
        self.hair_color = hair_color
        self.lh = lh
        self.rh = rh
        self.eyebrows = eyebrows
        self.eyes = eyes
        self.mouth = mouth
        self.unknown3 = unknown3
        self.last_zone = last_zone
        self.last_instance = last_instance
        self.last_clone = last_clone
        self.last_login = last_login
        self.items = items


    def serialize(self, stream):
        stream.write(c_int64(character_id))
        stream.write(c_uint32(unknown1))
        stream.write(character_name)
        stream.write(character_unapproved_name)
        stream.write(is_name_rejected)
        stream.write(free_to_play)
        stream.write(unknown2, allocated_length=10)
        stream.write(c_uint32(shirt_color))
        stream.write(c_uint32(shirt_style))
        stream.write(c_uint32(pants_color))
        stream.write(c_uint32(hair_style))
        stream.write(c_uint32(hair_color))
        stream.write(c_uint32(lh))
        stream.write(c_uint32(rh))
        stream.write(c_uint32(eyebrows))
        stream.write(c_uint32(eyes))
        stream.write(c_uint32(mouth))
        stream.write(c_uint32(unknown3))
        stream.write(c_uint16(last_zone))
        stream.write(c_uint16(last_instance))
        stream.write(c_uint32(last_clone))
        stream.write(c_uint64(last_login))
        stream.write(c_uint16(len(items)))
        for item in items:
            stream.write(c_uint32(item))

    @classmethod
    def deserialize(cls, stream):
        character_id = stream.read(c_int64)
        unknown1 = stream.read(c_uint32)
        character_name = stream.read(CString(self.unknown, allocated_length=66))
        character_unapproved_name = stream.read(CString(self.unknown, allocated_length=66))
        is_name_rejected = stream.read(c_bool)
        free_to_play = stream.read(c_bool)
        unknown2 = stream.read(bytes, allocated_length=10)
        shirt_color = stream.read(c_uint32)
        shirt_style = stream.read(c_uint32)
        pants_color = stream.read(c_uint32)
        hair_style = stream.read(c_uint32)
        hair_color = stream.read(c_uint32)
        lh = stream.read(c_uint32)
        rh = stream.read(c_uint32)
        eyebrows = stream.read(c_uint32)
        eyes = stream.read(c_uint32)
        mouth = stream.read(c_uint32)
        unknown3 = stream.read(c_uint32)
        last_zone = stream.read(c_uint16)
        last_instance = stream.read(c_uint16)
        last_clone = stream.read(c_uint32)
        last_login = stream.read(c_uint64)
        item_count = stream.read(c_uint16)
        items = []
        for item in range(item_count):
            items.append(stream.read(c_uint32))

        return cls(character_id, unknown1, character_name, character_unapproved_name, is_name_rejected, free_to_play,
                     unknown2, shirt_color, shirt_style, pants_color, hair_style, hair_color, lh, rh, eyebrows, eyes, mouth,
                     unknown3, last_zone, last_instance, last_clone, last_login, items)
