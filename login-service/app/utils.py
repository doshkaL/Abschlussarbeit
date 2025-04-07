#from ldap3 import Server, Connection, ALL, NTLM
#from app.config import config

#d##ef authenticate_user(matrikelnummer, password):
   # server = Server(config.LDAP_SERVER, port=config.LDAP_PORT, use_ssl=config.LDAP_SSL, get_info=ALL)
    #user_dn = config.LDAP_USER_DN.format(matrikelnummer)
    
   # try:
       # conn = Connection(server, user=user_dn, password=password, authentication=NTLM, auto_bind=True)
        #return conn.bound
    #except Exception as e:
        #return False
