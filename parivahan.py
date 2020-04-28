import requests
import lxml.html
import json


def session():
    # request headers to be submit along POST request
    headers = {
        'Accept': 'application/xml, text/xml, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Faces-Request': 'partial/ajax',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
        'Sec-Fetch-Site': 'same-origin',
        'X-Requested-With': 'XMLHttpRequest',
    }

    # form details to be sent for login into portal
    logindetails = {
        'javax.faces.partial.ajax': 'true',
        'javax.faces.source: form_rcdl': 'j_idt46',
        'javax.faces.partial.execute': '@all',
        'javax.faces.partial.render': 'form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl',
        'form_rcdl:j_idt46': 'form_rcdl:j_idt46',

    }
    # urls for requesting GET & POST request

    url = "https://parivahan.gov.in/rcdlstatus/?pur_cd=101"
    url2 = "https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml"
    # start session here.
    with requests.session() as s:
        r = s.get(url)  # call get request.
        login_html = lxml.html.fromstring(r.content)
        hidden_inputs = login_html.xpath('//form//input[@type="hidden"]')  # call for hidden inputs require  for login.
        form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}  # store in the dictionary with name form.

        # Update form with user details

        logindetails["form_rcdl:tf_dlNO"] = DL_NO
        logindetails.update(form)
        logindetails["form_rcdl:tf_dob_input"] = DOB
        logindetails.update(form)

        # url for captcha you can use getcaptcha() function here.
        captchaurl = "https://parivahan.gov.in/rcdlstatus/DispplayCaptcha?txtp_cd=1&bkgp_cd=2&noise_cd=2&gimp_cd=3&txtp_length=5&pfdrid_c=true?-1352556766&pfdrid_c=true"
        cimage = s.get(captchaurl)
        with open('DisplayCaptcha.png', 'wb') as f:
            f.write(cimage.content)
        captcha = input("Enter Captcha")
        logindetails["form_rcdl:j_idt34:CaptchaID"] =captcha  #update captcha into logindetails
        logindetails.update(form)

        # call POST request
        response = s.post(url2, data=logindetails, headers=headers)

        # store deatails after login in variable imp.
        imp = lxml.html.fromstring(response.content)
        #Cheking of login credentials
        try:
            output = response.text
            num2 = int(output.index("Verification code does not match"))
            captchaerror = output[num2:(num2 + 32)]
            print(captchaerror)
            return 1  #if captch not match will return to main
        except:
            try:
                output = response.text
                num=int(output.index("No DL"))
                error = output[num:(num+20)]
                print(error)
                return 2 #if DOB & DL. NO. not correct will return to main function
            except:
                # Data Scraping
                first_heading = imp.xpath('//*[@id="form_rcdl:j_idt118"]/div[1]/text()')
                second_heading = imp.xpath('//*[@id="form_rcdl:j_idt118"]/div[2]/text()')
                third_heading = imp.xpath('//*[@id="form_rcdl:j_idt118"]/div[3]/text()')

                # First table details
                param = []
                val = []
                for i in range(1, 6):
                    for j in range(1, 5):
                        userdetail1 = imp.xpath(
                            '//*[@id="form_rcdl:j_idt118"]/table[1]/tr[' + str(i) + ']/td[' + str(j) + ']/span/text()')
                        userdetail2 = imp.xpath(
                            '//*[@id="form_rcdl:j_idt118"]/table[1]/tr[' + str(i) + ']/td[' + str(j) + ']/text()')
                        if userdetail1 != []:
                            if (i == 1 and j == 2):
                                val.append(userdetail1[0])
                            else:
                                param.append(userdetail1[0])
                        if userdetail2 != []:
                            val.append(userdetail2[0])

                res1 = dict(zip(param, val))
                Dict = {}
                h1 = first_heading[0]
                Dict[h1[29:73]] = res1

                # Second table Contents

                param2 = []
                val2 = []
                for a in range(1, 4):
                    for b in range(1, 4):
                        userdetail3 = imp.xpath(
                            '//*[@id="form_rcdl:j_idt118"]/table[2]/tr[' + str(a) + ']/td[' + str(b) + ']/span/text()')
                        userdetail4 = imp.xpath(
                            '//*[@id="form_rcdl:j_idt118"]/table[2]/tr[' + str(a) + ']/td[' + str(b) + ']/text()')
                        if userdetail3 != []:
                            param2.append(userdetail3[0])
                        if userdetail4 != []:
                            val2.append(userdetail4[0])

                param2.pop(3)
                param2.pop(0)
                param3 = [param2[0], param2[1]]
                val3 = [val2[0], val2[1]]
                param2.pop(0)
                param2.pop(0)
                val2.pop(0)
                val2.pop(0)
                res2 = dict(zip(param2, val2))
                res3 = dict(zip(param3, val3))
                Dict1 = {}
                Dict1['Non-Transport'] = res3
                Dict2 = {}
                Dict2['Transport'] = res2
                Dict1.update(Dict2)

                param4 = []
                val4 = []
                for c in range(1, 5):
                    userdetail5 = imp.xpath('//*[@id="form_rcdl:j_idt118"]/table[3]/tr/td[' + str(c) + ']/span/text()')
                    userdetail6 = imp.xpath('//*[@id="form_rcdl:j_idt118"]/table[3]/tr/td[' + str(c) + ']/text()')
                    if userdetail5 != []:
                        param4.append(userdetail5[0])
                    if userdetail6 != []:
                        val4.append(userdetail6[0])
                res4 = dict(zip(param4, val4))
                Dict1.update(res4)
                Dict2 = {}
                h2 = second_heading[0]
                Dict2[h2[29:61]] = Dict1
                Dict.update(Dict2)

                # Table 3 contents
                param5 = []
                val5 = []
                userdetail7 = imp.xpath('//*[@id="form_rcdl:j_idt167:j_idt168"]/span/text()')
                param5.append(userdetail7[0])

                userdetail8 = imp.xpath('//*[@id="form_rcdl:j_idt167:j_idt170"]/span/text()')
                param5.append(userdetail8[0])

                userdetail9 = imp.xpath('//*[@id="form_rcdl:j_idt167:j_idt172"]/span/text()')
                param5.append(userdetail9[0])

                userdetail10= imp.xpath('//*[@id="form_rcdl:j_idt167_data"]/tr/td[1]/text()')
                val5.append(userdetail10[0])
                userdetail11 = imp.xpath('//*[@id="form_rcdl:j_idt167_data"]/tr/td[2]/text()')
                val5.append(userdetail11[0])
                userdetail12 = imp.xpath('//*[@id="form_rcdl:j_idt167_data"]/tr/td[3]/text()')
                val5.append(userdetail12[0])
                res5 = dict(zip(param5, val5))
                Dict3 = {}
                h3 = third_heading[0]
                Dict3[h3[29:53]] = res5
                Dict.update(Dict3)
                #save JSON file
                app_json = json.dumps(Dict)
                with open('outputfile.json', 'w') as fp:
                    json.dump(app_json, fp)
                return 3



if __name__=="__main__":
    Note = '''Note:Driving Licence number can be entered in any of the following formats: DL-1420110012345 or DL14 20110012345
    Total number of input characters should be exactly 16 (including space or '-').
    If you hold an old driving license with a different format, please convert the format as per below rule before entering.
    SS-RRYYYYNNNNNNN OR SSRR YYYYNNNNNNN
    Where
    SS - Two character State Code (like RJ for Rajasthan, TN for Tamil Nadu etc)
    RR - Two digit RTO Code
    YYYY - 4-digit Year of Issue (For Example: If year is mentioned in 2 digits, say 99, then it should be converted to 1999. Similarly use 2012 for 12).
    Rest of the numbers are to be given in 7 digits. If there are less number of digits, then additional 0's(zeros) may be added to make the total 7.
    For example: If the Driving Licence Number is RJ-13/DLC/12/ 123456 then please enter RJ-1320120123456 OR RJ13 20120123456.
    Date of Birth can be entered in any of the following formats: DD-MM-YYYY'''

    print(Note + "\n")

    # demand user for Driving Licence Number
    DL_NO = input('Enter Driving Licence No. : ')

    # demand user for Date of Birth
    DOB = input('Date Of Birth. : ')
    result = session()
    while True:
        if result==1:
            result=session()
        elif result==2:
            DL_NO = input('Enter Driving Licence No. : ')
            DOB = input('Date Of Birth. : ')
            result = session()
        elif result ==3:
            break
    print("JSON file Created Successfuly")

