# Author: Leif Johanson
# Date: November 21, 2019
# Description: Cancer Classification Using Machine Learning for A5

###############################################################################
# GLOBAL CONSTANT
# For use as dictionary keys
# You can use this list throughout the program without passing it to a function
# DO NOT MODIFY
ATTRS = []
ATTRS.append("ID")
ATTRS.append("radius")
ATTRS.append("texture")
ATTRS.append("perimeter")
ATTRS.append("area")
ATTRS.append("smoothness")
ATTRS.append("compactness")
ATTRS.append("concavity")
ATTRS.append("concave")
ATTRS.append("symmetry")
ATTRS.append("fractal")
ATTRS.append("class")
###############################################################################


def make_training_set(filename):
    """ Read trainig data from the file whose path is filename.
        Return a list of records, where each record is a dictionary
        containing a value for each of the 12 keys in ATTRS.
    """
    # COMPLETE - DO NOT MODIFY
    training_records = []
    # Read in file
    for line in open(filename,'r'):
        if '#' in line:
            continue
        line = line.strip('\n')
        line_list = line.split(',')
        
        # Create a dictionary for the line and map the attributes in
        # ATTRS to the corresponding values in the line of the file
        record = {}
        
        # read patient ID as an int:
        record[ATTRS[0]] = int(line_list[0].strip())
        
        # read attributes 1 through 10 as floats:
        for i in range(1,11):
            record[ATTRS[i]] = float(line_list[i])
        
        # read the class (label), which is "M", or "B" as a string:
        record[ATTRS[11]] = line_list[31].strip() 

        # Add the dictionary to a list
        training_records.append(record)        

    return training_records


def make_test_set(filename):
    """ Read test data from the file whose path is filename.
        Return a list with the same form as the training
        set, except that each dictionary has an additional
        key "prediction" initialized to "none" that will be
        used to store the label predicted by the classifier. 
    """
    # COMPLETE - DO NOT MODIFY
    test_records = make_training_set(filename)

    for record in test_records:
        record["prediction"] = "none"

    return test_records

def get_avg_m(training_records):
    """Helper function for train_classifier. Takes the training records from the text file as the single argument. It then creates a blank dictionary and adds to it
    if the tumor is malignant. It then takes the total of all the numbers for each attribute and divides it by the total amount of
    malignant tumors there were.
    Precondition: training_records is a list of patient record
                  dictionaries
    Postcondition: The return value dict_m_avg is a dictionary containing all the attributes of the malignant tumors with all of
    the average values"""
    # dictionary with all the values set to zero
    dict_m = {"radius": 0, "texture": 0, "perimeter": 0, "area": 0, "smoothness": 0, "compactness": 0, "concavity": 0, "concave": 0, "symmetry": 0, "fractal": 0, "class": 0}
    count = 0
    # indexes all the values and adds them to the total
    for line in training_records:
        if "M" in line["class"]:
            dict_m["radius"] = dict_m["radius"] + line["radius"]
            dict_m["texture"] = dict_m["texture"] + line["texture"]
            dict_m["perimeter"] = dict_m["perimeter"] + line["perimeter"]
            dict_m["area"] = dict_m["area"] + line["area"]
            dict_m["smoothness"] = dict_m["smoothness"] + line["smoothness"]
            dict_m["compactness"] = dict_m["compactness"] + line["compactness"]
            dict_m["concavity"] = dict_m["concavity"] + line["concavity"]
            dict_m["concave"] = dict_m["concave"] + line["concave"]
            dict_m["symmetry"] = dict_m["symmetry"] + line["symmetry"]
            dict_m["fractal"] = dict_m["fractal"] + line["fractal"]
            count += 1
    # averages each line
    dict_m_avg = {"radius": 0, "texture": 0, "perimeter": 0, "area": 0, "smoothness": 0, "compactness": 0, "concavity": 0, "concave": 0, "symmetry": 0, "fractal": 0, "class": 0}
    (dict_m_avg["radius"]) = dict_m["radius"] / count
    (dict_m_avg["texture"]) = dict_m["texture"] / count
    (dict_m_avg["perimeter"]) = dict_m["perimeter"] / count
    (dict_m_avg["area"]) = dict_m["area"] / count
    (dict_m_avg["smoothness"]) = dict_m["smoothness"] / count
    (dict_m_avg["compactness"]) = dict_m["compactness"] / count
    (dict_m_avg["concavity"]) = dict_m["concavity"] / count
    (dict_m_avg["concave"]) = dict_m["concave"] / count
    (dict_m_avg["symmetry"]) = dict_m["symmetry"] / count
    (dict_m_avg["fractal"]) = dict_m["fractal"] / count
    
    return dict_m_avg

def get_avg_b(training_records):
    """Helper function for train_classifier. Takes the training records from the text file as the single argument. It then creates a blank dictionary and adds to it
    if the tumor is benign. It then takes the total of all the numbers for each attribute and divides it by the total amount of
    benign tumors there were.
    Precondition: training_records is a list of patient record
                  dictionaries
    Postcondition: The return value dict_b_avg is a dictionary containing all the attributes of the benign tumors with all of
                   the average values"""
    # starting dictionary
    dict_ = {"radius": 0, "texture": 0, "perimeter": 0, "area": 0, "smoothness": 0, "compactness": 0, "concavity": 0, "concave": 0, "symmetry": 0, "fractal": 0, "class": 0}
    count = 0
    for line in training_records:
        if "B" in line["class"]:
            # indexes all the values and adds them to the total
            dict_["radius"] = dict_["radius"] + line["radius"]
            dict_["texture"] = dict_["texture"] + line["texture"]
            dict_["perimeter"] = dict_["perimeter"] + line["perimeter"]
            dict_["area"] = dict_["area"] + line["area"]
            dict_["smoothness"] = dict_["smoothness"] + line["smoothness"]
            dict_["compactness"] = dict_["compactness"] + line["compactness"]
            dict_["concavity"] = dict_["concavity"] + line["concavity"]
            dict_["concave"] = dict_["concave"] + line["concave"]
            dict_["symmetry"] = dict_["symmetry"] + line["symmetry"]
            dict_["fractal"] = dict_["fractal"] + line["fractal"]
            count += 1
    # averages each line
    dict_b_avg = {"radius": 0, "texture": 0, "perimeter": 0, "area": 0, "smoothness": 0, "compactness": 0, "concavity": 0, "concave": 0, "symmetry": 0, "fractal": 0, "class": 0}
    
    (dict_b_avg["radius"]) = dict_["radius"] / count
    (dict_b_avg["texture"]) = dict_["texture"] / count
    (dict_b_avg["perimeter"]) = dict_["perimeter"] / count
    (dict_b_avg["area"]) = dict_["area"] / count
    (dict_b_avg["smoothness"]) = dict_["smoothness"] / count
    (dict_b_avg["compactness"]) = dict_["compactness"] / count
    (dict_b_avg["concavity"]) = dict_["concavity"] / count
    (dict_b_avg["concave"]) = dict_["concave"] / count
    (dict_b_avg["symmetry"]) = dict_["symmetry"] / count
    (dict_b_avg["fractal"]) = dict_["fractal"] / count
    
    return dict_b_avg

def midpoint(dict_b, dict_m):
    """Helper function for train_classifier. Takes two dictionaries (one is average values of benign tumors, the other the
    same with malignant) as arguments and indexes each of them for each attribute. It then finds the midpoint between the value of
    each attribute.
        Postcondition: Returns final_dictionary, which contains midpoint for each attribute."""
    # indexes each value and finds the midpoint between them
    radius_mid = (dict_b["radius"] + dict_m["radius"]) / 2
    texture_mid = (dict_b["texture"] + dict_m["texture"]) / 2
    perimeter_mid = (dict_b["perimeter"] + dict_m["perimeter"]) / 2
    area_mid = (dict_b["area"] + dict_m["area"]) / 2
    smoothness_mid = (dict_b["smoothness"] + dict_m["smoothness"]) / 2
    compactness_mid = (dict_b["compactness"] + dict_m["compactness"]) / 2
    concavity_mid = (dict_b["concavity"] + dict_m["concavity"]) / 2
    concave_mid = (dict_b["concave"] + dict_m["concave"]) / 2
    symmetry_mid = (dict_b["symmetry"] + dict_m["symmetry"]) / 2
    fractal_mid = (dict_b["fractal"] + dict_m["fractal"]) / 2
    
    final_dictionary = {"radius": radius_mid, "texture": texture_mid, "perimeter": perimeter_mid, "area": area_mid, "smoothness": smoothness_mid, "compactness": compactness_mid, "concavity": concavity_mid, "concave": concave_mid, "symmetry": symmetry_mid, "fractal": fractal_mid}
    
    return final_dictionary

def train_classifier(training_records):
    """ Return a dict containing the midpoint between averages
        among each class (malignant and benign) of each attribute.
        (See the A5 writeup for a more complete description)
        Precondition: training_records is a list of patient record
                      dictionaries, each of which has the keys
                      in the global variable ATTRS
        Postcondition: the returned dict has midpoint values calculated
                       from the training set for all 10 attributes except
                       "ID" and"class".
    """
    # gets the two dictionaries with the average benign and malignant values and finds
    # the midpoint
    final = midpoint(get_avg_m(training_records), get_avg_b(training_records))
    
    return final

def m_or_b_count(attribute, line, classifier):
    """Helper function for mid_check function. For each line, it calculates whether the value of the midpoint
    list is greater or equal to the value of each attribute in the dictionary. If the test_record dictionary
    is less than the midpoint, it is marked as true, and counts as one benign vote, and vice versa.
    Preconditions: attribute is the attribute (radius, texture, etc) as a string. line is a single dictionary
                   from test_records.
    Postconditions: The return value t_or_f is whether the attribute is true of false."""
    if float(classifier[attribute]) >= float(line[attribute]):
        t_or_f = True
    else:
        t_or_f = False
    return t_or_f

def mid_check(line, classifier):
    """Helper function for the classify function. Uses the m_or_b_count function as a helper function
    to make function shorter.
    Precondition: line is a dictionary from test_records. classifier is a dictionary with all the
                  midpoints.
    Postcondition: The return value is a tuple with arguments of either True or False. """
    rad = m_or_b_count("radius", line, classifier)
    tex = m_or_b_count("texture", line, classifier)
    per = m_or_b_count("perimeter", line, classifier)
    area = m_or_b_count("area", line, classifier)
    smo = m_or_b_count("smoothness", line, classifier)
    comp = m_or_b_count("compactness", line, classifier)
    concavity = m_or_b_count("concavity", line, classifier)
    concave = m_or_b_count("concave", line, classifier)
    sym = m_or_b_count("symmetry", line, classifier)
    fra = m_or_b_count("fractal", line, classifier)
    
    return rad, tex, per, area, smo, comp, concavity, concave, sym, fra

def classify(test_records, classifier):
    """ Use the given classifier to make a prediction for each record in
        test_records, a list of dictionary patient records with the keys in
        the global variable ATTRS. A record is classified as malignant
        if at least 5 of the attribute values are above the classifier's
        threshold.
        Precondition: classifier is a dict with midpoint values for all
                      keys in ATTRS except "ID" and "class"
        Postcondition: each record in test_records has the "prediction" key
                       filled in with the predicted class, either "M" or "B"
    """
    # TODO 2 - implement this function
    # counts the true and false values and assigns it to either benign of malignant
    for line in test_records:
        a = mid_check(line, classifier)
        if int(a.count(True)) > int(a.count(False)):
            line["prediction"] = "B"
        else:
            line["prediction"] = "M"

def report_accuracy(test_records):
    """ Print the accuracy of the predictions made by the classifier
        on the test set as a percentage of correct predictions.
        Precondition: each record in the test set has a "prediction"
        key that maps to the predicted class label ("M" or "B"), as well
        as a "class" key that maps to the true class label. """
    # TODO 3 - implement this function
    correct_count = 0
    incorrect_count = 0
    # if the prediction value = the actual "M" of "B" value
    for line in test_records:
        if line["prediction"] == line["class"]:
            correct_count += 1
        else:
            incorrect_count += 1
    total = correct_count + incorrect_count
    print((correct_count/total)*100)

def table_line(line, classifier, ID):
    """Helper function for table_of_results. Starts with a list of all the attributes,
    and then goes through and prints the attribute, the test_records value"""
    attribute_list = ["radius", "texture", "perimeter", "area", "smoothness", "compactness", "concavity", "concave", "symmetry", "fractal"] 
    # Go through each attribute and prine a line of the table
    for attribute in attribute_list:
        if line[attribute] >= classifier[attribute]:
            vote = "Malignant"
        else:
            vote = "Benign"
        print(attribute.rjust(13), str("{:.4f}".format(line[attribute]).rjust(13)),
              str("{:.4f}".format(classifier[attribute]).rjust(13)), vote.rjust(13))

def table_of_results(test_records, classifier, ID):
    """Helper function for check_patients. It goes thorugh each line in test_records
    and prints the table using the table_line function."""
    check = False
    for line in test_records:
        if ID == str(line["ID"]):
            print()
            check = True
            print("Attribute".rjust(13), "Patient".rjust(13), "Classifier".rjust(13), "Vote".rjust(13))
            table_line(line, classifier, ID)
            # if line["prediction'] equals M or B
            if line["prediction"] == "B":
                print("Classifier's diagnosis: Benign")
            else:
                print("Classifier's diagnosis: Malignant")
            break
    if check == False:
            print("The ID provided is not in the test set.")

def check_patients(test_records, classifier):
    """ Repeatedly prompt the user for a Patient ID until the user
        enters "quit". For each patient ID entered, search the test
        set for the record with that ID, print a message and prompt
        the user again. If the patient is in the test set, print a
        table: for each attribute, list the name, the patient's value,
        the classifier's midpoint value, and the vote cast by the
        classifier. After the table, output the final prediction made
        by the classifier.
        If the patient ID is not in the test set, print a message and
        repeat the prompt. Assume the user enters an integer or quit
        when prompted for the patient ID.
    """
    # TODO 4 - implement this function
    
    # Pseudocode:
    
    # prompt user for an ID
    ID = str(input("Enter a patient ID to access classification details: "))
    # while the user has not entered "quit":
    while ID != "quit":
        # determine whether the entered patient ID is in the test set
        # if it is,
            # print a table of results (see the handout and sample output)
        table_of_results(test_records, classifier, ID)
        # otherwise,
            # print a message saying the patient ID wasn't found
        ID = str(input("Enter another ID: "))
        # prompt the user for anoher ID


if __name__ == "__main__":
    # Main program - COMPLETE
    # Do not modify except to uncomment each code block as described.
    
    # load the training set
    print("Reading in training data...")
    training_data_file = "cancerTrainingData.txt"
    training_set = make_training_set(training_data_file)
    print("Done reading training data.")
    
    # load the test set 
    print("Reading in test data...")
    test_file = "cancerTestingData.txt"
    test_set = make_test_set(test_file)
    print("Done reading test data.\n")

    # train the classifier: uncomment this block once you've
    # implemented train_classifier
    print("Training classifier..."    )
    classifier = train_classifier(training_set)
    print("Classifier cutoffs:")
    for key in ATTRS[1:11]:
        print("    ", key, ": ", classifier[key], sep="")
    print("Done training classifier.\n")
    # use the classifier to make predictions on the test set:
    # uncomment the following block once you've written classify
    # and report_accuracy
    print("Making predictions and reporting accuracy")
    classify(test_set, classifier)
    report_accuracy(test_set)
    print("Done classifying.\n")

    # prompt the user for patient IDs and provide details on
    # the diagnosis: uncomment this line when you've
    # implemented check_patients
    check_patients(test_set, classifier)
