def getModels(id, url='https://p3.theseed.org/services/ProbModelSEED', runapp=True, wsurl='https://p3.theseed.org/services/Workspace'):
    
    print id
    import json
    import requests
    import time
  

    token = 'un=mendessoares|tokenid=6D172906-93C2-11E5-8500-0FA9682E0674|expiry=1480025896|client_id=mendessoares|token_type=Bearer|SigningSubject=http://rast.nmpdr.org/goauth/keys/E087E220-F8B1-11E3-9175-BD9D42A49C03|this_is_globus=globus_style_token|sig=584b3513a70a45b2c8e3b3368a51fb5816ed990956ebff53ace27b47df63d70cb29e155701f3c94609409be1c3c616b6e0d2c2641b32df7eb00612b9a15c602686fb5ea4d472e1d75fb2df5910ff695030e3c52eb74111857dd1d06e4443e38ac3532da776041a855619a8505b14a352713d2129602097ece3ece1701bd334c7'
            
    # Create the headers for the request to the server.
    headers = dict()
    headers['AUTHORIZATION'] = token

    # Create the body of the request for the ModelReconstruction() method.
    input = dict()
    input['method'] = 'ProbModelSEED.ModelReconstruction'
    input['params'] = { 'genome': 'PATRIC:%s' %id, 'gapfill': 1, 'predict_essentiality': 0, 'media':'/chenry/public/modelsupport/media/ArgonneLBMedia' }
    input['version'] = '1.1'
    
    # Send the request to the server and get back a response.
    #added exception because the website gave an error and just stopped. I'll check in the morning how this looks. I'm not sure did it right (Lena)
    
    
    requests.packages.urllib3.disable_warnings()
    response = requests.post(url, data=json.dumps(input), headers=headers, verify = False)
            
    if response.status_code != requests.codes.OK:
        response.raise_for_status()
        
    jobid = json.loads(response.text)['result'][0] # Get the output from the method in the response
    
    # Wait for the job to finish when model reconstruction is run as an app.
    if runapp:
        input['method'] = 'ProbModelSEED.CheckJobs'
        input['params'] = { 'jobs': [ jobid ] }
        done = False
        while not done:
            response = requests.post(url, data=json.dumps(input), headers=headers)
            if response.status_code != requests.codes.OK:
                response.raise_for_status()
            output = json.loads(response.text)['result'][0]
            if jobid in output:
                task = output[jobid]
                print task['status']
                if task['status'] == 'failed':
                    # Still waiting on a fix to get the error returned in the output
                    raise Exception
                elif task['status'] == 'completed':
                    done = True
                else:
                    time.sleep(3)
            else:
                raise Exception
     
        print task
    
    # Create the body of the request for the export_model() method.
    # When ModelSEED server is reliable we could switch back to this method.
#     input['method'] = 'ProbModelSEED.export_model'
#     input['params'] = { 'model': '/mendessoares/home/models/'+id+'_model', 'format': 'sbml' }
    
    # Create the body of the request for the get() method.
    input['method'] = 'Workspace.get'
    input['params'] = { 'objects': [ '/mendessoares/home/models/.'+id+'_model/'+id+'_model.sbml' ] }
    
    # Send the request to the server and get back a response.            
    #added exception because the website gave an error and just stopped. I'll check in the morning how this looks. I'm not sure did it right (Lena)
    response = requests.post(wsurl, data=json.dumps(input), headers=headers)
            
    if response.status_code != requests.codes.OK:
        response.raise_for_status()
    output = json.loads(response.text)['result'][0]
            
    # Store the SBML text in a file.    
    with open('../userOutput/models/%s.sbml' %id, 'w') as handle: # Use the genome ID as the file name
        handle.write(output[0][1]) # File data is in the second element of the returned tuple
            
