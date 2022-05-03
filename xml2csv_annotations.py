import xml.etree.ElementTree as ET
import csv
import os

work_dir = "C:/Users/arno/Documents/fourthbrain/capstone/data/"
img_dir = work_dir + "training/"
orig_dir = work_dir + 'lesion_annotations/'
labels = open(work_dir + 'labels/labels_test3.txt', 'w', newline='')

listOfFiles = list()
listOfFileNames = list()
for (dirpath, dirnames, filenames) in os.walk(img_dir):
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]
    listOfFileNames += filenames
#print(listOfFileNames)
#print(listOfFiles)

csvwriter = csv.writer(labels)

files_labeled = os.listdir(orig_dir)
#print(files_labeled)

for tif in listOfFiles:
    #print(tif[-22:-4])
    match = [s[:-4] for s in files_labeled if tif[-22:-4] in s[:-4]]
    #print(match)
    folder = tif[-31:-23]
    #print(folder)

    if len(match) == 0:
        filename = "@"+ folder + "/" + tif
        #csvwriter.writerow([filename])
        zeile = "0 0 # healthy"
        #csvwriter.writerow([zeile])

    else:
        filename = "@"+ folder + "/" + str(match[0]) + ".tif"
        print(filename)
        csvwriter.writerow([filename])
        tree = ET.parse(os.path.join(orig_dir, str(match[0]) + ".xml"))
        root = tree.getroot()

        test_head = []
        for annotations in root.findall('Annotations'):
            count_h= -1
            count_m = -1
            for annotation in annotations:
                order = 0
                coord = []
                
                for coordinates in annotation.find('Coordinates'):
                    order = coordinates.attrib['Order']
                    coord.append([coordinates.attrib['X'] + " " + coordinates.attrib['Y']])

                anntype = -1
                zeile = ""
                if annotation.attrib['PartOfGroup'] == "healthy":
                    anntype = 0
                    count_h += 1
                    zeile = str(anntype) + " " + str(count_h) + " " + str(int(order) + 1) + " # " + annotation.attrib['PartOfGroup']
                
                elif annotation.attrib['PartOfGroup'] == "metastases":
                    anntype = 1
                    count_m += 1
                    zeile = str(anntype) + " " + str(count_m) + " " + str(int(order) + 1) + " # " + annotation.attrib['PartOfGroup']

                #ann = annotation.attrib['Name']
                #zeile = str(anntype) + " " + str(int(order) + 1) + " # " + annotation.attrib['PartOfGroup']
                csvwriter.writerow([zeile])

                for coo in coord:
                    csvwriter.writerow(coo)

labels.close()
print("fertich")