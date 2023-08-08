import json
from pynginxconfig import NginxConfig

nc = NginxConfig()
nc.loadf('test.conf')
# print(f"data: {json.dumps(nc.data,indent=4)}")
print(f"data: {json.dumps(nc.data)}")
# nc.append(item={'name':'events', 'param':'', 'value':[('connections', '2000'), ('use', 'kqueue')]},position=0)

print(f"nc data len: {len(nc.data)}")
for item in nc.data:
    print(f"item: {item}, {type(nc.data[0])}")

# nc.set([('server',),('worker_connections')], '999')
# nc.remove([('server',),('location','/name/')])
# nc.remove([('server',),("server_name")])
# nc.remove([('server',)])
nc.append_value(
    name="/gavin/", rule=[('proxy_pass', 'http://127.0.0.1/remote/')])
# nc.append_value(name="/name/",rule=[('proxy_socket_keepalive', 'off')])
print("--"*20)
# print(f"after data: {json.dumps(nc.data,indent=4)}")
nc.savef('nginx_new.conf')


# import crossplane
# import nginx
#
# filename="servers.conf"
#
# payload = crossplane.parse(filename)
# print(f"payload: {payload}")
#
# # c = nginx.loadf(filename)
# # print(f"c: {c}")
# # print(f"server: {c.servers}")
# # print(f"string: {c.as_strings}")
