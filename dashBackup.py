import requests, json, zipfile
from HTMLParser import HTMLParser
import tempfile, shutil, sys, zipfile, os
import datetime

class dashBackup(object):
	def __init__(self):
		self.sourceOAuth = "OAuth 00D1I000000mhr9!AQcAQAfXXSaG.bdWdtoET.b7x5XanvzgTkoj8Qehq_x6ooGXPdgdY7Nhh4c_TP.Xy_XSgwWvQn8RtIT.CtYbnOlSQLZjjRKxp_Z"
		self.sourceInst = "https://tomasz234.my.salesforce.com"

	def getDashboardsJson(self):
			#inApps = [x['source'] for x in self.appsMap]
			inApps = None
			header = {"Authorization": self.sourceOAuth}
			header["Content-Type"] = 'application/json'
			done = False
			nextPageUrl = '/services/data/v41.0/wave/dashboards'
			dashUrls = []
			dashDict = {}
			
			while not done:
				resp = requests.get(self.sourceInst + nextPageUrl, headers = header)

				respJson = json.loads(resp.text)
				if isinstance(respJson, list):
						print("Error! Unable to download dashboards")
						print(respJson)
						sys.exit()
				for dash in respJson['dashboards']:
					if (inApps == None):
						dashUrls.append(dash['url'])
					elif (('folder' in dash) and ('name' in dash['folder']) and (dash['folder']['name'] in inApps)):
						dashUrls.append(dash['url'])
				
				if respJson['nextPageUrl'] == None:
					done = True
				else:
					nextPageUrl = respJson['nextPageUrl']

			for jsonUrl in dashUrls:
				print jsonUrl
				resp = requests.get(self.sourceInst+jsonUrl, headers = header)
				try:
					jsonDash = json.loads(resp.text)
					dashDict[jsonDash['name']] = jsonDash
				except:
					print "Unable to get dashboard with url: {0}".format(jsonUrl)
					continue
					
			return dashDict

	def cleanJson(self, dashDict):
		h = HTMLParser()	
		for keyStep, valueStep in dashDict['state']['steps'].items():
			if 'query' in valueStep:
				if valueStep['type'] != "saql":
					unescapedQuery = h.unescape(valueStep['query']['query'])
					dashDict['state']['steps'][keyStep]['query'] = json.loads(unescapedQuery)

			elif 'values' in valueStep:
				valuesArray = []
				for val in valueStep['values']:
					valuesArray.append(json.loads(h.unescape(val)))

				valueStep['values'] = valuesArray

				if 'start' in valueStep:
					valueStep['start'] = json.loads(h.unescape(valueStep['start']))

		for keyWidget, valueWidget in dashDict['state']['widgets'].items():
			for keyParam, valueParam in valueWidget['parameters'].items():
				if type(valueParam) == unicode:
					dashDict['state']['widgets'][keyWidget]['parameters'][keyParam] = h.unescape(valueParam)
		
		return self.modify_all_simple_dict_values(dashDict, self.replaceEscapes)
		#return dashDict

	def modify_all_simple_dict_values(self, data, modfn):
		if isinstance(data, dict):
			for k, v in data.iteritems():
				if (isinstance(v, dict) or
					isinstance(v, list) or
					isinstance(v, tuple)
					):
					self.modify_all_simple_dict_values(v, modfn)
				else:
					data[k] = modfn(k, v)
		elif isinstance(data, list) or isinstance(data, tuple):
			for item in data:
				self.modify_all_simple_dict_values(item, modfn)

   		return data

	def replaceEscapes(self, key, value):
		if isinstance(value, unicode) or isinstance(value, str):
			value = value.replace('&quot;', '"')
			value = value.replace("&#39;", "'")

		return value

	def saveToFiles(self, dashDict):
		currentDir = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f'))
		os.makedirs(currentDir)
		for key, value in dashDict.items():
			with open(os.path.join(currentDir, key+'.json'), 'w') as fileout:
				fileout.write(json.dumps(value))
			print(key+'.json' + " Written!")

		print("Dashboards saved in directory: " + currentDir)
	
	def saveToFilesZip(self, dashDict):
		tmpdir = tempfile.mkdtemp()
		for key, value in dashDict.items():
			filename = os.path.join(tmpdir, key+'.json')
			with open(filename, 'w') as fileout:
				fileout.write(json.dumps(value))
			print(filename)
		
		zipf = zipfile.ZipFile('dashboards.zip', 'w', zipfile.ZIP_DEFLATED)
		dashBackup.zipdir(tmpdir, zipf)
		zipf.close()

		#shutil.rmtree(tmpdir)

	@staticmethod
	def zipdir(path, ziph):
		# ziph is zipfile handle
		for root, dirs, files in os.walk(path):
			for file in files:
				ziph.write(os.path.join(root, file))

		
def downloadAndSave():
		inst = dashBackup()
		dashDicts = inst.getDashboardsJson()
		for key, value in dashDicts.items():
			dashDicts[key] = inst.cleanJson(value)
		
		inst.saveToFiles(dashDicts)

if __name__ == "__main__":
	downloadAndSave()