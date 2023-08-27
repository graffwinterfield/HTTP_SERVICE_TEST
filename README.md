![image](https://github.com/graffwinterfield/HTTP_SERVICE_TEST/assets/110451740/994146ce-3a18-4370-95a4-f8da81598c23)Simple web_http service for upload files csv and xlsx


[Install]
pip install -r requirments.txt

[Uasge]
1. First you  need sign up in site with address http://127.0.0.1:5000/sigup/ for create account 
2. Go to address http://127.0.0.1:5000/login/ and login to your account
3. There you will see buttons list_files and upload
4. you can upload your csv file or delete it if you need
5. use filters like column_name:key
Example of filter:
data = {'EEID': 'E02387', 'Full Name': 'Emily Davis', 'Job Title': 'Sr. Manger', 'Department': 'IT', 'Business Unit': 'Research & Development', 'Gender': 'Female', 'Ethnicity': 'Black', 'Age': 55, 'Hire Date': '4/8/2016', 'Annual Salary': '$141,604 ', 'Bonus %': '15% ', 'Country': 'United States', 'City': 'Seattle', 'Exit Date': '10/16/2021'}
{'EEID': 'E04105', 'Full Name': 'Theodore Dinh', 'Job Title': 'Technical Architect', 'Department': 'IT', 'Business Unit': 'Manufacturing', 'Gender': 'Male', 'Ethnicity': 'Asian', 'Age': 59, 'Hire Date': '11/29/1997', 'Annual Salary': '$99,975 ', 'Bonus %': '0% ', 'Country': 'China', 'City': 'Chongqing', 'Exit Date': nan}
filter: <Full Name:Emily Davis> sort:<Department:IT>

![alt text]([http://url/to/img.png](https://github.com/graffwinterfield/HTTP_SERVICE_TEST/assets/110451740/ec0147f8-4993-474c-9c1f-45d0e91286a9)https://github.com/graffwinterfield/HTTP_SERVICE_TEST/assets/110451740/ec0147f8-4993-474c-9c1f-45d0e91286a9)
