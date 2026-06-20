import json, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date, datetime

TRACKER = r'C:\Users\gusta\zurich-events-scout\zurich-events-tracker.json'
HTML_OUT = r'C:\Users\gusta\zurich-events-scout\email_body.html'
TODAY = date.today().isoformat()

with open(TRACKER, encoding='utf-8') as f:
    events = json.load(f)

def is_active(e):
    if e.get('end_date'):
        return e['end_date'] >= TODAY
    return e['date'] >= TODAY

events = [e for e in events if is_active(e)]

def by_cat(cat):
    return sorted([e for e in events if e['category'] == cat], key=lambda x: x['date'])

def new(e):
    return e.get('first_seen') == TODAY

def fmt_date(d):
    try:
        return datetime.strptime(d, '%Y-%m-%d').strftime('%d %b %Y').lstrip('0')
    except:
        return d

def badge(text, color):
    return (f'<span style="background:{color};color:#fff;font-size:11px;font-weight:bold;'
            f'padding:2px 7px;border-radius:3px;margin-left:7px;vertical-align:middle">{text}</span>')

def event_card(e):
    is_new = new(e)
    is_ch = e.get('country') == 'Switzerland'
    title_badges = ''
    if is_new:
        title_badges += badge('NEW', '#22c55e')
    if is_ch and e['category'] in ('nancy_ajram', 'gogol_bordello'):
        title_badges += badge('SWITZERLAND', '#e63946')

    is_exhibition = bool(e.get('end_date'))

    if is_exhibition:
        meta = f"{e['venue']}, {e['city']} &nbsp;·&nbsp; <em>{fmt_date(e['date'])} – {fmt_date(e['end_date'])}</em>"
        border = '#0891b2'
        bg = '#f0f9ff'
    else:
        country_str = f", {e['country']}" if e['category'] in ('nancy_ajram', 'gogol_bordello') else ''
        meta = f"{e['venue']}, {e['city']}{country_str} &nbsp;·&nbsp; <em>{fmt_date(e['date'])}</em>"
        border = '#555'
        bg = '#fafafa'

    ticket_link = ''
    if e.get('ticket_url'):
        label = 'Exhibition info' if is_exhibition else 'Tickets / info'
        ticket_link = f'<a href="{e["ticket_url"]}" style="color:#2563eb;text-decoration:none;font-weight:bold">{label} →</a>'

    review_link = ''
    if e.get('review_url'):
        review_link = f'<a href="{e["review_url"]}" style="color:#7c3aed;text-decoration:none">★ Reviews &amp; press</a>'

    links_row = ' &nbsp;&nbsp; '.join(x for x in [ticket_link, review_link] if x)
    links_html = f'<div style="margin-top:8px;font-size:13px">{links_row}</div>' if links_row else ''

    return f'''
<div style="border-left:4px solid {border};background:{bg};padding:14px 16px;margin-bottom:14px;border-radius:0 4px 4px 0">
  <div style="font-weight:bold;font-size:15px;line-height:1.3">{e["artist"]}{title_badges}</div>
  <div style="color:#555;font-size:13px;margin:5px 0 8px">{meta}</div>
  <div style="font-size:14px;line-height:1.6;color:#222">{e["description"]}</div>
  {links_html}
</div>'''

def section(title, cat, cities_note):
    items = by_cat(cat)
    new_items = [e for e in items if new(e)]
    old_items  = [e for e in items if not new(e)]

    new_html = (''.join(event_card(e) for e in new_items)
                if new_items else
                '<p style="color:#999;font-style:italic;font-size:14px">No new additions this week.</p>')

    old_section = ''
    if old_items:
        old_section = (f'<h3 style="font-size:13px;color:#666;margin:18px 0 10px;'
                       f'text-transform:uppercase;letter-spacing:1px">Upcoming</h3>'
                       + ''.join(event_card(e) for e in old_items))

    return f'''
<div style="margin-bottom:36px">
  <h2 style="font-size:19px;border-bottom:2px solid #e5e7eb;padding-bottom:8px;margin-bottom:14px;color:#111">
    {title}
    <span style="font-size:13px;font-weight:normal;color:#999;margin-left:6px">{cities_note}</span>
  </h2>
  <h3 style="font-size:13px;color:#16a34a;margin:0 0 10px;text-transform:uppercase;letter-spacing:1px">New This Week</h3>
  {new_html}
  {old_section}
</div>'''

def empty_section(title, cities_note, msg='Nothing found this week.'):
    return f'''
<div style="margin-bottom:36px">
  <h2 style="font-size:19px;border-bottom:2px solid #e5e7eb;padding-bottom:8px;margin-bottom:14px;color:#111">
    {title}
    <span style="font-size:13px;font-weight:normal;color:#999;margin-left:6px">{cities_note}</span>
  </h2>
  <p style="color:#999;font-style:italic;font-size:14px">{msg}</p>
</div>'''

def nancy_section():
    items = by_cat('nancy_ajram')
    if items:
        return section('Nancy Ajram', 'nancy_ajram', 'Europe')
    return empty_section('Nancy Ajram', 'Europe', 'No European dates found this week.')

def gogol_section():
    items = by_cat('gogol_bordello')
    if items:
        return section('Gogol Bordello', 'gogol_bordello', 'Europe')
    return empty_section('Gogol Bordello', 'Europe', 'No European dates found this week.')

now_str   = datetime.now().strftime('%d %b %Y, %H:%M')
today_str = date.today().strftime('%d %b %Y').lstrip('0')

html = f'''<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Zurich Events Weekly</title></head>
<body style="margin:0;padding:0;background:#f3f4f6;font-family:Arial,Helvetica,sans-serif">
<div style="max-width:700px;margin:24px auto;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.08)">

  <div style="background:#111;color:#fff;padding:22px 28px">
    <div style="font-size:23px;font-weight:bold;letter-spacing:-0.5px">Zurich Events Weekly</div>
    <div style="font-size:14px;color:#aaa;margin-top:5px">{today_str}</div>
  </div>

  <div style="padding:28px 28px 12px">
    {section('Comedy', 'comedy', 'Zürich · Luzern · Zug')}
    {section('Classical Music &amp; Ballet', 'classical', 'Zürich · Luzern · Zug')}
    {section('Art Exhibitions', 'art_exhibitions', 'Zürich · Basel · Luzern · Bern · Winterthur · Aarau · Schaffhausen')}
    {section('International Megastars', 'megastars', 'Zürich · Luzern · Zug')}
    {gogol_section()}
    {nancy_section()}
  </div>

  <div style="background:#f9fafb;border-top:1px solid #e5e7eb;padding:14px 28px;font-size:12px;color:#9ca3af">
    Searched {now_str} &nbsp;·&nbsp;
    Zürich, Luzern, Zug, Basel, Bern, Winterthur, Aarau, Schaffhausen &nbsp;·&nbsp;
    Europe-wide for Nancy Ajram and Gogol Bordello
  </div>
</div>
</body>
</html>'''

with open(HTML_OUT, 'w', encoding='utf-8') as f:
    f.write(html)
print('HTML written.')

msg = MIMEMultipart('alternative')
msg['Subject'] = f'Zurich Events Weekly - {today_str}'
msg['From'] = 'gustavowen@gmail.com'
msg['To'] = 'gustavowen@gmail.com'
msg.attach(MIMEText(html, 'html', 'utf-8'))

with smtplib.SMTP('smtp.gmail.com', 587) as s:
    s.starttls()
    s.login('gustavowen@gmail.com', 'kiuuqlyslgclvekv')
    s.send_message(msg)
print('Email sent successfully')
