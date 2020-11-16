#!/usr/bin/env python
# encoding: utf-8

import os
import csv
import datetime

from decimal import Decimal
from decimal import ROUND_DOWN, ROUND_HALF_EVEN

class Pokemon():
	Num = ''
	Stamina = 0
	Attack = 0
	Defese = 0

class Cpm():
	Level = 0
	CPM = 0

class Stat():
	Num = 0
	Level = 0
	Attack = 0
	Defense = 0
	Stamina = 0
	CP = 0
	CPM = 0
	Stats = 0

csvpath = os.path.dirname(os.path.realpath(__file__))
pogo_stats = os.path.join(csvpath, "pokemongo_stats.csv")
pogo_cpm = os.path.join(csvpath, "pokemongo_cpm.csv")

pokemon_cpm = []
with open(pogo_cpm, 'r') as f:
	reader = csv.DictReader(f, delimiter=',')
	for row in reader:
		c = Cpm()
		c.Level = row['Level']
		c.CPM = Decimal(row['CP Multiplier'])
		pokemon_cpm.append(c)

pokemons = []
with open(pogo_stats, 'r') as f:

	reader = csv.DictReader(f, delimiter=',')
	for row in reader:
		p = Pokemon()
		p.Num = row['Pokemon Num']
		p.Stamina = Decimal(row['Stamina'])
		p.Attack = Decimal(row['Attack'])
		p.Defense = Decimal(row['Defense'])
		pokemons.append(p)

print("Start time.......: {0}".format(datetime.datetime.now().strftime('%d/%m_%H:%M:%S')))
print("Total cpm/levl...: {0}".format(len(pokemon_cpm)))
print("Total pokemons...: {0}".format(len(pokemons)))

# pokemon
for p in pokemons:
	pokemon_stats = []
	# attack
	for a in range(0,16):
		# defense
		for d in range(0,16):
			# stamina
			for s in range(0,16):
				# cpm / levels
				for c in pokemon_cpm:
					stat = Stat()
					stat.Num = p.Num
					stat.Attack = a
					stat.Defense = d
					stat.Stamina = s
					stat.Level = c.Level
					stat.CPM = c.CPM

					stat.CP = ( ((Decimal(p.Attack  + a)) *
						(Decimal(p.Defense + d) ** Decimal(0.5)) *
						(Decimal(p.Stamina + s) ** Decimal(0.5)) *
						Decimal(c.CPM ** 2) ) / Decimal(10) ).quantize(
							Decimal('0'), rounding=ROUND_DOWN)

					stat.Stats = Decimal( Decimal((p.Attack  + a) * c.CPM).quantize(Decimal('.01'), rounding=ROUND_HALF_EVEN) *
							 Decimal((p.Defense + d) * c.CPM).quantize(Decimal('.01'), rounding=ROUND_HALF_EVEN) *
							 Decimal((p.Stamina + s) * c.CPM).quantize(Decimal('.01'), rounding=ROUND_HALF_EVEN) ).quantize(
								Decimal('.01'), rounding=ROUND_HALF_EVEN)

					pokemon_stats.append(stat)

	# Sort dict and search for max stats
	max_stats_mega = 0
	max_stats_ultra = 0
	with open("pogo_stats_max.out", 'a+') as f:
		for s in sorted(pokemon_stats, key=lambda x: (x.CP, x.Stats), reverse=True):
			if (max_stats_mega == 0) and (s.CP >= 1400) and (s.CP <= 1500):
				max_stats_mega = s.Stats
			if (max_stats_ultra == 0) and (s.CP >= 2400) and (s.CP <= 2500):
				max_stats_ultra = s.Stats
		if (max_stats_mega != 0) or (max_stats_ultra != 0):
			f.write("{0},{1},{2}\n".format(s.Num, max_stats_mega, max_stats_ultra))

	# Write to file
	with open("pogo_stats.out", 'a+') as f:
		for s in sorted(pokemon_stats, key=lambda x: (x.Stats, x.CP), reverse=True):
			perc_mega = 0
			perc_ultra = 0
			if (s.CP <= 1500) and (max_stats_mega != 0):
				perc_mega = Decimal(s.Stats / max_stats_mega * 100).quantize(Decimal('.0'))
			if (s.CP <= 2500) and (max_stats_ultra != 0):
				perc_ultra = Decimal(s.Stats / max_stats_ultra * 100).quantize(Decimal('.0'))

			if (perc_mega >= 90) or (perc_ultra >= 90):
				txt = "{0} l:{1:>4} a:{2:2d} d:{3:2d} s:{4:2d} cp:{5} stats:{6} mega:{7:6.2f} ultra:{8:6.2f}]".format(
					s.Num,
					s.Level,
					s.Attack,
					s.Defense,
					s.Stamina,
					s.CP,
					s.Stats,
					perc_mega,
					perc_ultra)
				f.write(txt + "\n")
				#print(txt)

	print("Pokemon {0:>7} : {1}".format(p.Num, datetime.datetime.now().strftime('%d/%m_%H:%M:%S')))

print("End time.........: {0}".format(datetime.datetime.now().strftime('%d/%m_%H:%M:%S')))





# === VIM modeline ===
# :set modeline
# :e [reload buffer]
# vim: tabstop=4 shiftwidth=4 noexpandtab
# eof
