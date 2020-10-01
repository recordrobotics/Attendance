#discord imports
from discord.ext import commands, tasks
import discord
#datetime imports
import datetime
#google imports
import gspread
from gspread.models import Cell
#oauth2 imports
from oauth2client.service_account import ServiceAccountCredentials



def get_date():
    #gets specific time units
    hour = int(datetime.datetime.now().strftime("%I"))
    other = datetime.datetime.now().strftime(":%M %p")
    date = datetime.datetime.now().strftime("%Y-%m-%d ")

    #puts time units together
    display = str(date) + str(hour) + str(other)

    #returns time units
    return display



#sets up google sheets things
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('apikey.json', scope)
client = gspread.authorize(creds)
sheet = client.open("bruh").sheet1  #IMPORTANT ALSO ON LINE 56 IS GOOGLE DRIVE NAME



#sets up bot
bot = commands.Bot(command_prefix='-')
bot.remove_command('help')



#creates "help" command
@bot.command()
async def help(ctx):
    await ctx.channel.send('Just do "-attendance <attendance event>", where attendance event is what you want to call the meeting name')



#creates "attendance" command
@bot.command()
async def attendance(ctx, *args):
    #refreshes drive info
    scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('apikey.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("bruh").sheet1

    #runs only if someone is in voice channel
    if ctx.author.voice and ctx.author.voice.channel:
        #gets voice channel of author
        channel = ctx.author.voice.channel
        members = channel.members

        #gets members in voice channel
        connected = [] #(list)
        for member in members:
            #connected.append(str(bot.get_user(member.id)))
            connected.append(str(member.display_name)) #IMPORTANT DISPLAYS AS DISPLAY NAME


        #puts members into string
        connected_string = ""
        for i in connected:
            connected_string = connected_string + i + ", "
        connected_string = connected_string[:-2]


        #displays list of connected people
        await ctx.send("**Current list of connected people:**\n{}".format(connected_string))


        #gets event name
        if len(args) == 1:
            event_name = str(args[0]) + ", "
        else:
            event_name = ""

        #creates valuedata
        value_data = str(event_name + get_date())

        #adds values to sheets
        column = len(sheet.row_values(1)) + 1
        cells = []
        cells.append(Cell(row=1, col=column, value=value_data))
        for q in range(2, len(connected) + 2):
            cells.append(Cell(row=q, col=column, value=connected[q-2]))

        sheet.update_cells(cells)

        print("adding\n\n{}\n\nto sheets".format(connected))
        

    else:
        await ctx.send("Could be wrong, but \n*You are not connected to a voice channel*")


    


bot.run("NzU1MjEwNTM2MTgxOTU2Njc4.X1_-ng.9aJk1_JB2r7QYnZnORjGeQEcnGU")