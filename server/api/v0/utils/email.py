# Email server
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

from_user       = os.environ.get("GMAIL_EMAIL")
from_password   = os.environ.get("GMAIL_PASSWORD")

def init_server():
    try:
        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server_ssl.login(from_user, from_password)
    except:
        print("SMTP failed to initialize server connections")
    return server_ssl

def send_email(to_addr, subject, body):
    msg = MIMEText(body, 'html')
    msg['Subject']  = subject
    msg['From']     = from_user
    msg['To']       = ','.join(to_addr)
    server_ssl = init_server()
    server_ssl.sendmail(from_user, to_addr, msg.as_string())
    server_ssl.close()


def format_period_history(month_year, list_date, ref_data):
    def helper_find_name_from_id(inKey, inValue=None):
        # By default, it will search as key
        # if inValue==True, search as value
        for curr_dict in ref_data:
            if curr_dict['key'] == inKey:
                if not inValue:
                    return curr_dict['title']
                else:
                    foundIndex = curr_dict['availableOptions_id'].index(inValue)
                    return curr_dict['availableOptions'][foundIndex]
        return 'N/A'

    res = f"""
    <html>
    <h2>You have {len(list_date)} period days in {month_year}:</h2>
    <br/>
    """
    
    for curr_date in list_date:
        res += f"<h3>{curr_date['dateStr']}</h3>"
        for symp_key, symp_val in curr_date['symptoms'].items():
            symp_key_name = helper_find_name_from_id(symp_key)
            symp_val_names = [helper_find_name_from_id(symp_key, x) for x in symp_val]
            res += f"""
            <p><b>{symp_key_name}</b> : {', '.join(symp_val_names)}</p>
            """
        res += "<br/>"

    res += """
    </html>
    """

    return res

if __name__ == "__main__":
    server_ssl = init_server()
    server_ssl.sendmail(from_user, "aryapatel.1921@gmail.com", "Testing Period Tracker App")
    server_ssl.close()