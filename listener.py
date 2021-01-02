import asyncio
import logging
import json


class Listener:
  def __init__(self, ip, port, request_handler):
    self.port = port
    self.ip = ip
    self.received_msg = "ok"
    self._server = None
    self.request_handler = request_handler

  async def _listen(self):
    server = await asyncio.start_server(self.handler, self.ip, self.port)
    self._server = server

    addr = server.sockets[0].getsockname()
    logging.info(f'Serving on {addr}')

    async with server:
      await server.serve_forever()

  def listen(self):
    asyncio.run(self._listen())

  async def handler(self, reader, writer):
    data = await reader.read(1000)
    try:
      message = data.decode()
      message_dict = json.loads(message)
      self.request_handler.handle_request(message_dict)
      addr = writer.get_extra_info('peername')
      logging.debug(f"Received {message!r} from {addr!r}")

      logging.debug(f"Send: {message!r}")
      writer.write(self.received_msg.encode())
    except Exception as err:
      # writer.write(err)
      logging.exception(err)

    await writer.drain()
    logging.debug("Close the connection")
    writer.close()




def main():
  PORT = 4242
  IP = '127.0.0.1'
  logging.basicConfig(format='%(funcName)s:%(lineno)d %(levelname)s %(message)s', level=logging.INFO)
  listener = Listener(IP, PORT, handler)
  listener.listen()

def handler(message):
  logging.info(f"Received {message} in handler")

if __name__ == "__main__":
    main()