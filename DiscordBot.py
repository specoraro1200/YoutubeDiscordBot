import os
#from selenium import webdriver
import time
import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import youtube_dl
import re
import urllib.request
from bs4 import BeautifulSoup

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'True'}

#def setting_chrome_options():
#    chrome_options = webdriver.ChromeOptions()
#    chrome_options.add_argument("--window-size=1920,1080");
#    chrome_options.add_argument("--start-maximized");
#    chrome_options.add_argument("--headless");
#    chrome_options.add_argument('--no-sandbox')
#    return chrome_options;

#driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=setting_chrome_options())
#path_to_extension = '/Users/salpecoraro/Desktop/5.1.7_0'
client = commands.Bot(command_prefix='/',intents=discord.Intents.all())

@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

@client.command()
async def search(ctx,*args):
    print(args,*args)
    print(" ".join(args[:]))
    url = " ".join(args[:])
    query = urllib.parse.quote(url)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    answer = re.search('/watch?(.*)webPageType',soup.prettify())
    ihatere = re.search("match='(.*)\",\"",str(answer))
    print(ihatere.group(1))
    await play(ctx,"https://www.youtube.com/"+ihatere.group(1))

#@client.command()
#async def search(ctx,x):
#    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=setting_chrome_options())
#    time.sleep(1)
#    driver.get("https://www.youtube.com/results?search_query=" + x)
#    time.sleep(2)
    # currentTab = driver.current_window_handle
    # allTabs = driver.window_handles
    # driver.switch_to.window(allTabs[1])
    # driver.close()
    # driver.switch_to.window(allTabs[0])
#    videos = driver.find_elements_by_class_name('style-scope ytd-item-section-renderer')
#    time.sleep(2)
#    videos[0].click()
#    time.sleep(2)
#    url = driver.current_url
#    driver.close()
#    channel = ctx.message.author.voice.channel
#    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#    if voice and voice.is_connected():
#        await voice.move_to(channel)
#    else:
#        voice = await channel.connect()
#    ydl = youtube_dl.YoutubeDL(YDL_OPTIONS)
#    with ydl:
#        info = ydl.extract_info(url, download=False)
#        I_URL = info['formats'][0]['url']
#        print(I_URL)
#        source = await discord.FFmpegOpusAudio.from_probe(I_URL, **FFMPEG_OPTIONS)
#        voice.play(source)
#        voice.is_playing()

@client.command()
async def play(ctx,url):
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    ydl = youtube_dl.YoutubeDL(YDL_OPTIONS)
    with ydl:
        info = ydl.extract_info(url, download=False)
        I_URL = info['formats'][0]['url']
        print(I_URL)
        source = await discord.FFmpegOpusAudio.from_probe(I_URL, **FFMPEG_OPTIONS)
        voice.play(source)
        voice.is_playing()
        return True
    return False

@client.command()
async def queue(ctx):
    if((is_connected(ctx)==None)):
        await ctx.send("Use play command idiot, nothing to queue")
    await play()
    await ctx.send("HJ")
    
@client.command()
async def leave(ctx):
    if((is_connected(ctx)==None)):
        await ctx.send("Already left voice channel idiot")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")
#@client.command()
#async def stop(ctx,url):
@client.command()
async def pause(ctx):
    if((is_connected(ctx)==None)):
        await ctx.send("Not in voice channel idiot")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")

@client.command()
async def resume(ctx):
    if((is_connected(ctx)==None)):
        await ctx.send("Not in voice channel idiot")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")

def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

@client.command()
async def stop(ctx):
    if((is_connected(ctx)==None)):
        await ctx.send("Not in voice channel idiot")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run('MTAwNzg5MDYxMzI5Njk2MzU5NA.GXDupg.ieX3chIHdJU5FputmZL6N8yP9PQMMJhwGcmV9I')
