import time, random
from hashlib import sha256

questions = [
    "Which Group is associated with this campaign?",
    "In what year did the group acquire initial access?",
    "Which technique did the group use to achieve initial access?",
    "What was the product or solution that the group abused to achieve initial access?",
    "What CVE is attributed to the vulnerability that was abused in the product from the previous question? (CVE-YYYY-NNNN)",
    "What's the software ID of the malware that was used by the group as ransomware?",
    "What was the malware's name during the campaign?",
    "What's the software ID of the malware that was used to corrupt the disks?",
    "What was the malware's name during the campaign?",
    "What's the name of the process that was used to spread the ransomware in the internal network?",
    "The group used a script for input capture. What is its name? ",
    "The group used many scripts to achieve persistence. Give me a name for one of those scripts (include extensions)",
    "Which protocol was used by the group to exfiltrate data from compromised hosts?"
]

answers = [
    "HEXANE",
    "2021",
    "T1190",
    ["Microsoft SharePoint", "SharePoint", "sharepoint", "microsoft sharepoint"],
    "CVE-2019-0604",
    "S1150",
    "GoXML.exe",
    "S1151",
    "cl.exe",
    "Mellona.exe",
    "kl.ps1",
    ["pickers.aspx", "error4.aspx", "ClientBin.aspx"],
    ["HTTP","http"]
]

def get_flag():
    seed = (str(random.randint(10,99)) + ((hex(int(time.time()))[4:])))
    uni_hash = b"e042373490c35dc4b7be5b9420d22cbf"
    FLAG = b"SparkCTF{" + uni_hash[:12] + seed.encode() + uni_hash[-12:] + b"_1t_15_4ll_4b0ut_M1Tr3_4nd_4tt4ck_T3chn1qu3s}"
    print(FLAG)

def questions_answers():
    qs_num = len(questions)
    i = 0
    print("[+] NOTE: You have 3 attempts on each question before the connection is closed! GL HF \n")
    print("==============================================================================\n")
    while i < qs_num:
        wrong_attempts = 0
        while True:
            user_answer = input(f"{questions[i]} \n=> ")
            if type(answers[i]) == list:
                if user_answer.strip().lower() in str(answers[i]).lower():
                    print("[+] Correct!")
                    i += 1
                    break
                else:
                    wrong_attempts += 1
                    print(f"[-] Incorrect answer. Attempt {wrong_attempts} of 3.")
            else:
                if user_answer.strip().lower() == str(answers[i]).lower():
                    print("[+] Correct!")
                    i += 1
                    break
                else:
                    wrong_attempts += 1
                    print(f"[-] Incorrect answer. Attempt {wrong_attempts} of 3.")
            
            if wrong_attempts == 3:
                print("[-] You have made 3 incorrect attempts! Retry again later")
                quit()
                wrong_attempts = 0 
def main():
    questions_answers()
    get_flag()

main()
