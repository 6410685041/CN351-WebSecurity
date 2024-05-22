import asyncio
from aiosmtpd.controller import Controller

class DebuggingHandler:
    async def handle_DATA(self, server, session, envelope):
        print('Message from:', envelope.mail_from)
        print('Message to  :', envelope.rcpt_tos)
        print('Message data:')
        print(envelope.content.decode('utf8', errors='replace'))
        print('End of message')
        return '250 OK'

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    controller = Controller(DebuggingHandler(), hostname='localhost', port=1025)
    controller.start()
    print('SMTP server is running on localhost:1025')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()
