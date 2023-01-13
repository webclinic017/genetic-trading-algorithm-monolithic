import sys, pathlib, time, sys, logging, time, schedule, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent
working_dir = pathlib.Path(__file__).resolve().parent.parent
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
from multiprocessing import Process
import plot_report
from rich.logging import RichHandler
logging.basicConfig(level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)],)
log = logging.getLogger("rich")
#___________________________________________________________________________________

def multi_run():

    p1 = Process(target=plot_report.run, args=('BINANCE',))
    p2 = Process(target=plot_report.run, args=('BINANCETESTNET',))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
#___________________________________________________________________________________

def run():
    multi_run()

    schedule.every(2).hours.do(multi_run)

    # test
    # schedule.every(10).seconds.do(investment_report.multi_run)

    while True:
        schedule.run_pending()
        time.sleep(1)
#___________________________________________________________________________________

if __name__ == "__main__":

    run()
