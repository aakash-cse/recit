from pyresparser import ResumeParser
import os
import shutil
import json
from extra import write_log

dat_file_storage = 'json_files'

def model_extract():
    write_log('\n#Resume Parser Initiated#')
    try:
        shutil.rmtree(dat_file_storage, ignore_errors=True)
        write_log("destroyed json_files")
    except:
        write_log('unable to destry json_files')
        exit()

    if not os.path.isdir(dat_file_storage):
        os.makedirs(dat_file_storage, exist_ok=True)
        write_log("\ncreated json_files")
    else:
        write_log("unable create json_files")
        exit()

    try:
        for root, dirs, files in os.walk("./pdf_files", topdown=False):
            for name in files:
                write_log('Accessing File: '+name)
                filename = (os.path.join(root, name))
                if filename.endswith('.pdf'):
                    try:
                        data = ResumeParser(filename).get_extracted_data()
                        write_log('Parser failed to convert'+filename)
                    except:
                        write_log('Parsing completed'+filename)

                    file_path = os.path.join(dat_file_storage, name)
                    with open(file_path[:-4]+'.json', 'w') as file:
                        file.write(json.dumps(data))
                    write_log('Parsing Done')
                else:
                    write_log('Invalid File')
    except:
        write_log('Unable to fetch pdf files')

    write_log('\n#Resume Parser Ended#')

    try:
        shutil.rmtree('pdf_files', ignore_errors=True)
        write_log("destroyed pdf_files")
    except:
        write_log('unable to destry pdf_files')


# pip install pyresparser
# python -m nltk.downloader words
# python -m spacy download en_core_web_sm
