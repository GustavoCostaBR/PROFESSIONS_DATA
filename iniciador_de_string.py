import re
import string
import sqlite3
import urllib.request
from bs4 import BeautifulSoup
import ssl
import var_dump
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from lxml import html
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


conn = sqlite3.connect('content.sqlite')
conn.execute('PRAGMA foreign_keys = ON')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Jobs (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT UNIQUE, link TEXT UNIQUE, Profession TEXT UNIQUE, Workforce TEXT, [Average Age] REAL, [Average Salary] REAL, [Average Male Salary] REAL, [Average Female Salary] REAL, [Total of Male Workers] REAL, [Total of Female Workers] REAL, [Profession Tier] TEXT, [Salary Disparity] TEXT)')

cur.execute('CREATE TABLE IF NOT EXISTS Vari (Jobs_id INTEGER UNIQUE, vari FLOAT, dev FLOAT, [vari acumul] FLOAT, [disparidade salarial] FLOAT, [disparidade salarial relacao media] FLOAT, [disparidade salarial relacao media cumulativa] FLOAT, FOREIGN KEY(Jobs_id) REFERENCES Jobs(id))')

cur.execute('CREATE TABLE IF NOT EXISTS Keywords (id INTEGER PRIMARY KEY AUTOINCREMENT, palavra TEXT UNIQUE, validador INTEGER)')

keywords_0 = list(string.ascii_lowercase)
keywords_1 = ['administrator', 'advertiser', 'advocate', 'agent', 'agriculturist', 'analyst', 'animator', 'architect', 'artist', 'athlete', 'attorney', 'auctioneer', 'auditor', 'author', 'baker', 'banker', 'barber', 'bartender', 'biologist', 'blacksmith', 'bookkeeper', 'botanist', 'broker', 'builder', 'butcher', 'buyer', 'cameraman', 'carpenter', 'cartographer', 'cashier', 'ceramicist', 'chef', 'chemist', 'chiropractor', 'cleaner', 'clergy', 'coach', 'collector', 'comedian', 'composer', 'conductor', 'construction', 'consultant', 'contractor', 'cook', 'coordinator', 'counselor', 'curator', 'customer', 'dancer', 'data', 'dentist', 'designer', 'developer', 'dietitian', 'director', 'doctor', 'draftsman', 'driver', 'economist', 'editor', 'educator', 'electrician', 'engineer', 'entrepreneur', 'environmentalist', 'executive', 'fabricator', 'farmer', 'fashion', 'filmmaker', 'financier', 'firefighter', 'fisherman', 'florist', 'food', 'forester', 'furniture', 'gardener', 'geologist', 'glassblower', 'glazier', 'government', 'graphic', 'hairdresser', 'health', 'historian', 'home', 'horticulturist', 'hospitality', 'human', 'illustrator', 'industrial', 'information', 'insurance', 'interior', 'interpreter', 'inventor', 'investigator', 'jeweler', 'journalist', 'judge', 'landscaper', 'lawyer', 'librarian', 'lighting', 'lineman', 'logger', 'machinist', 'magician', 'maid', 'manager', 'manicurist', 'manufacturer', 'marine', 'marketing', 'masseur', 'mathematician', 'mechanic', 'medical', 'merchant', 'meteorologist', 'microbiologist', 'military', 'miner', 'model', 'musician', 'nanny', 'naturalist', 'news', 'nurse', 'nutritionist', 'occupational', 'oceanographer', 'office', 'optician', 'optometrist', 'orthodontist', 'osteopath', 'painter', 'paralegal', 'paramedic', 'parks', 'patent', 'pathologist', 'pension', 'personal', 'pest', 'pharmacist', 'philosopher', 'photographer', 'physicist', 'physician', 'physiotherapist', 'pianist', 'pilot', 'planner', 'plumber', 'podiatrist', 'poet', 'police', 'politician', 'porter', 'postal', 'potter', 'printer', 'producer', 'professor', 'programmer', 'psychiatrist', 'psychologist', 'public', 'publisher', 'purchaser', 'quality', 'radiologist', 'real', 'receptionist', 'recreational', 'recruiter', 'referee', 'refrigeration', 'reporter', 'researcher', 'restaurant']
keywords_2 = ['researcher','retail','sales','scientist','social','software','solicitor','strategist','student','supervisor','surgeon','surveyor','teacher','technician','therapist','trader','trainer','translator','travel','tutor','undertaker','university','urban','usability','user','ux','veterinarian','vet','video','virtual','volunteer','waiter','waitress','warden','warehouse','watchmaker','web','wedding','wellness','wildlife','window','wine','woodworker','writer','yoga','youth','zookeeper', 'detailed']
listacompleta=keywords_0 + keywords_1+ keywords_2
#print(listacompleta)
for palavrinha in listacompleta:
	cur.execute('INSERT OR IGNORE INTO Keywords (palavra, validador) VALUES ( ?, ? )', (palavrinha, 1) )
	conn.commit()
#		if cur.rowcount == 0:
#			cur.execute('UPDATE Keywords SET validador = ? WHERE palavra = ?', (2, palavrinha,))
#		else:
#			continue
conn.close()