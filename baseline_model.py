def helper_merge_two_dicts(d1, d2):
    d = d1
    for keys in d2:
        d[keys] += d2[keys]
    return d


bm_dict = {}
with open("Data_Entry_2017.csv", mode="r") as file:
    for i in file.readlines()[1:]:
        line_list = i.split(",")
        age_and_gender = str(line_list[4] + line_list[5])
        diseases = {"Cardiomegaly":0, "No Finding":0, "Effusion":0, "Infiltration":0, "Mass":0}
        types = line_list[1].split("|")
        for i in types:
            if i in diseases:
                diseases[i] += 1

        if age_and_gender in bm_dict:
            d1 = bm_dict[age_and_gender]
            d2 = diseases
            bm_dict[age_and_gender] = helper_merge_two_dicts(d1, d2)
        else:
            bm_dict[age_and_gender] = diseases
    # for i in bm_dict:
    #     if max(bm_dict[i].values()) != bm_dict[i]["No Finding"]:
    #         print(i)


def helper_find_key(d: dict):
    max_value = max(d.values())
    res = ""
    for i in d:
        if d[i] == max_value:
            if res != "":
                res += " or "
            res += i

    return res


def get_baseline_model(age, gender):
    if not isinstance(age, int) or gender not in ["M", "F"] or age not in range(0, 155):
        print("the input is incorrect")
    input_key = str(str(age) + gender)
    gender_string = "female"
    if gender == "M":
        gender_string = "male"
    print("a", age, "years old", gender_string, "'s most likely medical condition is:", helper_find_key(bm_dict[input_key]))


get_baseline_model(90, "F")
get_baseline_model(80, "F")
get_baseline_model(91, "M")
