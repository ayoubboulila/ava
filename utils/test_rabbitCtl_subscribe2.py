from RabbitCtl import BROKER


br = BROKER()

def callback(ch, method, properties, body):
	print(" [x] callback %r" % body)
	print("key: {}".format(method.routing_key))
	#br.publish("test_topic2", "published from callback")
	


br.subscribe(callback, "test_topic2")