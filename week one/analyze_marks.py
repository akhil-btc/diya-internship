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
        reader = csv.reader(a)
        csv_list = list(reader)
    title = csv_list[0]
    data = csv_list[1:]
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
        student = row[0]
        score = []
        test = row[1:]
        for val in test:
            try:
                mark = int(val)
                score.append(mark)
            except:
                missing.append(student) #flaggs missing data 1/3
                score.append(0)
        student_average[student] = sum(score)/ len(score)
        stud_ave.append(student_average[student])
        #subjects averages
    for subject in subjects:
        index+= 1
        sub_score = []
        for row in data:
            test = row[1:]
            try:
                mark = int(test[index])
                sub_score.append(mark)
            except:
                mark = 0
                sub_score.append(mark)
        sub_average = sum(sub_score)/ len(sub_score)
        sub_average = round(sub_average, 3)
        print(subject + " average: ", str(sub_average))  
                
        #student averages #2/3
    stud_ave.sort()
    highest = stud_ave[-1]
    for stud in student_average:
        if student_average[stud] == highest:
            print("student with highest average: ", stud, "with an average of ", str(highest)) 




missing = []
write("anaylze_marks.csv", rows)
title, data = read("anaylze_marks.csv")
average(title, data)
for elem in missing:
    count = missing.count(elem)
    if count > 1:
        missing.remove(elem)
print("students with misssing data: ", end = "")
for miss in missing:
    print(miss, end = ", ")