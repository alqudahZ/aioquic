import binascii
from unittest import TestCase

from aioquic.crypto import CryptoPair, derive_initial_secret, derive_key_iv_hp

CLIENT_PLAIN_HEADER = binascii.unhexlify('c3ff000012508394c8f03e51570800449f00000002')
CLIENT_PLAIN_PAYLOAD = binascii.unhexlify(
    '060040c4010000c003036660261ff947cea49cce6cfad687f457cf1b14531ba1'
    '4131a0e8f309a1d0b9c4000006130113031302010000910000000b0009000006'
    '736572766572ff01000100000a00140012001d00170018001901000101010201'
    '03010400230000003300260024001d00204cfdfcd178b784bf328cae793b136f'
    '2aedce005ff183d7bb1495207236647037002b0003020304000d0020001e0403'
    '05030603020308040805080604010501060102010402050206020202002d0002'
    '0101001c00024001') + bytes(963)
CLIENT_ENCRYPTED_PACKET = binascii.unhexlify(
    'c1ff000012508394c8f03e51570800449f0dbc195a0000f3a694c75775b4e546'
    '172ce9e047cd0b5bee5181648c727adc87f7eae54473ec6cba6bdad4f5982317'
    '4b769f12358abd292d4f3286934484fb8b239c38732e1f3bbbc6a003056487eb'
    '8b5c88b9fd9279ffff3b0f4ecf95c4624db6d65d4113329ee9b0bf8cdd7c8a8d'
    '72806d55df25ecb66488bc119d7c9a29abaf99bb33c56b08ad8c26995f838bb3'
    'b7a3d5c1858b8ec06b839db2dcf918d5ea9317f1acd6b663cc8925868e2f6a1b'
    'da546695f3c3f33175944db4a11a346afb07e78489e509b02add51b7b203eda5'
    'c330b03641179a31fbba9b56ce00f3d5b5e3d7d9c5429aebb9576f2f7eacbe27'
    'bc1b8082aaf68fb69c921aa5d33ec0c8510410865a178d86d7e54122d55ef2c2'
    'bbc040be46d7fece73fe8a1b24495ec160df2da9b20a7ba2f26dfa2a44366dbc'
    '63de5cd7d7c94c57172fe6d79c901f025c0010b02c89b395402c009f62dc053b'
    '8067a1e0ed0a1e0cf5087d7f78cbd94afe0c3dd55d2d4b1a5cfe2b68b86264e3'
    '51d1dcd858783a240f893f008ceed743d969b8f735a1677ead960b1fb1ecc5ac'
    '83c273b49288d02d7286207e663c45e1a7baf50640c91e762941cf380ce8d79f'
    '3e86767fbbcd25b42ef70ec334835a3a6d792e170a432ce0cb7bde9aaa1e7563'
    '7c1c34ae5fef4338f53db8b13a4d2df594efbfa08784543815c9c0d487bddfa1'
    '539bc252cf43ec3686e9802d651cfd2a829a06a9f332a733a4a8aed80efe3478'
    '093fbc69c8608146b3f16f1a5c4eac9320da49f1afa5f538ddecbbe7888f4355'
    '12d0dd74fd9b8c99e3145ba84410d8ca9a36dd884109e76e5fb8222a52e1473d'
    'a168519ce7a8a3c32e9149671b16724c6c5c51bb5cd64fb591e567fb78b10f9f'
    '6fee62c276f282a7df6bcf7c17747bc9a81e6c9c3b032fdd0e1c3ac9eaa5077d'
    'e3ded18b2ed4faf328f49875af2e36ad5ce5f6cc99ef4b60e57b3b5b9c9fcbcd'
    '4cfb3975e70ce4c2506bcd71fef0e53592461504e3d42c885caab21b782e2629'
    '4c6a9d61118cc40a26f378441ceb48f31a362bf8502a723a36c63502229a462c'
    'c2a3796279a5e3a7f81a68c7f81312c381cc16a4ab03513a51ad5b54306ec1d7'
    '8a5e47e2b15e5b7a1438e5b8b2882dbdad13d6a4a8c3558cae043501b68eb3b0'
    '40067152337c051c40b5af809aca2856986fd1c86a4ade17d254b6262ac1bc07'
    '7343b52bf89fa27d73e3c6f3118c9961f0bebe68a5c323c2d84b8c29a2807df6'
    '63635223242a2ce9828d4429ac270aab5f1841e8e49cf433b1547989f419caa3'
    'c758fff96ded40cf3427f0761b678daa1a9e5554465d46b7a917493fc70f9ec5'
    'e4e5d786ca501730898aaa1151dcd31829641e29428d90e6065511c24d3109f7'
    'cba32225d4accfc54fec42b733f9585252ee36fa5ea0c656934385b468eee245'
    '315146b8c047ed27c519b2c0a52d33efe72c186ffe0a230f505676c5324baa6a'
    'e006a73e13aa8c39ab173ad2b2778eea0b34c46f2b3beae2c62a2c8db238bf58'
    'fc7c27bdceb96c56d29deec87c12351bfd5962497418716a4b915d334ffb5b92'
    'ca94ffe1e4f78967042638639a9de325357f5f08f6435061e5a274703936c06f'
    'c56af92c420797499ca431a7abaa461863bca656facfad564e6274d4a741033a'
    'ca1e31bf63200df41cdf41c10b912bec')

SERVER_PLAIN_HEADER = binascii.unhexlify('c1ff00001205f067a5502a4262b50040740001')
SERVER_PLAIN_PAYLOAD = binascii.unhexlify(
    '0d0000000018410a020000560303eefce7f7b37ba1d1632e96677825ddf73988'
    'cfc79825df566dc5430b9a045a1200130100002e00330024001d00209d3c940d'
    '89690b84d08a60993c144eca684d1081287c834d5311bcf32bb9da1a002b0002'
    '0304')
SERVER_ENCRYPTED_PACKET = binascii.unhexlify(
    'c4ff00001205f067a5502a4262b5004074f7ed5f01c4c2a2303d297e3c519bf6'
    'b22386e3d0bd6dfc66121677298031041bb9a79c9f0f9d4c5877270a660f5da3'
    '6207d98b73839b2fdf2ef8e7df5a51b17b8c68d864fd3e708c6c1b71a98a3318'
    '15599ef5014ea38c44bdfd387c03b5275c35e009b6238f831420047c7271281c'
    'cb54df7884')


class CryptoTest(TestCase):
    """
    Test vectors from:

    https://tools.ietf.org/html/draft-ietf-quic-tls-18#appendix-A
    """
    def test_client_initial(self):
        cid = binascii.unhexlify('8394c8f03e515708')
        algorithm, secret = derive_initial_secret(cid, is_client=True)
        key, iv, hp = derive_key_iv_hp(algorithm, secret)
        self.assertEqual(key, binascii.unhexlify('98b0d7e5e7a402c67c33f350fa65ea54'))
        self.assertEqual(iv, binascii.unhexlify('19e94387805eb0b46c03a788'))
        self.assertEqual(hp, binascii.unhexlify('0edd982a6ac527f2eddcbb7348dea5d7'))

    def test_server_initial(self):
        cid = binascii.unhexlify('8394c8f03e515708')
        algorithm, secret = derive_initial_secret(cid, is_client=False)
        key, iv, hp = derive_key_iv_hp(algorithm, secret)
        self.assertEqual(key, binascii.unhexlify('9a8be902a9bdd91d16064ca118045fb4'))
        self.assertEqual(iv, binascii.unhexlify('0a82086d32205ba22241d8dc'))
        self.assertEqual(hp, binascii.unhexlify('94b9452d2b3c7c7f6da7fdd8593537fd'))

    def test_decrypt_packet_client(self):
        pair = CryptoPair.initial(cid=binascii.unhexlify('8394c8f03e515708'), is_client=False)

        plain_header, plain_payload = pair.recv.decrypt_packet(CLIENT_ENCRYPTED_PACKET, 17)
        self.assertEqual(plain_header, CLIENT_PLAIN_HEADER)
        self.assertEqual(plain_payload, CLIENT_PLAIN_PAYLOAD)

    def test_decrypt_packet_server(self):
        pair = CryptoPair.initial(cid=binascii.unhexlify('8394c8f03e515708'), is_client=True)

        plain_header, plain_payload = pair.recv.decrypt_packet(SERVER_ENCRYPTED_PACKET, 17)
        self.assertEqual(plain_header, SERVER_PLAIN_HEADER)
        self.assertEqual(plain_payload, SERVER_PLAIN_PAYLOAD)

    def test_encrypt_packet_client(self):
        pair = CryptoPair.initial(cid=binascii.unhexlify('8394c8f03e515708'), is_client=True)

        packet = pair.send.encrypt_packet(CLIENT_PLAIN_HEADER, CLIENT_PLAIN_PAYLOAD)
        self.assertEqual(packet, CLIENT_ENCRYPTED_PACKET)

    def test_encrypt_packet_server(self):
        pair = CryptoPair.initial(cid=binascii.unhexlify('8394c8f03e515708'), is_client=False)

        packet = pair.send.encrypt_packet(SERVER_PLAIN_HEADER, SERVER_PLAIN_PAYLOAD)
        self.assertEqual(packet, SERVER_ENCRYPTED_PACKET)
