def getModels(id):
    
    print id
    import argparse
    import json
    import requests
    
  

        
    parser = argparse.ArgumentParser(prog='widget3')
    parser.add_argument('--genome', help='reference to genome', action='store', default=None)
    parser.add_argument('--token', help='token to authenticate to server', action='store', default='un=mendessoares|tokenid=6D172906-93C2-11E5-8500-0FA9682E0674|expiry=1480025896|client_id=mendessoares|token_type=Bearer|SigningSubject=http://rast.nmpdr.org/goauth/keys/E087E220-F8B1-11E3-9175-BD9D42A49C03|this_is_globus=globus_style_token|sig=584b3513a70a45b2c8e3b3368a51fb5816ed990956ebff53ace27b47df63d70cb29e155701f3c94609409be1c3c616b6e0d2c2641b32df7eb00612b9a15c602686fb5ea4d472e1d75fb2df5910ff695030e3c52eb74111857dd1d06e4443e38ac3532da776041a855619a8505b14a352713d2129602097ece3ece1701bd334c7')
    parser.add_argument('--url', help='url of model seed service endpoint', action='store', dest='url', default='https://p3.theseed.org/services/ProbModelSEED')
    args = parser.parse_args()
            
    # Create the headers for the request to the server.
    headers = dict()
    headers['AUTHORIZATION'] = args.token

    # Create the body of the request for the ModelReconstruction() method.
    input = dict()
    input['method'] = 'ProbModelSEED.ModelReconstruction'
    input['params'] = { 'genome': 'PATRICSOLR:%s' %id, 'gapfill': 1, 'predict_essentiality': 0, 'media':'/chenry/public/modelsupport/media/ArgonneLBMedia' }
    input['version'] = '1.1'
    
    # Send the request to the server and get back a response.
    #added exception because the website gave an error and just stopped. I'll check in the morning how this looks. I'm not sure did it right (Lena)

    response = requests.post(args.url, data=json.dumps(input), headers=headers)
            
    if response.status_code != requests.codes.OK:
        response.raise_for_status()
    output = json.loads(response.text)['result'][0] # Get the output from the method in the response
            
    # Create the body of the request for the export_model() method.
    input['method'] = 'ProbModelSEED.export_model'
    input['params'] = { 'model': output['ref'], 'format': 'sbml' }
    
    # Send the request to the server and get back a response.
            
    #added exception because the website gave an error and just stopped. I'll check in the morning how this looks. I'm not sure did it right (Lena)
    response = requests.post(args.url, data=json.dumps(input), headers=headers)
            
    if response.status_code != requests.codes.OK:
        response.raise_for_status()
    output = json.loads(response.text)['result'][0]
            
    # Store the SBML text in a file.    
    with open('../userOutput/models/%s.sbml' %id, 'w') as handle: # Use the genome ID as the file name
        handle.write(output)
            
