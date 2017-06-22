# Facebook webhook over Python
###### A basic example for webhook to Facebook messenger

##### Ejecutar
```sh
$ pip install -r requirements.txt
```

### Notas:
Para poder ingresar URLs en los templates de Facebook, es necesario dar de alta los dominios donde se consumiran los recursos, con CURL sería algo como 

```sh
curl -X POST \
  'https://graph.facebook.com/v2.6/me/thread_settings?access_token=TOKEN' \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{
  "setting_type" : "domain_whitelisting",
  "whitelisted_domains" : ["https://aad6ae76.ngrok.io"],
  "domain_action_type": "add"
}'
```

Para verificar la suscripcion se usará:
```sh
curl -X GET \
  'https://graph.facebook.com/v2.6/me/thread_settings?fields=whitelisted_domains&access_token=TOKEN' \
  -H 'cache-control: no-cache' \
```
