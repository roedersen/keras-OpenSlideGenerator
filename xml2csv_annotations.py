import xml.etree.ElementTree as ET
import csv
import os

work_dir = "C:/Users/arno/Documents/fourthbrain/capstone/data/"
img_dir = work_dir + "training/"
orig_dir = work_dir + 'lesion_annotations/'
labels = open(work_dir + 'labels/labels_test2.txt', 'w', newline='')

listOfFiles = list()
listOfFileNames = list()
for (dirpath, dirnames, filenames) in os.walk(img_dir):
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]
    listOfFileNames += filenames
print(listOfFileNames)

csvwriter = csv.writer(labels)

files_labeled = os.listdir(orig_dir)
print(files_labeled)

for tif in listOfFileNames:
    #print(tif[:-4])
    match = [s[:-4] for s in files_labeled if tif[:-4] in s[:-4]]
    #print(match)

    if len(match) == 0:
        filename = "@"+ tif
        #csvwriter.writerow([filename])
        zeile = "0 0 # healthy"
        #csvwriter.writerow([zeile])

    else:
        filename = "@"+ str(match[0]) + ".tif"
        print(filename)
        csvwriter.writerow([filename])
        tree = ET.parse(os.path.join(orig_dir, str(match[0]) + ".xml"))
        root = tree.getroot()

        test_head = []
        for annotations in root.findall('Annotations'):
            for annotation in annotations:
                order = 0
                coord = []
                
                for coordinates in annotation.find('Coordinates'):
                    order = coordinates.attrib['Order']
                    coord.append([coordinates.attrib['X'] + " " + coordinates.attrib['Y']])

                ann = annotation.attrib['Name']
                zeile = str(ann.split(" ")[1]) + " " + str(int(order) + 1) + " # " + annotation.attrib['PartOfGroup']
                csvwriter.writerow([zeile])

                for coo in coord:
                    csvwriter.writerow(coo)

labels.close()