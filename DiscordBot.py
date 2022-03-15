import os
from selenium import webdriver
import time
import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import youtube_dl

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'True'}

def setting_chrome_options():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080");
    chrome_options.add_argument("--start-maximized");
  #  chrome_options.add_argument("--headless");
    #chrome_options.add_argument('--no-sandbox')
    return chrome_options;

driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=setting_chrome_options())
#path_to_extension = '/Users/salpecoraro/Desktop/5.1.7_0'
client = commands.Bot(command_prefix='$')

@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

@client.command()
async def search(ctx,x):
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=setting_chrome_options())
    time.sleep(1)
    driver.get("https://www.youtube.com/results?search_query=" + x)
    time.sleep(2)
    # currentTab = driver.current_window_handle
    # allTabs = driver.window_handles
    # driver.switch_to.window(allTabs[1])
    # driver.close()
    # driver.switch_to.window(allTabs[0])
    videos = driver.find_elements_by_class_name('style-scope ytd-item-section-renderer')
    time.sleep(2)
    videos[0].click()
    time.sleep(2)
    url = driver.current_url
    driver.close()
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

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run('OTUyMzEyNjUxNjA4ODkxNDMy.Yi0MRQ.AcbGab-FrCkR-PSx0_OF6IZXzd4')