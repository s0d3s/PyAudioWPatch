from threading import Thread
import time


class Spinner(Thread):
    """Helper class for examples"""
    def __init__(self, spinner_style: int = 1) -> None:
        super().__init__()
        self.style = spinner_style
        self.running = False
        self.output_queue = []
        
    def start(self) -> None:
        self.running = True
        super().start()
        
    def stop(self) -> None:
        while len(self.output_queue)>0:
            time.sleep(0.05)
        self.running = False
        super().join()
        self.clear()
        
    def clear(self) -> None:
        print(f"\r{' '*20}\r", end="")
        
    def print(self, msg: str) -> None:
        self.output_queue.append(msg)
        
    def run(self) -> None:
        def spinner_generator(style: int = 0):
            sp_styles = [
                ["◌","○","●","○",],
                ["█","▓","▒","░","▒","▓",],
                ["/","|","\\",]
            ]
            sp_list = sp_styles[style % len(sp_styles)]
            last_sp_index = 0
            while True:
                yield sp_list[last_sp_index]
                last_sp_index = (last_sp_index+1)%len(sp_list)
                
        sp_gen = spinner_generator(self.style)
        
        while self.running:
            self.clear()
            if len(self.output_queue) > 0:
                print(self.output_queue.pop(0))
            print(f"\r{next(sp_gen)}", end="")    
            time.sleep(0.1)
        
    def __enter__(self) -> 'Spinner':
        self.start()
        return self
        
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.stop()

if __name__ == "__main__":
    with Spinner() as spinner:
        spinner.print("Some text")    
        time.sleep(3)