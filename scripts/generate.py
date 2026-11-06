import json,subprocess,pathlib,html,datetime,collections,math
ROOT=pathlib.Path(__file__).resolve().parents[1]
A=ROOT/'assets';A.mkdir(exist_ok=True)
query='query { user(login:"AndrianDev0") { contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { contributionCount date color } } } } repositories(first:100,privacy:PUBLIC,ownerAffiliations:OWNER) { nodes { name stargazerCount languages(first:10,orderBy:{field:SIZE,direction:DESC}) { edges { size node { name color } } } } } } }'
u=json.loads(subprocess.check_output(['gh','api','graphql','-f','query='+query],encoding='utf-8'))['data']['user']
E=html.escape
style='''<style>text{font-family:Consolas,"DejaVu Sans Mono",monospace;fill:#dbe5f7}.muted{fill:#a1afc8}.blue{fill:#5dc9f2}.pink{fill:#f47a96}.cursor{animation:blink 1.2s steps(1) infinite}@keyframes blink{50%{opacity:0}}.runner{animation:run 18s linear infinite}@keyframes run{0%{transform:translateX(0)}100%{transform:translateX(822px)}}@media(prefers-reduced-motion:reduce){.cursor,.runner{animation:none}}</style>'''
def svg(w,h,content,title):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{E(title)}</title>{style}<rect width="{w}" height="{h}" rx="14" fill="#0b1120"/>{content}</svg>'
def text(x,y,s,size=16,cl='',extra=''):return f'<text x="{x}" y="{y}" font-size="{size}" class="{cl}" {extra}>{E(str(s))}</text>'
c='<path d="M14 0H886Q900 0 900 14V40H0V14Q0 0 14 0" fill="#141e33"/>'
for x,col in [(24,'#ff5f57'),(46,'#febc2e'),(68,'#28c840')]:c+=f'<circle cx="{x}" cy="20" r="6" fill="{col}"/>'
c+=text(450,25,'andrian@github: ~',13,'muted','text-anchor="middle"')+text(30,80,'$ whoami',18,'pink')
art=['    /\\      ____  ','   /  \\    |  _ \\ ','  / /\\ \\   | | | |',' / ____ \\  | |_| |','/_/    \\_\\ |____/ ']
for i,line in enumerate(art):c+=text(34,150+i*27,line,22,'blue','xml:space="preserve"')
c+=text(54,314,'BUILD. TEST. SHIP.',15,'muted')
c+='<line x1="323" y1="113" x2="323" y2="334" stroke="#25334e"/>'
c+=text(355,129,'AndrianDev0',28,'blue')+text(355,158,'Веб-разработка · Telegram · Автоматизация',16)
for i,(label,value) in enumerate([('учёба','ЮЯТК / ИСП'),('стек','TypeScript · React · Python'),('данные','PostgreSQL · SQLite'),('проект','SIMKA — магазин SIM и eSIM'),('статус','Открыт к работе и стажировке')]):
 c+=text(355,199+i*29,label,15,'pink')+text(452,199+i*29,value,15)
c+=text(30,385,'$ превращаю задачи в работающие проекты',17,'blue')+'<rect x="452" y="371" width="9" height="20" fill="#5dc9f2" class="cursor"/>'
(A/'profile.svg').write_text(svg(900,420,c,'Андриан — веб-разработка, Telegram и автоматизация'),encoding='utf-8')
repos=u['repositories']['nodes'];langs=collections.Counter();colors={}
for r in repos:
 if r['name']=='andrian-dev-portfolio':continue
 for edge in r['languages']['edges']:
  n=edge['node']['name'];langs[n]+=edge['size'];colors[n]=edge['node']['color'] or '#5dc9f2'
total=sum(langs.values()) or 1;top=langs.most_common(5)
c=text(30,40,'GITHUB / ЯЗЫКИ КОДА',19,'blue')+text(30,67,'Публичные репозитории · объём кода',13,'muted')
for i,(n,count) in enumerate(top):
 y=105+i*42;p=count/total;c+=text(30,y,n,15)+text(410,y,f'{p:.1%}',14,'muted','text-anchor="end"')+f'<rect x="30" y="{y+10}" width="380" height="7" rx="3" fill="#1b2840"/><rect x="30" y="{y+10}" width="{max(2,380*p)}" height="7" rx="3" fill="{colors[n]}"/>'
c+=text(480,45,'АКТИВНОСТЬ',19,'blue')+text(480,91,u['contributionsCollection']['contributionCalendar']['totalContributions'],38)+text(480,117,'вкладов за последние 12 месяцев',14,'muted')
c+=text(480,170,len(repos),32)+text(535,169,'публичных репозиториев',14,'muted')
c+=text(480,220,sum(r['stargazerCount'] for r in repos),32)+text(535,219,'звёзд у проектов',14,'muted')
c+=text(480,277,'Источник: GitHub API',13,'muted')+text(480,302,'Обновлено: '+datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d UTC'),13,'muted')
c+=text(30,344,'Копия портфолио исключена из подсчёта языков. Это не оценка уровня навыков.',12,'muted')
(A/'stats.svg').write_text(svg(900,365,c,'Языки публичного кода и активность GitHub'),encoding='utf-8')
c=text(30,36,'CONTRIBUTION ACTIVITY',19,'blue');weeks=u['contributionsCollection']['contributionCalendar']['weeks']
for x,week in enumerate(weeks):
 for y,d in enumerate(week['contributionDays']):
  count=d['contributionCount'];color='#1b2840' if count==0 else '#17475b' if count<4 else '#217a98' if count<9 else '#39acd1' if count<16 else '#7bdef7'
  c+=f'<rect x="{30+x*16}" y="{60+y*16}" width="12" height="12" rx="3" fill="{color}"><title>{d["date"]}: {count}</title></rect>'
c+='<g class="runner"><path d="M30 199 L40 191 A13 13 0 1 0 40 207 Z" fill="#5dc9f2"/><circle cx="29" cy="191" r="2" fill="#0b1120"/></g>'
c+=text(30,239,'Реальные вклады GitHub · декоративная анимация',12,'muted')
(A/'activity.svg').write_text(svg(900,260,c,'Календарь вкладов AndrianDev0 за 12 месяцев'),encoding='utf-8')
print('Generated profile, statistics and activity SVGs')
