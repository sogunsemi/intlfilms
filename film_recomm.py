import multiprocessing, sys, time
from ifilms import init_movie_list, collect_data
def main():
    try:
        init_movie_list()
        mProcess = multiprocessing.Process(target=collect_data)
        mProcess.daemon = True
        mProcess.start()
        print "Collecting data..."
        time.sleep(200)
    except:
        print "Error: Main process exited."
        sys.exit(0)
if __name__ == "__main__":
    main()
