memory_usage_log = open("memory_usage_log.txt","w")

data = "aqui texto aqui".encode()
memory_usage_log.write(data.decode("utf-8"))
print(type(data))