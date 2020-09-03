import sqlite3
import os
import json
from extra import write_log

dat_file_storage = 'json_files'


def data_load():

    write_log('\n#Data Load Started#')
    conn = sqlite3.connect('database.sql')

    cur = conn.cursor()
    cmd = '''INSERT INTO CANDIDATES (NAME,EMAIL,MOBILE_NO,SKILLS,COLLEGE_NAME, YEARS_OF_EXP,NO_OF_PAGES,QUALIFICATION,DESIGNATION,EXPERIENCE,COMPANY_NAME,YEARS_OF_EXP,NO_OF_PAGES,LAST_UPDATED_DATE) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,DATE('now'))'''

    for root, dirs, files in os.walk(dat_file_storage, topdown=False):
        for name in files:
            write_log('\nAccessing File: '+name)
            filename = (os.path.join(root, name))
            if filename.endswith('.json'):
                with open(filename) as f:
                    dat_obj = json.load(f)

                name = dat_obj['name']
                email = dat_obj['email']
                mob_no = dat_obj['mobile_number']
                skills = ', '.join(dat_obj['skills'])
                college_name = dat_obj['college_name']

                degree = dat_obj['degree']
                if isinstance(degree, list):
                    degree = ' '.join(degree)

                designation = dat_obj['designation']
                if isinstance(designation, list):
                    designation = ' '.join(designation)

                experience = dat_obj['experience']
                if isinstance(experience, list):
                    experience = ' '.join(experience)

                company_names = dat_obj['company_names']
                if isinstance(company_names, list):
                    company_names = ' '.join(company_names)

                total_experience = dat_obj['total_experience']
                pg_count = dat_obj['no_of_pages']

                try:
                    cur.execute(cmd, (name, email, mob_no, skills, college_name, total_experience, pg_count,
                                      degree, designation, experience, company_names, total_experience, pg_count))
                    conn.commit()
                    write_log('Data loaded successfully')
                except:
                    write_log("Data load failure")

    conn.close()
    write_log('\n#Data Load Finished#')
    