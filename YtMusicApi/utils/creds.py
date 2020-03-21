import json

def load_creds(ROOT_DIR):
        try: 
            with open(ROOT_DIR + '/creds.json') as f:
                data = json.load(f)
                username = data['username']
                password = data['password']

            return username, password
            
        except Exception as e: print(e)