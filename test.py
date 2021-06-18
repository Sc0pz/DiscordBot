from urllib.request import urlopen
import random

print(random.randint(1, 69))
exit()

print('Enter the course name')
inputString = input()
inputString = inputString.split()
inputString = '+'.join(inputString)
url = "https://catalog.gmu.edu/search/?scontext=all&search=" + inputString
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
#title_index = html.find("<title>")
#start_index = title_index + len("<title>")
#end_index = html.find("</title>")
#title = html[start_index:end_index]
testIndex = html.find("Results not found")
onlyDeptIndex = html.find('<div class="searchresult search-courseresult"><h2><strong class="cb_code">')
if testIndex != -1 or onlyDeptIndex == -1:
    print('No Results Found')
else:
    title_index = html.find('<div class="searchresult search-courseresult"><h2><strong class="cb_code">')
    start_index = title_index + len('<div class="searchresult search-courseresult"><h2><strong class="cb_code">')
    end_index = html.find('</strong>')
    classID = html[start_index:end_index - 1]
    title_index = html.find('<em class="cb_title">')
    start_index = title_index + len('<em class="cb_title">')
    end_index = html.find('</em>')
    className = html[start_index:end_index]
    title_index = html.find('<div class="courseblockdesc">')
    start_index = title_index + len('<div class="courseblockdesc">')
    end_index = html.find('</div><div class="courseblockextra">')
    class_desc = html[start_index:end_index]
    start_index = class_desc.find('<a target')
    end_index = class_desc.find('</a>') + len('</a>')
    print(start_index)
    print(end_index)
    class_deptHTML = class_desc[start_index:end_index]
    class_dept = ''
    deptIndex = -1
    skipIndex = -1
    indexTracker = 0
    print(class_desc)
    print('\n')
    
    end_index = class_desc.find('</a>')
    startEnd_index = class_desc.find(');">') + len(');">')
    start_index = class_desc.find('<a href')
    dept_html_index = class_desc.find('<a target')
    print(class_desc)
    print("AHDIUWAHGDUIHGAUOIDHAUOIDHA")
    print(dept_html_index)
    print('\n')
    indexTracker = 0
    while (end_index != -1):
        print(dept_html_index)
        print(start_index)
        if ((dept_html_index < start_index and dept_html_index != -1) or start_index == -1):
            print("THIS SHOULD RUN YOU LITTLE SHIT")
            print(dept_html_index)
            print(end_index)
            class_deptHTML = class_desc[class_desc.find('<a target'):end_index + len('</a>')]
            print(class_deptHTML)
            for c in range(1, len(class_deptHTML)):
                if (c < 5): continue
                if (class_deptHTML[c * -1] == '>'):
                    deptIndex = c * -1
                    break
                class_dept += class_deptHTML[c * -1]
                if (class_deptHTML[c * -1] == '&'):
                    skipIndex = indexTracker
                print(class_deptHTML[c * -1])
                indexTracker += 1
                
            print(class_dept)
            if (skipIndex != -1): class_dept = class_dept[:skipIndex - 4] + class_dept[skipIndex:]
            print(class_dept)
            class_dept = class_dept[::-1]
            print(dept_html_index)
            print(class_desc[:dept_html_index])
            print("\n")
            print(class_desc)
            print("\n")
            class_desc = class_desc[:dept_html_index] + class_dept + class_desc[end_index + len('</a>'):]
            print(class_desc)
            end_index = class_desc.find('</a>')
            dept_html_index = -1
            startEnd_index = class_desc.find(');">') + len(');">')
            start_index = class_desc.find('<a href')
            print(end_index)
            print('----------------------------------------')
            print("\n")
            continue
        altClass = class_desc[startEnd_index:end_index]
        print(start_index)
        print(altClass)
        print("-----")
        print(end_index)
        class_desc = class_desc[:start_index] + altClass + class_desc[end_index + len('</a>'):]
        end_index = class_desc.find('</a>')
        startEnd_index = class_desc.find(');">') + len(');">')
        start_index = class_desc.find('<a href')
        dept_html_index = class_desc.find('<a target')
        print(class_desc)
        print('\n')
        
    print("OUT OF LOOP:\n")
    print(class_desc)
    exit()
    for c in range(1, len(class_deptHTML)):
        if (c < 5): continue
        if (class_deptHTML[c * -1] == '>'):
            deptIndex = c * -1
            break
        
        class_dept += class_deptHTML[c * -1]
        if (class_deptHTML[c * -1] == '&'): skipIndex = indexTracker
        print(class_deptHTML[c * -1])
        indexTracker += 1
    if (skipIndex != -1): class_dept = class_dept[:skipIndex - 4] + class_dept[skipIndex:]
    class_dept = class_dept[::-1]
    print(class_dept)
    class_desc = class_desc[:start_index] + class_dept + class_desc[end_index:]
    print('\n')
    print(class_desc)
    print(start_index)
    
    
    print('\n')
    print(classID)
    print(className)
    print(class_desc)
    