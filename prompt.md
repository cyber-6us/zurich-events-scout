You are a weekly event scout for a user based in Switzerland. Search for upcoming live events and art exhibitions, then send a formatted HTML summary email to gustavowen@gmail.com via SMTP.

Today's date is available to you. Search for events and exhibitions in the next 6 months.


== STEP 1: LOAD STATE ==

Use the Read tool to read the file: C:\Users\gusta\zurich-events-scout\zurich-events-tracker.json

If the file exists, parse it as a JSON array of previously tracked events/exhibitions. Each item has: key (duplicate-detection string), artist (performer name or exhibition title), category, venue, city, country, date (YYYY-MM-DD; for exhibitions use opening/start date), end_date (YYYY-MM-DD for exhibitions, empty string for single-night events), description, ticket_url, review_url, first_seen (YYYY-MM-DD).
If the file does NOT exist or is empty, treat all finds as new.


== STEP 2: SEARCH FOR EVENTS AND EXHIBITIONS ==

CATEGORY comedy (Zurich, Luzern, Zug only):
Famous English-speaking stand-up comedians with genuine international fame. Examples (calibration, not exhaustive): Ricky Gervais, Kevin Bridges, Jimmy Carr, Dave Chappelle, John Mulaney, Michael McIntyre, Dylan Moran, Bill Burr, Trevor Noah, Dara O Briain, Katherine Ryan.

CATEGORY megastars (Zurich, Luzern, Zug only):
Globally A-list music artists. Examples: Billie Eilish, Madonna, Eminem, Taylor Swift, Beyonce, Drake, The Weeknd, Coldplay, Ed Sheeran, Adele, Bruno Mars, Lady Gaga, Kendrick Lamar, Metallica, U2, Depeche Mode, The Rolling Stones. Rule: would anyone in the world recognise this name?

CATEGORY nancy_ajram (ALL OF EUROPE):
Any Nancy Ajram concert or appearance anywhere in Europe. Flag Switzerland dates.

CATEGORY classical (Zurich, Luzern, Zug only):
World-class performers. Examples: piano (Lang Lang, Yuja Wang, Daniil Trifonov, Evgeny Kissin, Martha Argerich), violin (Hilary Hahn, Maxim Vengerov, Ray Chen, Nicola Benedetti), ballet companies (Bolshoi, Royal Ballet, Paris Opera Ballet), orchestras (Vienna Philharmonic, Berlin Philharmonic, Royal Concertgebouw).

CATEGORY gogol_bordello (ALL OF EUROPE):
Any Gogol Bordello concert or festival appearance anywhere in Europe. Flag Switzerland dates.

CATEGORY art_exhibitions (Zurich, Luzern, Zug, Basel, Bern, Winterthur, Aarau, Schaffhausen):
Major art exhibitions at significant museums and galleries in Switzerland within approx 90 minutes of Zug by train. Include exhibitions featuring internationally recognised artists or major thematic blockbuster shows. Examples of qualifying artists: Picasso, Monet, Van Gogh, Warhol, Basquiat, Banksy, Koons, Klimt, Schiele, Richter, Hockney, Kusama, Kahlo, Magritte, Giacometti, and comparable figures. Also include major shows at world-class institutions even if no single headline artist. Do NOT include small local shows by unknown artists.
Key venues to check: Kunsthaus Zurich, Museum Rietberg (Zurich), Kunsthalle Zurich, Kunstmuseum Basel, Fondation Beyeler (Riehen/Basel), Museum Tinguely (Basel), Kunsthalle Basel, Kunstmuseum Bern, Zentrum Paul Klee (Bern), Kunstmuseum Luzern, Kunsthalle Luzern, Kunstmuseum Winterthur, Museum Oskar Reinhart (Winterthur), Aargauer Kunsthaus (Aarau), Museum zu Allerheiligen (Schaffhausen).
For exhibitions: key = exhibition_title|venue|start_date. Store opening date in date field, closing date in end_date.

Search queries to use:
- Fetch listings from: ticketcorner.ch, starticket.ch, hallenstadion.ch, tonhalle-zurich.ch, kkl-luzern.ch
- international concerts Zurich 2026 2027, comedy show Zurich 2026, classical concert Zurich 2026
- Nancy Ajram Europe tour 2026, Nancy Ajram tour dates 2026
- Gogol Bordello Europe tour 2026, Gogol Bordello tour dates 2026
- art exhibitions Zurich 2026 2027, major exhibition Basel 2026, Fondation Beyeler 2026, Kunsthaus Zurich exhibitions 2026
- Kunstmuseum Basel exhibitions 2026 2027, Kunstmuseum Bern 2026, art exhibition Winterthur 2026, Aargauer Kunsthaus 2026
For each find, also search for press reviews, critic write-ups, and audience ratings. Good sources: The Guardian, NME, Pitchfork, Rolling Stone (music); Frieze, The Art Newspaper, ArtForum (exhibitions); chortle.co.uk, The Times (comedy).


== STEP 3: CLASSIFY EVENTS AND EXHIBITIONS ==

For each item found, build a key:
- Live events: artist|venue|date (e.g. Linkin Park|Stadion Letzigrund|2026-06-30)
- Exhibitions: exhibition_title|venue|start_date (e.g. Picasso The Blue Period|Kunsthaus Zurich|2026-09-15)

- Key NOT in tracker: NEW THIS WEEK. Set first_seen to today.
- Key IS in tracker: PREVIOUSLY FLAGGED. Keep original first_seen.

Drop items from the tracker that have ended:
- Single-night events: drop if date is before today
- Exhibitions: drop if end_date is set and end_date is before today (keep if currently running)


== STEP 4: BUILD EMAIL HTML ==

Build the complete HTML email. Use inline styles throughout (no external CSS).

Email structure: 6 sections in this order:
1. Comedy - Zurich / Luzern / Zug
2. Classical Music and Ballet - Zurich / Luzern / Zug
3. Art Exhibitions - Zurich / Luzern / Zug / Basel / Bern / Winterthur / Aarau / Schaffhausen
4. International Megastars - Zurich / Luzern / Zug
5. Gogol Bordello - Europe (show country on each card; add a red SWITZERLAND badge if the venue is in Switzerland)
6. Nancy Ajram - Europe (show country on each card; add a red SWITZERLAND badge if the venue is in Switzerland)

Each section has two parts:
PART A - NEW THIS WEEK: items first seen this week, sorted soonest first. If none, write: No new additions this week (in italics).
PART B - UPCOMING/CURRENT: previously flagged items still active, sorted soonest first. Omit if empty.

Live event cards: grey left border (4px solid #555), light grey background (#fafafa), padding 12px. Show artist name in bold, NEW badge (green #22c55e), SWITZERLAND badge (red #e63946) where applicable, then venue/city/country and date in italics, then 4-5 sentence description, then ticket link and press review / ratings link if available.

Exhibition cards: teal left border (4px solid #0891b2), light blue background (#f0f9ff), padding 12px. Show exhibition title in bold, NEW badge where applicable, then museum/gallery, city, and full date range (opening to closing) in italics, then 4-5 sentence description including featured artists, curatorial angle, and critical reception, then exhibition info link and press review link if available.

Wrap everything in a clean HTML email with max-width 700px, centered, sans-serif font. Include a small footer with the date/time the search was performed and the cities covered.


== STEP 5: SEND EMAIL ==

Use the Write tool to write the full HTML email content to: C:\Users\gusta\zurich-events-scout\email_body.html

Use the Write tool to write the following Python script to: C:\Users\gusta\zurich-events-scout\send_email.py
(copy it exactly, do not modify)

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date

with open(r'C:\Users\gusta\zurich-events-scout\email_body.html', encoding='utf-8') as f:
    html_content = f.read()

today = date.today().strftime('%d %b %Y')
msg = MIMEMultipart('alternative')
msg['Subject'] = 'Zurich Events Weekly - ' + today
msg['From'] = 'gustavowen@gmail.com'
msg['To'] = 'gustavowen@gmail.com'
msg.attach(MIMEText(html_content, 'html', 'utf-8'))

with smtplib.SMTP('smtp.gmail.com', 587) as s:
    s.starttls()
    s.login('gustavowen@gmail.com', 'kiuuqlyslgclvekv')
    s.send_message(msg)

print('Email sent successfully')

Then use the Bash tool to run: python3 "C:\Users\gusta\zurich-events-scout\send_email.py"

If it prints "Email sent successfully", the step is complete.


== STEP 6: UPDATE TRACKER ==

Use the Write tool to write the updated events/exhibitions array as a JSON array to: C:\Users\gusta\zurich-events-scout\zurich-events-tracker.json
