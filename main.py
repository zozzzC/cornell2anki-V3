from bs4 import BeautifulSoup
import shutil
import os.path
from pathlib import Path
import re
import urllib


html_file = input("Enter file name (must be inside Notion HTML files folder within current directory.)")
#location of images folder
images_path = Path.cwd() / 'HTML Files' / html_file
html_file = html_file + '.html'
html_path = Path.cwd()
html_path = html_path / 'HTML files' / html_file

#path where image files need to be transferred.

with open(html_path, encoding="utf8") as html_file:
	soup = BeautifulSoup(html_file, 'lxml')

#scrape for the title of the file to name the images later (among other things)
title = soup.find('title')
title = title.text

#text file that contains the info 
txt = ""

scrape_content = soup.find('div', class_='page-body') 
#page body is where all the main content is stored.

for front in soup.find_all("summary"): #gets the 'front' where front is an item
	front.children #gets non html-ed text

pageHasBeenRenamed = False
img_val = 0 #because the image is shown twice, count how many times it has been shown already. 
count = 0 #counts the amount of elements on the back of the card

#for front in details.find("summary"):
        #print(front) #gets the front of each card
for details in soup.find_all("details"):
    #details contains the front and back of each card

    for back_items in details:
        pre_change_BI = back_items
        back_items = str(back_items)
        if bool(re.search("summary", back_items)) == True:
              front = pre_change_BI.text
              itemFront = True

        elif bool(re.search("application/x-tex", back_items)) == True: #identify katex
              pre_change_BI = pre_change_BI.find("annotation")
              pre_change_BI = "\[" + pre_change_BI.text + "\]"

        elif bool(re.search("bulleted-list", back_items)) == True:
              pre_change_BI = "<li>" + pre_change_BI.text + "</li>"

        elif bool(re.search("em", back_items )) == True:
              pre_change_BI = "<em>" + pre_change_BI.text + "</em>"
        
        elif bool(re.search("strong", back_items)) == True: 
              pre_change_BI = "<strong>" + pre_change_BI.text + "</strong>"

        elif (bool(re.search("a href", back_items)) == True):
            if pageHasBeenRenamed == False:
                anki_path = Path.home()
                anki_path = anki_path / 'Library' / 'Application Support' / 'Anki2' / 'User 1' / 'collection.media'
                pre_change_BI = pre_change_BI.find('img')
            #once the image is found this will return an imgsrc, use regex to get the source only.
                pre_change_BI = str(pre_change_BI)
                link = re.search('"(.*)" ', pre_change_BI)
            #the below variable stores the path of the original image file
                OG_img = link.group(1)
                OG_file_name = OG_img.split("/")[1]                OG_file_name = urllib.parse.unquote(OG_file_name, encoding='utf-8', errors='replace')
                renamed_file = OG_img.split("/")[1]
                renamed_file = str(title + '_' + str(img_val) + renamed_file)
                renamed_file = urllib.parse.unquote(renamed_file, encoding='utf-8', errors='replace')
                renamed_OG_path = OG_img.split("/")[0]
                #this is in html encoding. return to unescaped form 
                renamed_OG_path = urllib.parse.unquote(renamed_OG_path, encoding='utf-8', errors='replace')
                print(renamed_OG_path)
                renamed_image_path = Path.cwd() / 'HTML Files' / renamed_OG_path / renamed_file 
            #assuming img folder is renamed to title only
                OG_img = Path.cwd() / 'HTML Files' / renamed_OG_path / OG_file_name
                os.rename(OG_img, renamed_image_path)
                pageHadBeenRenamed = True     
                img_val += 1
                shutil.move(renamed_image_path, anki_path)
                pre_change_BI = '<img src="' + renamed_file + '">'
            else:
                pageHadBeenRenamed = False
        else:
            pre_change_BI = pre_change_BI.text
        
        #this section is for formatting it into a text file. 
        if itemFront == True: 
            txt += "\n" + front + ' ; '
            itemFront = False
            count = 0 
        elif count > 0: 
        #else this means the item is a back item, now determine if it is the first or last item on that list.
             txt = txt + pre_change_BI + " <br> "
             count = count + 1
        else:
            txt = txt + pre_change_BI + " <br> "
            count = count + 1

save_path = Path.cwd() / 'Anki txt files'

completeName = os.path.join(save_path, title+".txt")

os.remove(html_path)

with open(completeName, 'w', encoding='utf8') as f:
     f.write(txt)

print("Success! Please open the Anki file using folder Anki txt files.")
