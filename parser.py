import os
import errno
import email
from xml.dom.minidom import parseString

filename = "dba_7920_new.csv"
delimiter = "^"
terminator = "~"
output_directory = "exportfiles"

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def read_file(path):
    with open(path, 'rb') as csvfile:
        return csvfile.read().split(terminator)

def create_file(path, content):
    new_file = open(path, 'w+')
    new_file.write(content)
    new_file.close()

def parse_email(xmlemailtext):
    msg = email.message_from_string(xmlemailtext)
    result = msg.get_payload()
    print(result)
    return result

def parse_xml(xmltext):
    result = "<b>No data found<b>"
    return result

def process_subrecord(subrecords):
    # Check if record is valid
    if(len(subrecords) > 1):

        # Get info from the record
        loanid = subrecords[0]
        email = subrecords[2]
        xmlemailtext = subrecords[4]
        creationdate = subrecords[6]
        formatteddate = '_'.join(creationdate.split('.')[0].split(' '))

        # Create the folder for the current loanid
        mkdir_p(str(loanid))
        exportfilename = output_directory + "/" + (loanid) + "/" + str(loanid) + "_" + formatteddate + ".html"

        # Parse Email
        escapedbody = parse_email(xmlemailtext)

        # Create File
        print("Creating -> " + exportfilename)
        create_file(exportfilename, unescapedbody)

def process_records(records):
    # Process each record
    for i in range(len(records)):

        # Skip header row
        if i == 0:
          continue

        # Access the record by index
        record = records[i]

        # Split custom delimited record
        subrecords = record.split(delimiter)
        process_subrecord(subrecords)
        break

# Main
if __name__ == "__main__":

    # Create a new export folder
    mkdir_p(output_directory)

    print("Reading the file")

    records = read_file(filename)

    # Total records in the file
    print("Total records -> " + str(len(records)))

    print("Processing all records")
    process_records(records)