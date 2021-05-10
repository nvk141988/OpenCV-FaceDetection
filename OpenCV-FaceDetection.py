from zipfile import ZipFile
from PIL import Image
import cv2 as cv
import io
from PIL import ImageDraw
import IPython.display as display
#Using haar cascade classifier for face detection
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
#Zip with images to analyze
imges_zip = "images.zip"

#get cropped image according to bounding box provided
def getFaceImage(img, box):
    img = img.crop(box)
    # img = img.thumbnail((20,20))
    return (img)

#Extract image and image names from zip
def getSrcFileName():
    filenames = []
    names = []
    file_name = "images.zip"
    with ZipFile(file_name, 'r') as zip:
        for info in zip.infolist():
            # zip.printdir()
            img = Image.open(io.BytesIO(zip.read(info.filename)))
            names.append(info.filename)
            filenames.append(img)
    return (filenames, names)

#Create a portrait of extracted images
def createContactSheet(faces):
    # print("Type of faces:",type(faces))
    noOfImages = len(faces)
    # print(noOfImages)
    contact_sheet = Image.new("RGB", ((100 * noOfImages), (100)))
    x = 0
    y = 0
    for face in faces:
        contact_sheet.paste(face, (x, y))
        if x + 100 == contact_sheet.width:
            x = 0
            y = y + 100
        else:
            x = x + 100
    contact_sheet = contact_sheet.convert("RGBA")
    #display(contact_sheet) #To see results in JupyterLab
    #cv.imshow("Results",np.array(contact_sheet))
    return(contact_sheet)

#Extract faces from image and return a portrait of faces
def extractFaces(img, faces):
    results = []
    if len(faces) != 0:
        # Set our drawing context
        drawing = ImageDraw.Draw(img)
        # And plot all of the rectangles in faces
        for x, y, w, h in faces:
            drawing.rectangle((x, y, x + w, y + h), outline="white")
            results.append(getFaceImage(img, (x, y, x + w, y + h)))
        # Finally lets display this
        for result in results:
            result.thumbnail((100, 100))
            # display(result)
        output = createContactSheet(results)
        return output
    else:
        print("But there are no faces in that file")
    

#detect faces in image
def detectFacesOnPage(pageIndex):
    pages, names = getSrcFileName()
    pages[pageIndex].save('Page.png')
    # display(Image.open('Page.png'))
    img = cv.imread('Page.png')
    faces = face_cascade.detectMultiScale(img, 1.35)
    # print("No of faces=",len(faces))
    out=extractFaces(pages[pageIndex], faces)
    return out


#Main of the code
#Get filenames from zip
data = getSrcFileName()

i = 0
output_faces=[]
for file, face in zip(data[0], data[1]):
    print("Results found in {}".format(face))
    output_faces.append(detectFacesOnPage(i))
    display.display(output_faces[i])
    i += 1

    