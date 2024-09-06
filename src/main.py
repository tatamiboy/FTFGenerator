import os, argparse
from ui.gui import GUI
from ui.cli import CLI
from config import settings
from config.constants import Directon, Targets, TEXT_EN

if os.name == 'nt':
    print("Detected OS: Windows")
elif os.name == 'posix':
    print('Detected OS: Mac/Linux')

def main():

    message_target_list = []
    for idx, val in enumerate(list(Targets.__members__.keys())):
        if idx == 0: val += "(default)"
        message_target_list.append(f"{idx}={val}")
    message_dir_list = []
    for idx, val in enumerate(list(Directon.__members__.keys())):
        if idx == 0: val += "(default)"
        message_dir_list.append(f"{idx}={val}")

    argPaser = argparse.ArgumentParser()
    argPaser.add_argument("--cli" , action="store_true", help="CLI mode.")
    argPaser.add_argument("-i", "--input", "--video", help="Video file. Required for CLI mode.")
    argPaser.add_argument("-t", "--target" , help=f"Detection target. ({str.join(", ", message_target_list)})", type=int, default=0)
    argPaser.add_argument("-d", "--dir" , help=f"Direction. ({str.join(", ", message_dir_list)})", type=int, default=0)
    argPaser.add_argument("-c", "--chapter" , help="Chapter file.")
    argPaser.add_argument("-a", "--auto-sampling" , action="store_true", help="Enable auto downsampling.")
    argPaser.add_argument("-s", "--sampling-eps", help="Epsilon for auto downsampling.", type=float, default=settings.INITIAL_SAMPLE_EPSILON)
    args = argPaser.parse_args()

    print(args)
    if args.cli :
        if not args.input :
            print("Video file is not specified. CLI mode requires video specification. (--input)")
            return
        app = CLI(args.input, args.target, args.dir, args.auto_sampling, args.chapter)
        app.run()   
    else :
        app = GUI()
        app.start()      

if __name__ == "__main__":
    main()