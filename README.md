# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

## Recommended IDE Setup

- [VS Code](https://code.visualstudio.com/) + [Vue - Official](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (previously Volar) and disable Vetur

Option 1: Generate a New Self-Signed Certificate
Generate a new private key:

bash
Copy code
openssl genpkey -algorithm RSA -out key.pem
Generate a new certificate signing request (CSR):

bash
Copy code
openssl req -new -key key.pem -out cert.csr -subj "/CN=127.0.0.1"
Generate the self-signed certificate:

bash
Copy code
openssl x509 -req -days 365 -in cert.csr -signkey key.pem -out cert.pem
Use the new certificate in your Flask app:

python
Copy code
app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
Test with curl:

bash
Copy code
curl https://127.0.0.1:5000/api/healthcheck --insecure

curl -k https://127.0.0.1:5000/api/healthcheck

Install ngrok via Homebrew with the following command:
brew install ngrok/ngrok/ngrok

Run the following command to add your authtoken to the default ngrok.yml configuration file.
ngrok config add-authtoken ${auth_key}

Deploy your app online
ngrok http ${http://localhost:8080} --host-header=rewrite



# gunicorn -w 4 -b 0.0.0.0:5000 --certfile=../server/cert.pem --keyfile=../server/key.pem app:app

# sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
# sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/local/bin/nginx
# sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblockapp /usr/local/bin/nginx

# sudo brew services restart nginx

# curl -k https://172.20.10.5:5000/api/
# curl -k https://161.3.32.40:5000/api/
# curl -k https://127.0.0.1:5000/api/