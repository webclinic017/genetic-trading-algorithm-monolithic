import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
sys.path.append(f"{str(working_dir)}/strategy")
import setup, qualify, kline, stream, session
import multiprocessing
import logging
from rich.logging import RichHandler

logging.basicConfig(level=logging.INFO,format="%(message)s",datefmt="[%X]",handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")


def run(ExchangeClient, Session, ExchangeID, CandleTimeFrame, list_symbols):
    try:
        id_0 = multiprocessing.Process(name="", target=kline.run,   args=(Session, ExchangeID, CandleTimeFrame, list_symbols))
        id_1 = multiprocessing.Process(name="", target=stream.run,  args=(Session, ExchangeID, CandleTimeFrame, list_symbols))
        id_2 = multiprocessing.Process(name="", target=session.run, args=(ExchangeClient, Session, ExchangeID, CandleTimeFrame, list_symbols))
        id_0.start()
        id_1.start()
        id_2.start()
    except Exception as e:
        logging.warning(e)


if __name__ == "__main__":

    Strategy, SessionTime, Session, bucket_name, bucket_client,\
    bucket, stage, ExchangeID, CandleTimeFrame, ExchangeClient = setup.run()

    list_symbols = qualify.run(Strategy, SessionTime, Session, bucket_name, bucket_client, bucket, stage)

    run(ExchangeClient, Session, ExchangeID, CandleTimeFrame, list_symbols)




