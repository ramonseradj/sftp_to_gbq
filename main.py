from google.cloud import storage
import pandas as pd
import pandas_gbq
import pysftp
from google.oauth2 import service_account

#Create function that is triggered by http request
def importCsv():

    #BigQuery information
    project_id = ""
    dataset = ""
    table = ""
    destination = f"{dataset}.{table}"

    #Connection Params
    myHostname = "" #hostname
    myUsername = "" #username
    myPassword = "" #password
    myDefaultPath = "" #path to file
    file_name = "" #filename
    port = 22 #port
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    cf_path = '/tmp/{}'.format(file_name)

    #Load Data
    sftp = pysftp.Connection(host=myHostname,port=port,username=myUsername,password=myPassword,cnopts=cnopts,default_path=myDefaultPath)
    sftp.get(file_name,cf_path)

	# Retrieve credentials from the service account file (assuming in /tmp)
    credentials_path = "./service_account.json" #path to service account file

	# Read CSV into dataframe using pandas
    df = pd.read_csv(cf_path)

	# Optionally transform the dataframe for BigQuery destination
    ##

	# Load df to BigQuery
    pandas_gbq.to_gbq(df, destination, project_id = project_id, if_exists="replace")

def run_import(data, context):
	importCsv()
	print("all functions executed.")