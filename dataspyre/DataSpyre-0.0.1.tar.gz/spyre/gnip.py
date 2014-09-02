# from spyre import server
import server

from nbsutils import imp
import matplotlib.pyplot as plt
import pandas as pd
import numpy
import urllib2, base64
import json
from datetime import datetime as dt


class MyLaunch(server.Launch):
	templateVars = {"shared_fields" : [
								{"label": 'Standard Error', "value": 15, "variable_name": 'std_err', "inumpyut_type":'text'},
								{"label": 'Max Sample Rate', "value": 40, "variable_name": 'max_rate', "inumpyut_type":'text'},
								{"label": 'Sample Threshold', "value": 100, "variable_name": 'samp_thresh', "inumpyut_type":'text'},
						],
					"controls" : [
					{"output_type" : "image",
						"control_type" : "button",
						"control_name" : "button1",
						"output_name" : "plot",
						"button_label" : "Plot",
						"button_id" : "submit-plot",
						"on_page_load" : "true",
						"text_fields" : []
					},
					{"output_type" : "table",
						"control_type" : "button",
						"control_name" : "button2",
						"button_label" : "Load Table",
						"button_id" : "load-table",
						"text_fields" : []
					},
					{
						"control_type" : "button",
						"control_name" : "refresh_data_button",
						"button_label" : "Refresh Data",
						"button_id" : "refresh-data",
						"text_fields" : []
					}
					]
				}
	
	def __init__(self):
		# due to an issue with impala retweets and mentions, we need to multiply by a correction factor
		# TODO: fix impala issue
		self.correction_factor = 4.6  
		
		# make necessary impala query
		# TODO: add button to refresh this data
		self.historical_data = self.getHistoricalData()	 
	
	
	def getData(self, params):
		df = self.getDataFrame(params)
		
		# turn NA's and floats into pretty strings (with single digit precision)
		df = df.fillna("")
		df_string = pd.DataFrame()
		for col in df.columns:
			tmp = []
			if col=='day_of_month':
				df_string[col] = df[col]
				continue
			for i in df.index:
				try:
					tmp.append('%.1f' % df[col][i])
				except:
					tmp.append("")
			df_string[col] = tmp
		return df_string

	def getDataFrame(self,params):
		std_error_pct = int(params['std_err'])
		max_sample_rate = int(params['max_rate'])
		baseline = int(params['samp_thresh'])
		
		# make call to gnip api to get usage for current month
		# uncomment second line and edit fromDate and toDate to get usage data from a specific time period
		api_endpoint = 'https://account-api.gnip.com/accounts/NextBigSound/usage.json?bucket=day'
# 		api_endpoint = 'https://account-api.gnip.com/accounts/NextBigSound/usage.json?bucket=day&fromDate=201408010000&toDate=201408120000'
		username = 'bugs@nextbigsound.com'
		password = 'KfQu1a13SqFgMxDurCio'
		request = urllib2.Request(api_endpoint)
		base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
		request.add_header("Authorization", "Basic %s" % base64string)   
		result = urllib2.urlopen(request)
		r = json.loads(result.read())
		
		# put gnip data into a data frame
		publishers = r['publishers']
		dates = []
		days = []
		tweets = []
		total_tweets = []
		projected_total_tweets = []
		updated_projection = []
		days_in_month = 31
		for p in publishers:
			if p['name'] == 'Twitter':
				for d in p['used']:
					dates.append(dt.strptime(d['fromDate'][:8], "%Y%m%d").date())
					days.append(dt.strptime(d['fromDate'][:8], "%Y%m%d").date().day)
					projected_total_tweets.append(None)
					updated_projection.append(None)
					tweets.append(1.0*d['activities']/10**6)
					total_tweets.append(sum(tweets))

		# figure out projected values for the rest of the month
		daily_change = numpy.mean(tweets)
		estimated_daily_change = 1.0*self.estimate_tweet_volume(std_error_pct, baseline, max_sample_rate)/10**6
		last_day = max(days)
		last_day_value = total_tweets[-1]
		projected_total_tweets[-1] = last_day_value
		updated_projection[-1] = last_day_value
		for i in range(last_day+1,days_in_month+1):
			projected_total_tweets.append(projected_total_tweets[-1]+daily_change)
			updated_projection.append(updated_projection[-1]+estimated_daily_change)
			days.append(i)
			total_tweets.append(None)
			tweets.append(None)

		df = pd.DataFrame({'day_of_month':days,'daily_tweets':tweets,'total_tweets':total_tweets,'projected_total_tweets':projected_total_tweets, 'updated_projection':updated_projection})
		return df

	def getPlot(self, params):
		# plot past and projected data
		df = self.getDataFrame(params)
		fig = plt.figure()
		splt = fig.add_subplot(1,1,1)
		splt.plot(df['day_of_month'], df['daily_tweets'], label="tweets per day")
		splt.plot(df['day_of_month'], df['total_tweets'], label="total tweets to date")
		splt.plot(df['day_of_month'], df['projected_total_tweets'], label="projected total tweets")
		splt.plot(df['day_of_month'], df['updated_projection'], label="updated projection")
		splt.axhline(y=60, linestyle =':')
		splt.set_ylabel('tweets (in millions)')
		splt.set_xlabel('day of month')
		splt.legend(loc=2)
		return fig
	
	def getHistoricalData(self):
		# impala query to get number of retweets and mentions from 5 days ago
		db = imp.Connection()
		query = "SELECT DISTINCT unix_seconds FROM idx_entity WHERE metric_id=247 AND count_type='d' ORDER BY unix_seconds DESC LIMIT 5"
		tss = db.fetchAll(query)
		ts = tss['unix_seconds'].tolist()[-1]
		query247 = """SELECT value, COUNT(*) as cnt FROM idx_entity 
		WHERE metric_id=247 AND count_type='d' AND unix_seconds={} 
		GROUP BY value""".format(ts)
		query248 = """SELECT value, COUNT(*) as cnt FROM idx_entity 
		WHERE metric_id=248 AND count_type='d' AND unix_seconds={} 
		GROUP BY value""".format(ts)
		df247 = db.fetchAll(query247)
		df248 = db.fetchAll(query248)
		db.close()
		df247['total'] = df247['value']*df247['cnt']
		df248['total'] = df248['value']*df248['cnt']
		df = pd.concat([df247,df248],ignore_index=True)
		return df
	
	def estimate_tweet_volume(self, std_error_pct, baseline, max_sample_rate):
		# estimate daily tweet volume based on the df from getHistoricalData and the sampling formula
		correction_factor = self.correction_factor
		df = self.historical_data
		sample_rate = []
		sample_freq = []
		for i in df.index:
			actual_freq = df['total'][i]
			if actual_freq > baseline:
				raw_sample_rate = 100.0/(actual_freq*numpy.power(std_error_pct/100.0, 2.0) + 1.0)
			else:
				raw_sample_rate = 100.0
			sampleRate = numpy.ceil(min(raw_sample_rate,max_sample_rate))
			sample_rate.append(sampleRate)
			sample_freq.append(sampleRate*actual_freq/100.0)
		df['sample_rate'] = sample_rate
		df['sample_freq'] = sample_freq
		df['sample_freq_corrected'] = df['sample_freq']*correction_factor
		return(sum(df['sample_freq_corrected']))

ml = MyLaunch()
ml.launch(port="9090")

