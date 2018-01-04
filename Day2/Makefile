encrypt-secret:
	openssl enc -aes-256-cbc -salt -a -in api_keys.json -out api_keys.json.enc

decrypt-secret:
	openssl enc -aes-256-cbc -salt -a -d -in api_keys.json.enc -out api_keys.json
