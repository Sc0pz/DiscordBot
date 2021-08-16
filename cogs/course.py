from discord.ext import commands
from urllib.request import urlopen
import discord
import random

class Course(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def course(self, ctx, *lookup):
        #If no arguments are given in command
        if (len(lookup) == 0): 
            await ctx.send("Please enter an argument.")
            return
        
        #Parses arguments into url search resultsand grabs html of result
        inputString = '+'.join(lookup)
        url = "https://catalog.gmu.edu/search/?scontext=all&search=" + inputString
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        
        #Indices determine if any courses are found on the page
        testIndex = html.find("Results not found") #Only shows up if no results found on page
        onlyDeptIndex = html.find('<div class="searchresult search-courseresult"><h2><strong class="cb_code">') #Attempts to find HTML for courses - in case departments but not courses found
        if (testIndex != -1 or onlyDeptIndex == -1):
            Embed = discord.Embed(title='No Results Found', colour=discord.Colour.dark_green())
            await ctx.send(embed=Embed)
        else:
            #Indices used to grab HTML of key items and extract contents
            #start_index: First instance of HTML to find, indicates beginning index in html item.
            #end_index: Indicates end index - index of where the HTML to find ends.
            start_index = html.find('<div class="searchresult search-courseresult"><h2><strong class="cb_code">') + len('<div class="searchresult search-courseresult"><h2><strong class="cb_code">')
            end_index = html.find('</strong>')
            classID = html[start_index:end_index - 1] #Extracts Class ID (ex: CS 330) from HTML
            start_index = html.find('<em class="cb_title">') + len('<em class="cb_title">')
            end_index = html.find('</em>')
            className = html[start_index:end_index - 1] #Extracts full class name from HTML
            start_index = end_index + len('</em>')
            newHTML = html[start_index:]
            end_index = newHTML.find('</h2>')
            className += ' (' + newHTML[1:end_index - 1] + ').'
            
            #Extracts class description from HTML
            start_index = html.find('<div class="courseblockdesc">') + len('<div class="courseblockdesc">')
            end_index = html.find('</div><div class="courseblockextra">')
            class_desc = html[start_index:end_index]
            #Extra work needed to clean up description from any
            #extraneous html tags present such as additional hyperlinks
            start_index = class_desc.find('<a href') #Marks index of where html starts
            startEnd_index = class_desc.find(');">') + len(');">') #Marks index of the end of the beginning html tag
            end_index = class_desc.find('</a>') #Marks index of the end of the tag's contents
            dept_html_index = class_desc.find('<a target') #Specific HTML case that all courses have - 'Offered by Computer Science' hyperlink
            class_dept = ''
            deptIndex = -1 #Grabs department name of course from description
            indexTracker = 0 #Tracks number of times iterated through loop
            
            #While loop runs as long as there's additional extraneous html
            #in the description, removing additional html tags.
            while (end_index != -1):
                #Specific branch to extract department from course description - only runs if
                #all previous hyperlinks in front of the department hyperlink has been removed
                if ((dept_html_index < start_index and dept_html_index != -1) or start_index == -1):
                    class_deptHTML = class_desc[class_desc.find('<a target'):end_index + len('</a>')]
                    #For loop iterates through html and extracts department name
                    for c in range(1, len(class_deptHTML)):
                        #HTML string is reversed, can skip '</a>'
                        if (c < 5): continue
                        #If statement to prevent iterating more than necessary
                        if (class_deptHTML[c * -1] == '>'):
                            deptIndex = c * -1
                            break
                        class_dept += class_deptHTML[c * -1]
                    class_dept = class_dept[::-1]
                    class_desc = class_desc[:dept_html_index] + class_dept + class_desc[end_index + len('</a>'):]
                    
                    #Reassigns indices to find first instance of HTML - necessary 
                    #in case more html is present after department.
                    end_index = class_desc.find('</a>')
                    dept_html_index = -1
                    startEnd_index = class_desc.find(');">') + len(');">')
                    start_index = class_desc.find('<a href')
                    continue
                
                #altClass is resultant extracted contents of the hyperlink.
                #Hyperlink usually something like 'COURSE' can be used to fulfull...
                altClass = class_desc[startEnd_index:end_index]
                #Readds extracted contents while removing the html.
                class_desc = class_desc[:start_index] + altClass + class_desc[end_index + len('</a>'):]
                #Attempts to find more html, if -1 then loop is exited.
                end_index = class_desc.find('</a>')
                startEnd_index = class_desc.find(');">') + len(');">')
                start_index = class_desc.find('<a href')
                dept_html_index = class_desc.find('<a target')
            
            #Final Class Description cleaning - checks for items such as &amp; and &quot; and removes them
            skipIndex1 = class_desc.find('&amp;')
            skipIndex2 = class_desc.find('&quot;')
            while (skipIndex1 != -1 or skipIndex2 != -1):
                if (skipIndex1 != -1):
                    class_desc = class_desc[:skipIndex1 + 1] + class_desc[skipIndex1 + 5:]
                elif (skipIndex2 != -1):
                    class_desc = class_desc[:skipIndex2] + '"' + class_desc[skipIndex2 + 6:]
                skipIndex1 = class_desc.find('&amp;')
                skipIndex2 = class_desc.find('&quot;')
            
            #Adds all items to discord embed and sends.
            Embed = discord.Embed(title=classID, colour=discord.Colour.dark_green(), url=url)
            Embed.add_field(name=className, value=class_desc)
            await ctx.send(embed=Embed)

    @commands.command()
    async def honorcode(self, ctx):
        Embed = discord.Embed(title='Honor Code Statement', description='To promote a stronger sense of mutual responsibility, respect, trust, and fairness among all members of the George Mason University Community and with the desire for greater academic and personal achievement, we, the student members of the university community, have set for this Honor Code: Student Members of the George Mason University community pledge not to cheat, plagiarize, steal, or lie in matters related to academic work.', colour = discord.Colour.dark_green())
        await ctx.send(embed=Embed)

def setup(bot):
    bot.add_cog(Course(bot))