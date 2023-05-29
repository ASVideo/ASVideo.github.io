import pandas as pd
import os
import glob


LANGUAGES = { 	"zh-tw" : "",
		"en"	: "_en",
		"ja"	: "_ja",
	}

data = pd.read_csv("data.csv")


for lang in LANGUAGES:
	print(lang)

	ALL = {}
	for file in glob.glob(f"data/*-summary{LANGUAGES[lang]}.txt"):
		file = file[5:]
		tokens = file.split("-summary")
		df = data.loc[data['date'] == tokens[0]]
		v_youtube_ID = df['youtube_ID'].iloc[0]
		v_title = df['title'].iloc[0]
		v_speaker = df['speaker'].iloc[0]
		v_affiliation = df['affiliation'].iloc[0]
		v_event = df['event'].iloc[0]
		v_host = df['host'].iloc[0]
		year = tokens[0][0:4]

		if year not in ALL:
			ALL[year] = {}

		ALL[year][tokens[0]] =  v_youtube_ID

	for year in ALL:
		if not os.path.exists(f"output/{year}"):
			os.makedirs(f"output/{year}")

		with open(f"output/{year}/_index.{lang}.md", "w") as outfile:

			outfile.write("---\n")
			outfile.write("title: \"" + year + "\"\n")
			outfile.write("weight: " + str(2300-int(year)) + "\n")
			outfile.write("chapter: true\n")
			outfile.write("---\n\n\n")


			for day in ALL[year]:
				outfile.write("{{<youtube id=\"" + ALL[year][day] + "\">}}")
				outfile.write("\n\n")
				with open(f"data/{day}-summary{LANGUAGES[lang]}.txt") as infile:
					summary = infile.read()
					outfile.write(summary)
				outfile.writelines("\n\n")

	
	
