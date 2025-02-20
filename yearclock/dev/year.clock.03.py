#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import math
import random
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd4in26
import time
import datetime
from PIL import Image,ImageDraw,ImageFont
import traceback

factor = 4
render_width, render_height = 800*factor, 480*factor
xpd_width, xpd_height = 800, 480
xpd_GRAY1  = 0xff #white
xpd_GRAY2  = 0xC0
xpd_GRAY3  = 0x80 #gray
xpd_GRAY4  = 0x00 #Blackest

logging.basicConfig(level=logging.DEBUG)

def draw_textsize( text, font ):
    bbox = draw.textbbox((0, 0), text, font=font)  # (0, 0) is an arbitrary position
    text_width = bbox[2] - bbox[0]  # Calculate width
    text_height = bbox[3] - bbox[1] # Calculate height
    return text_width, text_height

# draw an arrow at the given position and angle
def draw_arrow(draw, x, y, angle, length, color):
    arrow_head_length = int(render_height / 20)
    line_width = int(render_height / 80)
    
    angle_rad = math.radians(angle)
    x2 = x + length * math.cos(angle_rad)
    y2 = y + length * math.sin(angle_rad)
    draw.line((x, y, x2, y2), fill=color, width=line_width)
    draw.line((x2, y2, x2 + arrow_head_length * math.cos(angle_rad + math.radians(135)), y2 + arrow_head_length * math.sin(angle_rad + math.radians(135))), fill=color, width=line_width)
    draw.line((x2, y2, x2 + arrow_head_length * math.cos(angle_rad - math.radians(135)), y2 + arrow_head_length * math.sin(angle_rad - math.radians(135))), fill=color, width=line_width)

# draw the x and y axis on the image
def draw_axis(draw):
    draw_arrow(draw, 25,25, 0, render_width / 4, epd.GRAY4)
    draw_arrow(draw, 25,25, 90, render_height / 4, epd.GRAY2)
    
# create a function that draws an analog clock face given the current time
def draw_day_clock(draw, current_time, center_x, center_y, size):
    face_radius = int(size)
    center_radius = int(face_radius * 0.075)
    hourhand_len = int(face_radius * 0.55)
    minutehand_len = int(face_radius * 0.8)
    secondhand_len = int(face_radius * 0.90)
    line_width =int(face_radius * 0.02)
    
    # draw the clock face
    draw.ellipse((center_x-face_radius, center_y-face_radius, center_x+face_radius, center_y+face_radius), fill=epd.GRAY1)
    draw.ellipse((center_x-face_radius, center_y-face_radius, center_x+face_radius, center_y+face_radius), outline=epd.GRAY4, width=line_width)
    # draw the clock center
    draw.ellipse((center_x-center_radius, center_y-center_radius, center_x+center_radius, center_y+center_radius), fill=epd.GRAY4)
    
    # draw the hour hand
    hour_angle = (current_time.tm_hour % 12 + current_time.tm_min / 60.0) * 30 - 90
    hour_x = center_x + hourhand_len * math.cos(math.radians(hour_angle))
    hour_y = center_y + hourhand_len * math.sin(math.radians(hour_angle))
    draw.line((center_x, center_y, hour_x, hour_y), fill=epd.GRAY4, width=line_width*2)
    # draw the minute hand
    minute_angle = (current_time.tm_min + current_time.tm_sec / 60.0) * 6 - 90
    minute_x = center_x + minutehand_len * math.cos(math.radians(minute_angle))
    minute_y = center_y + minutehand_len * math.sin(math.radians(minute_angle))
    draw.line((center_x, center_y, minute_x, minute_y), fill=epd.GRAY4, width=line_width*2)
    # draw the second hand
    #second_angle = current_time.tm_sec * 6 - 90
    #second_x = center_x + secondhand_len * math.cos(math.radians(second_angle))
    #second_y = center_y + secondhand_len * math.sin(math.radians(second_angle))
    #draw.line((center_x, center_y, second_x, second_y), fill=epd.GRAY4, width=line_width)

        
    # draw the clock face numbers
    bDrawNumbers = True
    if bDrawNumbers:
        nDays = 0
        for i in range(1,13):
            angle = (i*360/12) - 90
            tick_len = face_radius * 0.15
            tick_x1 = center_x + (face_radius + tick_len * 0.5) * math.cos(math.radians(angle))
            tick_y1 = center_y + (face_radius + tick_len * 0.5) * math.sin(math.radians(angle))
            tick_x2 = center_x + face_radius * math.cos(math.radians(angle))
            tick_y2 = center_y + face_radius * math.sin(math.radians(angle))
            draw.line((tick_x1, tick_y1, tick_x2, tick_y2), fill=epd.GRAY4, width=int(6*1.5))
            # draw the hour
            hour_x = center_x + (face_radius + tick_len * 1.0) * math.cos(math.radians(angle))
            hour_y = center_y + (face_radius + tick_len * 1.0) * math.sin(math.radians(angle))
            # get the text bounds for the hour number
            text_width, text_height = draw_textsize(str(i), font=font35)
            hour_x -= text_width / 2
            hour_y -= text_height / 2
            draw.text((hour_x, hour_y), str(i), font=font35, fill=epd.GRAY4)
    
    # draw the clock face ticks
    for i in range(60):
        angle = i * 6 - 90
        if i % 5 == 0:
            tick_len = face_radius * 0.1
        else:
            tick_len = face_radius * 0.05
        tick_x1 = center_x + (face_radius - tick_len) * math.cos(math.radians(angle))
        tick_y1 = center_y + (face_radius - tick_len) * math.sin(math.radians(angle))
        tick_x2 = center_x + face_radius * math.cos(math.radians(angle))
        tick_y2 = center_y + face_radius * math.sin(math.radians(angle))
        draw.line((tick_x1, tick_y1, tick_x2, tick_y2), fill=epd.GRAY4, width=6)
        
        
# draw year clock
def draw_year_clock(draw, current_time):
    center_x = int(render_width / 2)
    center_y = int(render_height / 2)
    face_radius = int(render_height / 2 * 0.9)
    hourhand_len = int(face_radius * 0.5)
    minutehand_len = int(face_radius * 0.7)
    secondhand_len = int(face_radius * 0.90)
    line_width =int(face_radius * 0.03)
    
    # draw the clock face
    draw.ellipse((center_x-face_radius, center_y-face_radius, center_x+face_radius, center_y+face_radius), outline=epd.GRAY4, width=line_width)
    
    # draw the hour hand as the day of the year
    day_of_year = current_time.tm_yday
    hour_angle = (day_of_year % 365 / 365.0) * 360 - 90
    hour_x = center_x + hourhand_len * math.cos(math.radians(hour_angle))
    hour_y = center_y + hourhand_len * math.sin(math.radians(hour_angle))
    draw.line((center_x, center_y, hour_x, hour_y), fill=epd.GRAY4, width=line_width*2)
    
    # draw the minute hand as the month of the year
    month_of_year = current_time.tm_mon - 1
    minute_angle = (month_of_year % 12 / 12.0) * 360 - 90
    minute_x = center_x + minutehand_len * math.cos(math.radians(minute_angle))
    minute_y = center_y + minutehand_len * math.sin(math.radians(minute_angle))
    draw.line((center_x, center_y, minute_x, minute_y), fill=epd.GRAY4, width=line_width*2)
    
    # draw the second hand as the day of the month
    day_of_month = current_time.tm_mday
    second_angle = (day_of_month % 31 / 31.0) * 360 - 90
    second_x = center_x + secondhand_len * math.cos(math.radians(second_angle))
    second_y = center_y + secondhand_len * math.sin(math.radians(second_angle))
    draw.line((center_x, center_y, second_x, second_y), fill=epd.GRAY4, width=line_width)
    
    # list the months
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    # list the days of the month
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
    # draw the clock face ticks as days of the year
    for i in range(365):
        angle = i - 90
        tick_len = face_radius * 0.05
        tick_x1 = center_x + (face_radius - tick_len) * math.cos(math.radians(angle))
        tick_y1 = center_y + (face_radius - tick_len) * math.sin(math.radians(angle))
        tick_x2 = center_x + face_radius * math.cos(math.radians(angle))
        tick_y2 = center_y + face_radius * math.sin(math.radians(angle))
        draw.line((tick_x1, tick_y1, tick_x2, tick_y2), fill=epd.GRAY4, width=3)
        
    # draw the clock face numbers as months
    nDays = 0
    for i in range(12):
        angle = (nDays/365 * 360) - 90
        tick_len = face_radius * 0.15
        tick_x1 = center_x + (face_radius - tick_len) * math.cos(math.radians(angle))
        tick_y1 = center_y + (face_radius - tick_len) * math.sin(math.radians(angle))
        tick_x2 = center_x + face_radius * math.cos(math.radians(angle))
        tick_y2 = center_y + face_radius * math.sin(math.radians(angle))
        draw.line((tick_x1, tick_y1, tick_x2, tick_y2), fill=epd.GRAY4, width=3)
        # draw the month name
        month_x = center_x + (face_radius - tick_len * 1.5) * math.cos(math.radians(angle))
        month_y = center_y + (face_radius - tick_len * 1.5) * math.sin(math.radians(angle))
        #draw.ellipse((month_x-10, month_y-10, month_x+10, month_y+10), outline=epd.GRAY4, width=3)
        # get the text bounds for the month name
        text_width, text_height = draw_textsize(months[i], font=font35)
        month_x -= text_width / 2
        month_y -= text_height / 2
        draw.text((month_x, month_y), months[i], font=font35, fill=epd.GRAY4)
        nDays += days[i]

# draw year clock
def draw_year_clock_with_weeks(draw, current_time, center_x, center_y, size):

    face_radius = int(size)
    center_radius = int(face_radius * 0.075)
    hand_len = int(face_radius * 0.95)
    line_width =int(face_radius * 0.02)
    
    draw.ellipse((center_x-face_radius, center_y-face_radius, center_x+face_radius, center_y+face_radius), fill=epd.GRAY1)

    # draw the hand as the day of the year
    day_of_year = current_time.tm_yday
    hour_angle = (day_of_year % 365 / 365.0) * 360 - 90
    hour_x = center_x + hand_len * math.cos(math.radians(hour_angle))
    hour_y = center_y + hand_len * math.sin(math.radians(hour_angle))
    draw.line((center_x, center_y, hour_x, hour_y), fill=epd.GRAY4, width=int(line_width*0.5))
    hour_x = center_x + hand_len * 0.75 * math.cos(math.radians(hour_angle))
    hour_y = center_y + hand_len * 0.75 * math.sin(math.radians(hour_angle))
    draw.line((center_x, center_y, hour_x, hour_y), fill=epd.GRAY4, width=line_width*3)
    
    
    # draw a arc from the start of the year to the current day
    draw.arc((center_x-face_radius, center_y-face_radius, center_x+face_radius, center_y+face_radius), -90, hour_angle, fill=epd.GRAY2, width=120)

    # draw the clock face
    draw.ellipse((center_x-face_radius, center_y-face_radius, center_x+face_radius, center_y+face_radius), outline=epd.GRAY4, width=line_width)
    # draw the clock center
    draw.ellipse((center_x-center_radius, center_y-center_radius, center_x+center_radius, center_y+center_radius), fill=epd.GRAY4)
  
    # list the months
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    # list the days of the month
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
    # draw the clock face ticks as where the sundays are in the year
    # find the first sunday of the year
    jan1st_time = time.struct_time((current_time.tm_year, 1, 1, 0, 0, 0, 0, 1, -1))
    # Get the timestamp (seconds since the epoch) for January 1st
    jan1st_timestamp = time.mktime(jan1st_time)
    # Calculate the day of the week (0 = Monday, 6 = Sunday)
    day_of_week = time.localtime(jan1st_timestamp).tm_wday
    # Calculate days to add to get to the first Sunday
    days_to_add = (6 - day_of_week) % 7
        
    for i in range(52):
        angle = ((i*7 + days_to_add)/365*360) - 90
        tick_len = face_radius * 0.05
        tick_x1 = center_x + (face_radius - tick_len) * math.cos(math.radians(angle))
        tick_y1 = center_y + (face_radius - tick_len) * math.sin(math.radians(angle))
        tick_x2 = center_x + face_radius * math.cos(math.radians(angle))
        tick_y2 = center_y + face_radius * math.sin(math.radians(angle))
        draw.line((tick_x1, tick_y1, tick_x2, tick_y2), fill=epd.GRAY4, width=3)
        
    # draw the clock face numbers as months
    bDrawMonths = True
    if bDrawMonths:
        nDays = 0
        for i in range(12):
            angle = (nDays/365 * 360) - 90
            tick_len = face_radius * 0.15
            tick_x1 = center_x + (face_radius + tick_len * 0.5) * math.cos(math.radians(angle))
            tick_y1 = center_y + (face_radius + tick_len * 0.5) * math.sin(math.radians(angle))
            tick_x2 = center_x + face_radius * math.cos(math.radians(angle))
            tick_y2 = center_y + face_radius * math.sin(math.radians(angle))
            draw.line((tick_x1, tick_y1, tick_x2, tick_y2), fill=epd.GRAY4, width=6)
            # draw the month name
            month_x = center_x + (face_radius + tick_len * 1.0) * math.cos(math.radians(angle))
            month_y = center_y + (face_radius + tick_len * 1.0) * math.sin(math.radians(angle))
            #draw.ellipse((month_x-10, month_y-10, month_x+10, month_y+10), outline=epd.GRAY4, width=3)
            # get the text bounds for the month name
            text_width, text_height = draw_textsize(months[i], font=font35)
            month_x -= text_width / 2
            month_y -= text_height / 2
            draw.text((month_x, month_y), months[i], font=font35, fill=epd.GRAY4)
            nDays += days[i]
        
    # draw the sprints of the year
    nDays = 0
    sprints = [3,3,3,4, 3,3,3,4, 3,3,3,4, 3,3,3,4]
    for i, sprint in enumerate(sprints):
        angle = ((nDays+days_to_add)/365 * 360) - 90
        tick_len = face_radius * 0.1
        tick_x1 = center_x + (face_radius - tick_len) * math.cos(math.radians(angle))
        tick_y1 = center_y + (face_radius - tick_len) * math.sin(math.radians(angle))
        tick_x2 = center_x + face_radius * math.cos(math.radians(angle))
        tick_y2 = center_y + face_radius * math.sin(math.radians(angle))
        draw.line((tick_x1, tick_y1, tick_x2, tick_y2), fill=epd.GRAY4, width=12)
        # draw the sprint name
        # format is year.quarter.sprint
        sprint_name = str(current_time.tm_year - 2000) + "." + str(int((nDays + sprint/2)/365 * 4) + 1) + "." + str(i % 4 + 1)
        angle += sprint*7/365 * 360 / 2
        sprint_x = center_x + (face_radius - tick_len * 2.5) * math.cos(math.radians(angle))
        sprint_y = center_y + (face_radius - tick_len * 2.5) * math.sin(math.radians(angle))
        #draw.ellipse((month_x-10, month_y-10, month_x+10, month_y+10), outline=epd.GRAY4, width=3)
        # get the text bounds for the month name
        text_width, text_height = draw_textsize(str(sprint_name), font=font24)
        sprint_x -= text_width / 2
        sprint_y -= text_height / 2
        draw.text((sprint_x, sprint_y), str(sprint_name), font=font24, fill=epd.GRAY4)
        nDays += sprint*7


def draw_swirl(draw, center_x, center_y, radius, turns, width, color):
    fromx = 0
    fromy = 0

    angle_step = 0.01  # Adjust for smoothness
    for i in range(int(turns / angle_step)):
        angle = i * angle_step * 2 * math.pi
        r = radius * angle / (turns * 2 * math.pi) # radius increases with angle
        x = center_x + r * math.cos(angle)
        y = center_y - r * math.sin(angle)

        if i == 0:
            fromx = x
            fromy = y
        else:
            draw.line([fromx, fromy, x, y], fill=color, width=width)
            fromx = x
            fromy = y


def draw_flower(draw, center_x, center_y, radius, petals, color):
    angle_step = 2 * math.pi / petals
    for i in range(petals):
        angle = i * angle_step
        x1 = center_x + radius * math.cos(angle)
        y1 = center_y + radius * math.sin(angle)
        x2 = center_x + radius * 0.6 * math.cos(angle + angle_step / 2) # Inner points
        y2 = center_y + radius * 0.6 * math.sin(angle + angle_step / 2)
        #ctx.move_to(center_x, center_y)  # Center of the flower
        #ctx.curve_to(x1, y1, x2, y2, center_x, center_y) # Cubic bezier curve
        #draw.line([center_x, center_y, x1, y1], fill=color, width=2)
        draw.line([x1, y1, x2, y2], fill=color, width=2)
          
def draw_background(draw):
    for _ in range(1000): 
        x = random.randint(0, render_width)
        y = random.randint(0, render_height)
        size = random.randint(10, 45)
        petals = random.randint(7, 12)
        draw_flower(draw, x, y, size, petals, epd.GRAY2)
        
    for _ in range(50): 
        x = random.randint(0, render_width)
        y = random.randint(0, render_height)
        size = random.randint(20, 450)
        turns = random.randint(2, 5)
        draw_swirl(draw, x, y, size, turns, 1, epd.GRAY2)
        
        
def render(draw):
    logging.info("render")
    
    draw_background(draw)
    
    # Draw the clock face
    center_x = int(render_width / 4 * 3)
    center_y = int(render_height / 2)
    size = render_height / 2 * 0.8 * 0.75
    draw_year_clock_with_weeks(draw, time.localtime(), center_x, center_y, size)
    
    center_x = int(render_width / 4 * 1)
    draw_day_clock(draw, time.localtime(), center_x, center_y, size)
    
    # Display the image
    resized_image = image.resize((epd.width, epd.height), resample=Image.LANCZOS)
    #resized_image.show()    
    epd.display_4Gray(epd.getbuffer_4Gray(resized_image))


           
def run_every_minute(draw):
    while True:
        render(draw)  # Call the function

        # Calculate time to sleep until the next minute
        now = datetime.datetime.now()
        next_minute = now + datetime.timedelta(minutes=1)
        sleep_time = (next_minute - now).total_seconds()

        logging.info("sleeping for %d seconds", sleep_time)
        time.sleep(sleep_time)  # Sleep until the next minute
        logging.info("awake")


if __name__ == "__main__":
    try:
        logging.info("YearClock Start")
        epd = epd4in26.EPD()

        logging.info("init and Clear")
        epd.init_4GRAY()
        #epd.Clear()

        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24 * 2)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18 * 2)
        font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35 * 2)

        image = Image.new('L', (render_width, render_height), epd.GRAY1)  # clear the frame
        draw = ImageDraw.Draw(image)
        
        run_every_minute(draw)
        
            
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd4in26.epdconfig.module_exit(cleanup=True)
        exit()
