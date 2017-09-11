from xml.dom.minidom import parseString

def read_file(path):
    with open(path, 'r') as xmlfile:
        result = xmlfile.read()
        return result

if __name__ == "__main__":

    xmltext = read_file("ignore_data/multipart.xml")

    minidom = parseString(xmltext.encode('utf-16-be'))

    bodycontents = minidom.getElementsByTagName("Body-Content")

    for bodycontent in bodycontents:
        print(bodycontent.firstChild.data)
