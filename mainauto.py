import multiprocessing
from monitor.file_monitor import monitor_folder
from ransomware_sim.ransomware_script import simulate_attack

if __name__ == "__main__":
    monitor_proc = multiprocessing.Process(target=monitor_folder)
    simulate_proc = multiprocessing.Process(target=simulate_attack)

    monitor_proc.start()
    simulate_proc.start()

    monitor_proc.join()
    simulate_proc.join()
