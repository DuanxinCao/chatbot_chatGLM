import redis
import tair

class TairWrapper(object):
    def __init__(self,host:str,port:str,password=None):
        self.client = tair.Tair(host,port,password=password)

    def set(self,key:str,value:str):
        try:
            self.client.set(key,value)
        except Exception as e:
            return f"Error with {e}"

    def get(self,key:str):
        try:
            result = self.client.get(key)
            return result
        except Exception as e:
            return f"Error with {e}"
