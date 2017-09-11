import os
import errno
from xml.dom.minidom import parseString
data_filename = "ignore_data/dba_7920_new.csv"
data_delimiter = "^"
data_terminator = "~"

keywords_filename = "ignore_data/keywords.csv"
keywords_terminator = ","
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
    with open(path, 'rb') as pathfile:
        return pathfile.read()

def clean_text(uncleantext):
    return uncleantext.replace("=0A","")

def create_file(path, content):
    new_file = open(path, 'w+')
    new_file.write(content)
    new_file.close()

def parse_xml(xmltext):
    try:
        minidom = parseString(xmltext.encode('utf-16-be'))
        bodycontents = minidom.getElementsByTagName("Body-Content")
        results = []
        if(len(bodycontents) > 0):
            for bodycontent in bodycontents:
                if (bodycontent is not None and
                            bodycontent.firstChild is not None and
                            bodycontent.firstChild.data is not None):
                    results.append(bodycontent.firstChild.data)
        if(len(results) > 0):
            return "\n".join(results)
        else:
            return None
    except:
        return None

def keyword_exists(subject, xmlemailtext, keyword_records):
    result = False
    for keyword in keyword_records:
        if(keyword.lower() in subject.lower() or keyword.lower() in xmlemailtext.lower()):
            result = True
            break
    return result

def create_pdf(content, path):
    print("creating pdf -> " + path)

def process_subrecord(subrecords, keyword_records):
    # Check if record is valid
    if(len(subrecords) > 1):

        # Get info from the record
        loanid = subrecords[0]
        email = subrecords[2]
        subject = subrecords[3]
        xml_email_text = subrecords[4]
        creation_date = subrecords[6]
        formatted_date = '_'.join(creation_date.split('.')[0].split(' ')).replace(":","-")
        export_filename_html = output_directory + "/" + (loanid) + "/" + str(loanid) + "_" + formatted_date + ".html"
        export_filename_pdf = output_directory + "/" + (loanid) + "/" + str(loanid) + "_" + formatted_date + ".pdf"

        # Create the folder for the current loanid
        mkdir_p(output_directory + "/" + (loanid))

        skip = keyword_exists(subject, xml_email_text, keyword_records)
        if skip is True:
            # Parse Email
            parsedtext = parse_xml(xml_email_text)

            # Create File
            if(parsedtext is not None):
                print("Creating -> " + export_filename_html)
                cleantext = clean_text(parsedtext)
                create_file(export_filename_html, cleantext)
                # convert_html_to_pdf(export_filename_html, export_filename_pdf)
                create_pdf(export_filename_pdf, cleantext)
            else:
                print("No Data: Skipping -> " + export_filename_html)
        else:
            print("Keyword Not Present: Skipping -> " + export_filename_html)

def process_records(data_records, keyword_records):
    # Process each record
    for i in range(len(data_records)):

        # Skip header row
        if i == 0:
          continue

        # Access the record by index
        record = data_records[i]

        # Split custom delimited record
        subrecords = record.split(data_delimiter)
        process_subrecord(subrecords, keyword_records)

# Main
if __name__ == "__main__":

    # Create a new export folder
    mkdir_p(output_directory)

    print("Reading the file")

    datafile_as_string = read_file(data_filename)
    data_records = datafile_as_string.split(data_terminator)
    # Total records in the file
    print("Total data records -> " + str(len(data_records)))

    keywordfile_as_string = read_file(keywords_filename)
    keyword_records = keywordfile_as_string.split(keywords_terminator)
    # Total records in the file
    print("Total keyword records -> " + str(len(keyword_records)))


    print("Processing all records")
    process_records(data_records, keyword_records)