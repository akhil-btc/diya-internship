import csv
rows = [
    ["student_name", "math", "science", "english", "history"],



    ["Arjun", 60, 54, 75, 36],
    ["Kavya", 44, 47, 73, 37],
    ["Meera", 98, 99, 63, 34],
    ["Rohan", 45, 90, 76, 38],
    ["Priya", 55, 46, 85, 84],
    ["Ved", 43, 50, 64, 37],
    ["Ishaan", 76, 85, 53, 58],
    ["Saanvi", 42, 52, 68, 83],
    ["Diya", 49, 50, 86, 69],
    ["Aarav", 75, 58, 56, 54],
    ["Akhil", "N/A", 78, 82, "absent"],
    ["Neha", 91, "N/A", 88, 74]
]

def write(csv_file, rows):
    with open(csv_file, "w", newline="") as a:
        writer = csv.writer(a)
        writer.writerows(rows)
def read(csv_file):
    with open(csv_file, "r", newline="") as a:
        try:
            reader = csv.reader(a)
            csv_list = list(reader)
            title = csv_list[0]
            data = csv_list[1:]
        except FileNotFoundError:
            title = []
            data = []
            print("file not found! exiting")
    #[sttudents, ///jjjj riw 2 students, data data]///
    return title, data
def average(title, data): #calculate average per subject
    global missing
    student_average = {}
    stud_ave = []
    index = -1
    # four subjects, 5 items 
    subjects = title[1:]
    for row in data:
        try:
            student = row[0]
            score = []
            test = row[1:]
            for val in test:
                try:
                    mark = int(val)
                    score.append(mark)
                except ValueError:
                    print(student +"'s Score ", "couldn't be converted to an integer!")
                    missing.append(student) #flaggs missing data 1/3
                    score.append(0)
            student_average[student] = sum(score)/ len(score)
            stud_ave.append(student_average[student])
        except IndexError:
            print("Row doesn't exist; skipping;")
            continue
            #subjects averages
    for subject in subjects:
        index+= 1
        sub_score = []
        for row in data:
            try:
                test = row[1:]
                try:
                    mark = int(test[index])
                    sub_score.append(mark)
                except ValueError :
                    print(row[0], "'s Score in ", subject, "couldn't be converted to an integer! scoring as 0")
                    mark = 0
                    sub_score.append(mark)
            except IndexError:
                print("Row doesn't exist; skipping;")
                continue
        sub_average = sum(sub_score)/ len(sub_score)
        sub_average = round(sub_average, 3)
        print(subject + " average: ", str(sub_average))  
                
        #student averages #2/3
    stud_ave.sort()
    first = stud_ave[-1]
    second = stud_ave[-2]
    third = stud_ave[-3]
    for stud in student_average:
        if student_average[stud] == first:
            print("student with highest average: ", stud, "with an average of ", str(first)) 
        elif student_average[stud] == second:
            print("student with second highest average: ", stud, "with an average of ", str(second))
        elif student_average[stud] == third:
            print("student with third highest average: ", stud, "with an average of ", str(third))




missing = []
 
write("robust_analyze.csv", rows)
expected = ["student_name", "math", "science", "english", "history"]
title, data = read("robust_analyze.csv")
if title != expected:
    print("The file has unexpected columns")
    print("expected: ", expected)
    print("found: ", title)
average(title, data)
for elem in missing:
    count = missing.count(elem)
    if count > 1:
        missing.remove(elem)
print("students with misssing data: ", end = "")
for miss in missing:
    print(miss, end = ", ")
#What happens if the file doesn't exist?
#Title, data = read("analysis.csv")
    #if the file doesn't exist, we will be notified,
    #and the program will return a black list for the title and data,
    #being able to be used for the remainder of the program wirhour crashing.
#What happens if a row is missing a score?
#Rohan,82,20,49
    # if a row is missing a score, it will notify us of missing data and 
    # skip the data for that row, using continue to go back to the loop, without 
    # leaving an error.
#What happens if a score says "absent"?
#Akhil,N/A,78,82,absent
    #if a score says absent, it will notify us of missing data and mark
    # the score as 0, doing the proper calculations with 0 as the score.
#What happens with an empty CSV?
#rows = []
#write("robust_analyze.csv", rows)
    #the program will run with an empty file, notifying us that there is missing code,
    #and will print results with no data.