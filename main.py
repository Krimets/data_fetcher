import csv
import json
import requests

# Refine fetches data
print('Hello, please, input data, like: date, campaign, clicks')
fields = input().replace(' ', '').split(',')
print('Now input the URL for the file, like: https://drive.google.com/file/d/13F7qRnIQC0buvWuxX8GvUG5yEwAJ6vnP/view')
url = input().replace(' ', '').split('/')
url = f'https://drive.google.com/uc?id={url[5]}'


def json_former(row4):
    # save the result
    with open('data.json', 'w') as outfile:
        json.dump(row4, outfile)


def task_file_downloader():
    # Connecting to google drive and downloading data
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) "
                             "Chrome/92.0.4515.131 Safari/537.36"}
    client = requests.Session()
    response = client.get(url, headers=headers)
    print(response.status_code)
    file_type = 'csv'
    with open(f"task_file.{file_type}", "wb") as task_file:
        task_file.write(response.content)


def main():
    # Connecting to google drive and downloading data
    task_file_downloader()

    # Specifying what data to collect
    with open('task_file.csv') as task_file:  # open file
        reader = csv.reader(task_file)  # read file as reader
        row_master = []  # create row master
        field_master = []  # create field master

        for row in reader:  # Looping the lines of a task_file
            # Specifying data to collect
            for field in fields:
                for i in range(len(fields)):
                    try:
                        if field == row[i] and field not in field_master and field != '':
                            row_master.append(i)
                            field_master.append(field)
                    except:
                        pass

        # Sorting data
        # If we collect more than one value
        if len(row_master) > 1:
            field_master2 = []
            row_master2 = row_master.copy()
            row_master2.sort()
            for i in row_master2:
                if i == row_master[i]:
                    field_master2.append(field_master[i])
                else:
                    field_master2.append(field_master[row_master[i]])
        else:
            # If we collect only one value
            field_master2 = field_master
            row_master2 = row_master

        # flush memory
        task_file.flush()

        data_dict = {}  # Create an empty dictionary
        data_array = []  # Create an empty array
        data = {}  # Create an empty dictionary

        with open('task_file.csv') as task_file:  # open file
            reader = csv.reader(task_file)  # read file as reader
            for row in reader:
                if row[0] == 'date':
                    pass
                else:
                    for i in row_master2:
                        # If we collect more than one value
                        if len(row_master2) > 1:
                            data_dict[field_master2[i]] = row[i]  # Collecting values
                        else:
                            # If we collect only one value
                            data_dict[field_master2[0]] = row[i]  # Collecting values
                    data_array.append(data_dict)  # Collecting data in array
                    data_dict = {}  # Clearing the dictionary
                data['data'] = data_array
        json_former(data)


if __name__ == '__main__':
    main()
