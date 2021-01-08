import pika

class BROKER:
	_HOST_ = "localhost"
	_EXCH_ = "rpi_queue"
	_TYPE_ = 'topic'
	_CONN_ = None
	_CH_ = None
	
	
	
	
	
	def __init__(self):
		#print("INIT BROKER")
		self._CONN_ = pika.BlockingConnection(pika.ConnectionParameters(host=self._HOST_, heartbeat=600, blocked_connection_timeout=300))
		self._CH_ = self._CONN_.channel()
		self._CH_.exchange_declare(exchange=self._EXCH_, exchange_type=self._TYPE_)
		
	def reconnect(self):
		self._CONN_ = pika.BlockingConnection(pika.ConnectionParameters(host=self._HOST_))
		self._CH_ = self._CONN_.channel()
		self._CH_.exchange_declare(exchange=self._EXCH_, exchange_type=self._TYPE_)	
		
		
		
	def publish(self, key="test_topic", message="test message"):
		try:
			
			self._CH_.basic_publish(exchange=self._EXCH_, routing_key=key, body=message, properties=pika.BasicProperties(expiration='4000',))
			#print(" [x] Sent %r" % message)
		except pika.exceptions.ConnectionClosed:
			print("PIKA connection closed, reopening")
			self.reconnect()
			self.publish(key, message)
		
	def subscribe(self, callback, key="test_topic"):
		result = self._CH_.queue_declare(queue='', exclusive=True)
		queue_name = result.method.queue
		self._CH_.queue_bind(exchange=self._EXCH_, queue=queue_name, routing_key=key)
		print(" [*] Activated subscriber on {}: waiting for commands".format(key))
		self._CH_.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
		self._CH_.start_consuming()
		
