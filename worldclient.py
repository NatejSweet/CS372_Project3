import sys
import socket

# How many bytes is the word length?
WORD_LEN_SIZE = 2

def usage():
    print("usage: wordclient.py server port", file=sys.stderr)

packet_buffer = b''

def get_next_word_packet(s):
    """
    Return the next word packet from the stream.

    The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.

    Returns None if there are no more words, i.e. the server has hung
    up.
    """

    global packet_buffer
    data = s.recv(1024)
    if not data and not packet_buffer:
        return None
    data = data
    packet_buffer += data
    if packet_complete(packet_buffer):
        length = int.from_bytes(packet_buffer[:WORD_LEN_SIZE], byteorder="big") #extract length from the header (\x00\x05 -> 5)
        word_packet = packet_buffer[:WORD_LEN_SIZE+length] #extract message from the data (\x00\x05hello -> hello)
        packet_buffer = packet_buffer[WORD_LEN_SIZE+length:]
        return word_packet
    else:
        return get_next_word_packet(s)
    
def packet_complete(data):
    if len(data) < WORD_LEN_SIZE: #no complete header / buffer empty
        return False
    length = int.from_bytes(data[:WORD_LEN_SIZE], byteorder="big") #extract length from the header (\x00\x05 -> 5)
    message = data[WORD_LEN_SIZE:length+WORD_LEN_SIZE] #extract message from the data (\x00\x05hello -> hello)
    return  length == len(message)#if the expected length is the actual length of the message, return True


def extract_word(word_packet):
    """
    Extract a word from a word packet.

    word_packet: a word packet consisting of the encoded word length
    followed by the UTF-8 word.

    Returns the word decoded as a string.
    """
    length = int.from_bytes(word_packet[:WORD_LEN_SIZE], byteorder="big") #extract length from the header
    packet = word_packet[WORD_LEN_SIZE:length+WORD_LEN_SIZE] #extract packet from the data (\x00\x05hello\x00\x01\h -> \x00\x05hello)
    return packet.decode('utf-8')

# Do not modify:

def main(argv):
    try:
        host = argv[1]
        port = int(argv[2])
    except:
        usage()
        return 1

    s = socket.socket()
    s.connect((host, port))

    print("Getting words:")

    while True:
        word_packet = get_next_word_packet(s)

        if word_packet is None:
            break

        word = extract_word(word_packet)

        print(f"    {word}")

    s.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
